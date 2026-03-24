import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import json
import re
import argparse
from datetime import datetime
from urllib.parse import urljoin, urlparse
import time
import os
import sys
import signal
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass

REQUEST_TIMEOUT = 5.0
REQUEST_RETRIES = 3
RETRY_SLEEP_SECONDS = 2.0
METADATA_REQUEST_TIMEOUT = REQUEST_TIMEOUT
METADATA_REQUEST_RETRIES = REQUEST_RETRIES
METADATA_RETRY_SLEEP_SECONDS = RETRY_SLEEP_SECONDS
DBLP_REQUEST_INTERVAL_SECONDS = 4.0
ENABLE_METADATA_CACHE = True
PER_ITEM_SLEEP_SECONDS = 1.0
PER_PUBLICATION_TIMEOUT_SECONDS = 20
MAX_WORKERS = 1
DEFAULT_DBLP_URL = "https://dblp.org/pid/c/SCCheung.html"
DEFAULT_CONFIG_FILENAME = "config.json"
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PublicationScraper/1.0; +https://dblp.org)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

_THREAD_LOCAL = threading.local()
_DBLP_RATE_LIMIT_LOCK = threading.Lock()
_DBLP_NEXT_ALLOWED_TS = 0.0
_METADATA_CACHE_LOCK = threading.Lock()
_METADATA_CACHE = {}
_METADATA_CACHE_DIRTY = False
_METADATA_CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".metadata_cache.json")


def get_http_session():
    session = getattr(_THREAD_LOCAL, "http_session", None)
    if session is None:
        session = requests.Session()
        session.mount("http://", HTTPAdapter(pool_connections=32, pool_maxsize=32))
        session.mount("https://", HTTPAdapter(pool_connections=32, pool_maxsize=32))
        _THREAD_LOCAL.http_session = session
    return session


class PublicationTimeout(BaseException):
    pass


def _publication_timeout_handler(signum, frame):
    raise PublicationTimeout()


def run_with_publication_timeout(func, timeout_seconds, *args, **kwargs):
    if not hasattr(signal, "SIGALRM"):
        return func(*args, **kwargs)
    if threading.current_thread() is not threading.main_thread():
        return func(*args, **kwargs)

    previous_handler = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, _publication_timeout_handler)
    signal.setitimer(signal.ITIMER_REAL, timeout_seconds)
    try:
        return func(*args, **kwargs)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)


def get_url_text(url):
    return get_url_text_with_options(url, REQUEST_TIMEOUT, REQUEST_RETRIES, RETRY_SLEEP_SECONDS)


def is_dblp_url(url):
    try:
        hostname = (urlparse(str(url or "")).hostname or "").lower()
        return hostname.endswith("dblp.org") or hostname.endswith("dblp.uni-trier.de") or hostname.endswith("dblp.dagstuhl.de")
    except Exception:
        return False


def wait_for_dblp_slot():
    global _DBLP_NEXT_ALLOWED_TS
    interval = max(0.0, float(DBLP_REQUEST_INTERVAL_SECONDS or 0.0))
    if interval <= 0:
        return
    while True:
        with _DBLP_RATE_LIMIT_LOCK:
            now = time.time()
            if now >= _DBLP_NEXT_ALLOWED_TS:
                _DBLP_NEXT_ALLOWED_TS = now + interval
                return
            sleep_seconds = _DBLP_NEXT_ALLOWED_TS - now
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)


def parse_retry_after_seconds(header_value):
    text = str(header_value or "").strip()
    if not text:
        return 0.0
    if re.fullmatch(r"\d+", text):
        try:
            return max(0.0, float(text))
        except Exception:
            return 0.0
    return 0.0


def split_bibtex_entries(text):
    entries = []
    raw = str(text or "")
    n = len(raw)
    i = 0
    while i < n:
        at = raw.find("@", i)
        if at < 0:
            break
        brace = raw.find("{", at)
        if brace < 0:
            break
        depth = 0
        j = brace
        while j < n:
            ch = raw[j]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    entries.append(raw[at:j + 1].strip())
                    i = j + 1
                    break
            j += 1
        else:
            break
    return entries


def load_metadata_cache(cache_path):
    global _METADATA_CACHE, _METADATA_CACHE_DIRTY
    if not ENABLE_METADATA_CACHE:
        _METADATA_CACHE = {}
        _METADATA_CACHE_DIRTY = False
        return
    try:
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as cache_file:
                data = json.load(cache_file)
            if isinstance(data, dict):
                _METADATA_CACHE = data
            else:
                _METADATA_CACHE = {}
        else:
            _METADATA_CACHE = {}
    except Exception:
        _METADATA_CACHE = {}
    _METADATA_CACHE_DIRTY = False


def save_metadata_cache(cache_path):
    global _METADATA_CACHE_DIRTY
    if not ENABLE_METADATA_CACHE:
        return
    with _METADATA_CACHE_LOCK:
        if not _METADATA_CACHE_DIRTY:
            return
        snapshot = dict(_METADATA_CACHE)
        _METADATA_CACHE_DIRTY = False
    try:
        with open(cache_path, "w", encoding="utf-8") as cache_file:
            json.dump(snapshot, cache_file, ensure_ascii=False, indent=2)
    except Exception:
        pass


def metadata_cache_key(paper_url):
    text = str(paper_url or "").strip()
    if not text:
        return ""
    doi = extract_doi_from_url(text)
    if doi:
        return f"doi:{doi.lower()}"
    return f"url:{text}"


def get_cached_metadata(paper_url):
    if not ENABLE_METADATA_CACHE:
        return None
    key = metadata_cache_key(paper_url)
    if not key:
        return None
    with _METADATA_CACHE_LOCK:
        cached = _METADATA_CACHE.get(key)
    if not isinstance(cached, dict):
        return None
    return {
        "abstract": str(cached.get("abstract", "") or ""),
        "date": str(cached.get("date", "") or ""),
        "tags": cached.get("tags", []) if isinstance(cached.get("tags", []), list) else [],
    }


def put_cached_metadata(paper_url, metadata):
    global _METADATA_CACHE_DIRTY
    if not ENABLE_METADATA_CACHE:
        return
    key = metadata_cache_key(paper_url)
    if not key:
        return
    payload = {
        "abstract": str((metadata or {}).get("abstract", "") or ""),
        "date": str((metadata or {}).get("date", "") or ""),
        "tags": (metadata or {}).get("tags", []) if isinstance((metadata or {}).get("tags", []), list) else [],
    }
    with _METADATA_CACHE_LOCK:
        previous = _METADATA_CACHE.get(key)
        if previous != payload:
            _METADATA_CACHE[key] = payload
            _METADATA_CACHE_DIRTY = True


def build_author_bib_url(author_pid_html_url):
    text = str(author_pid_html_url or "").strip()
    if not text:
        return ""
    if text.endswith(".html"):
        return text[:-5] + ".bib"
    if text.endswith("/"):
        return text[:-1] + ".bib"
    return text + ".bib"


def build_bibtex_map_for_author(author_pid_html_url):
    bib_url = build_author_bib_url(author_pid_html_url)
    if not bib_url:
        return {}
    bib_text = get_url_text_with_options(bib_url, timeout_seconds=REQUEST_TIMEOUT, retries=max(1, REQUEST_RETRIES), retry_sleep_seconds=RETRY_SLEEP_SECONDS)
    if not bib_text:
        return {}
    result = {}
    for entry in split_bibtex_entries(bib_text):
        title_match = re.search(r"\btitle\s*=\s*\{([\s\S]+?)\}\s*(?:,\s*\n|,\s*$)", entry, re.IGNORECASE)
        if not title_match:
            continue
        title = re.sub(r"\s+", " ", title_match.group(1).replace("{", "").replace("}", "")).strip()
        if not title:
            continue
        key = normalize_title_for_key(title)
        if key and key not in result:
            result[key] = entry
    return result


def get_url_text_with_options(url, timeout_seconds, retries, retry_sleep_seconds):
    last_exception = None
    last_status_code = 0
    dblp_target = is_dblp_url(url)
    for attempt in range(max(1, int(retries or 1))):
        try:
            if dblp_target:
                wait_for_dblp_slot()
            response = get_http_session().get(url, timeout=timeout_seconds, headers=REQUEST_HEADERS)
            last_status_code = int(response.status_code or 0)
            if response.status_code == 200:
                return response.text
            if response.status_code == 429:
                retry_after_seconds = parse_retry_after_seconds(response.headers.get("Retry-After", ""))
                sleep_seconds = max(float(retry_sleep_seconds or 0.0), retry_after_seconds)
                if sleep_seconds > 0:
                    time.sleep(sleep_seconds)
                continue
        except Exception as exc:
            last_exception = exc
        if attempt < max(1, int(retries or 1)) - 1:
            time.sleep(retry_sleep_seconds)
    if last_exception or last_status_code:
        return ""
    return ""

def normalize_date(date_str):
    if not date_str:
        return ""
    date_str = date_str.strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    year_match = re.search(r"(19|20)\d{2}", date_str)
    if year_match:
        return f"{year_match.group(0)}-01-01"
    return ""


def parse_human_readable_date(date_str):
    if not date_str:
        return ""
    cleaned = re.sub(r"\s+", " ", date_str).strip()
    for fmt in ("%d %b %Y", "%d %B %Y"):
        try:
            return datetime.strptime(cleaned, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return ""


def extract_arxiv_submitted_date(text):
    if not text:
        return ""

    patterns = [
        r"\[\s*Submitted on\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})\s*\]",
        r"Submitted on\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
        r"\[\s*v\d+\s*\]\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            continue
        parsed = parse_human_readable_date(match.group(1))
        if parsed:
            return parsed
    return ""


def is_coarse_date(date_str):
    if not date_str:
        return True
    raw = str(date_str).strip()
    if re.fullmatch(r"\d{4}", raw):
        return True
    normalized = normalize_date(raw)
    if not normalized:
        return True
    return bool(re.fullmatch(r"\d{4}-01-01", normalized))


def parse_include_arxiv_input(raw_value):
    value = (raw_value or "").strip().lower()
    if not value:
        return False

    true_values = {
        "y", "yes", "1", "true", "t",
        "是", "要", "需要", "包含", "包括", "包含arxiv", "要arxiv",
    }
    false_values = {
        "n", "no", "0", "false", "f",
        "否", "不要", "不", "不需要", "不包含", "不包括", "不要arxiv",
    }

    if value in true_values:
        return True
    if value in false_values:
        return False
    return False


def parse_start_year(raw_value):
    text = str(raw_value or "").strip()
    if not text:
        return ""
    if re.fullmatch(r"\d{4}", text):
        return text
    return ""


def is_on_or_after_start_year(date_str, start_year):
    if not start_year:
        return True

    normalized_publication_date = normalize_date(date_str)
    if not normalized_publication_date:
        return False
    publication_year = normalized_publication_date[:4]
    return publication_year >= start_year


def extract_year_from_entry(entry):
    date_tag = entry.find("span", itemprop="datePublished")
    if date_tag and date_tag.get_text(strip=True):
        normalized = normalize_date(date_tag.get_text(strip=True))
        if normalized:
            return normalized

    year_tag = entry.find("span", class_=re.compile(r"year", re.IGNORECASE))
    if year_tag and year_tag.get_text(strip=True):
        normalized = normalize_date(year_tag.get_text(strip=True))
        if normalized:
            return normalized

    entry_text = entry.get_text(" ", strip=True)
    year_match = re.search(r"\b(19|20)\d{2}\b", entry_text)
    if year_match:
        return f"{year_match.group(0)}-01-01"

    return ""


def extract_bibtex_from_view(
    bibtex_view_url,
    fast_mode=False,
    timeout_seconds=None,
    retries=None,
    retry_sleep_seconds=None,
):
    if not bibtex_view_url:
        return ""
    try:
        request_timeout = timeout_seconds
        request_retries = retries
        request_retry_sleep = retry_sleep_seconds
        if request_timeout is None:
            request_timeout = 6 if fast_mode else REQUEST_TIMEOUT
        if request_retries is None:
            request_retries = 1 if fast_mode else REQUEST_RETRIES
        if request_retry_sleep is None:
            request_retry_sleep = 0 if fast_mode else RETRY_SLEEP_SECONDS

        # DBLP view pages often expose a direct .bib endpoint that is more reliable
        # than parsing the HTML page under concurrent requests.
        direct_bib_urls = []
        view_base = re.sub(r"\?.*$", "", str(bibtex_view_url or "").strip())
        if "dblp.org/rec/" in view_base:
            if view_base.endswith(".html"):
                rec_base = view_base[:-5]
            else:
                rec_base = view_base
            if rec_base:
                direct_bib_urls.append(f"{rec_base}.bib")
                direct_bib_urls.append(f"{rec_base}.bib?param=1")

        for direct_bib_url in direct_bib_urls:
            bib_text = get_url_text_with_options(
                direct_bib_url,
                timeout_seconds=request_timeout,
                retries=request_retries,
                retry_sleep_seconds=request_retry_sleep,
            )
            if bib_text:
                bib_text = bib_text.strip()
                if bib_text.startswith("@"):
                    return bib_text

        if fast_mode:
            bibtex_view_text = get_url_text_with_options(
                bibtex_view_url,
                timeout_seconds=request_timeout,
                retries=request_retries,
                retry_sleep_seconds=request_retry_sleep,
            )
        else:
            bibtex_view_text = get_url_text_with_options(
                bibtex_view_url,
                timeout_seconds=request_timeout,
                retries=request_retries,
                retry_sleep_seconds=request_retry_sleep,
            )
        if not bibtex_view_text:
            return ""
        bibtex_text_match = re.search(r"@\w+\{[\s\S]+?\n\}", bibtex_view_text)
        if bibtex_text_match:
            return bibtex_text_match.group(0).strip()
        bibtex_view_soup = BeautifulSoup(bibtex_view_text, "html.parser")
        pre_tag = bibtex_view_soup.find("pre")
        if pre_tag and pre_tag.text.strip():
            return pre_tag.text.strip()

        bibtex_div = bibtex_view_soup.find("div", class_=re.compile(r"bibtex", re.IGNORECASE))
        if bibtex_div and bibtex_div.text.strip():
            return bibtex_div.text.strip()

        bib_url = ""
        direct_bib_link = bibtex_view_soup.find("link", attrs={"type": "application/x-bibtex"})
        if direct_bib_link and direct_bib_link.get("href"):
            bib_url = urljoin(bibtex_view_url, direct_bib_link["href"])

        biburl_match = re.search(r"biburl\s*=\s*\{(https?://[^}]+\.bib)\}", bibtex_view_soup.get_text("\n"))
        if not bib_url and biburl_match:
            bib_url = biburl_match.group(1)
        else:
            bib_link = bibtex_view_soup.find("a", href=re.compile(r"\.bib(\?|$)"))
            if bib_link and bib_link.get("href"):
                bib_url = urljoin(bibtex_view_url, bib_link["href"])

        if not bib_url:
            return ""

        bib_text = get_url_text_with_options(
            bib_url,
            timeout_seconds=request_timeout,
            retries=request_retries,
            retry_sleep_seconds=request_retry_sleep,
        )
        if not bib_text:
            return ""
        return bib_text.strip()
    except Exception:
        return ""


def build_direct_bib_url_from_view_url(bibtex_view_url):
    text = str(bibtex_view_url or "").strip()
    if not text:
        return ""

    if text.endswith(".bib"):
        return text

    parsed = text
    if "?" in parsed:
        parsed = parsed.split("?", 1)[0]

    if parsed.endswith(".html"):
        parsed = parsed[:-5]

    if not parsed or "/rec/" not in parsed:
        return ""

    return f"{parsed}.bib"


def extract_bibtex_from_direct_bib_url(bibtex_url, timeout_seconds, retries, retry_sleep_seconds):
    if not bibtex_url:
        return ""
    text = get_url_text_with_options(
        bibtex_url,
        timeout_seconds=timeout_seconds,
        retries=retries,
        retry_sleep_seconds=retry_sleep_seconds,
    )
    if not text:
        return ""
    if re.search(r"@\w+\{", text):
        return text.strip()
    return ""


def extract_bibtex_with_fallback(bibtex_view_url, prefer_fast=False):
    if not bibtex_view_url:
        return ""

    direct_bib_url = build_direct_bib_url_from_view_url(bibtex_view_url)
    if direct_bib_url:
        bibtex = extract_bibtex_from_direct_bib_url(
            direct_bib_url,
            timeout_seconds=8 if prefer_fast else REQUEST_TIMEOUT,
            retries=2 if prefer_fast else REQUEST_RETRIES,
            retry_sleep_seconds=0.5 if prefer_fast else RETRY_SLEEP_SECONDS,
        )
        if bibtex:
            return bibtex

    bibtex = extract_bibtex_from_view(bibtex_view_url, fast_mode=prefer_fast)
    if bibtex:
        return bibtex

    if prefer_fast:
        bibtex = extract_bibtex_from_view(bibtex_view_url, fast_mode=False)
        if bibtex:
            return bibtex

    # Final resilient retry for transient failures under concurrent fetching.
    return extract_bibtex_from_view(
        bibtex_view_url,
        fast_mode=False,
        timeout_seconds=max(REQUEST_TIMEOUT, 15),
        retries=max(REQUEST_RETRIES, 4),
        retry_sleep_seconds=max(RETRY_SLEEP_SECONDS, 1.0),
    )


def recover_missing_bibtex_fields(publications):
    candidates = []
    for publication in publications:
        if publication.get("skip"):
            continue
        if publication.get("bibtex"):
            continue
        if publication.get("bibtexViewUrl"):
            candidates.append(publication)

    if not candidates:
        return 0

    def _recover_single(publication):
        bibtex_view_url = publication.get("bibtexViewUrl", "")
        if not bibtex_view_url:
            return ""

        # Fast path for concurrent mode: direct .bib endpoint is usually the
        # most stable and significantly faster than parsing HTML pages.
        direct_bib_url = build_direct_bib_url_from_view_url(bibtex_view_url)
        if direct_bib_url:
            bibtex = extract_bibtex_from_direct_bib_url(
                direct_bib_url,
                timeout_seconds=8,
                retries=2,
                retry_sleep_seconds=0.5,
            )
            if bibtex:
                return bibtex

        bibtex = extract_bibtex_from_view(
            bibtex_view_url,
            fast_mode=False,
            timeout_seconds=8,
            retries=2,
            retry_sleep_seconds=0.5,
        )
        if bibtex:
            return bibtex

        return ""

    recovered = 0
    workers = max(1, min(int(MAX_WORKERS or 1), 8))
    if workers > 1 and len(candidates) > 1:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_publication = {
                executor.submit(_recover_single, publication): publication
                for publication in candidates
            }
            for future in as_completed(future_to_publication):
                publication = future_to_publication[future]
                try:
                    bibtex = future.result()
                except Exception:
                    bibtex = ""
                if not bibtex:
                    continue

                publication["bibtex"] = bibtex
                recovered += 1

                if not publication.get("date"):
                    year_text = extract_year_from_bibtex(bibtex)
                    if year_text:
                        publication["date"] = year_text

                venue, venue_short = extract_venue_from_bibtex(bibtex)
                if venue and not publication.get("venue"):
                    publication["venue"] = venue
                if venue_short and not publication.get("venueShort"):
                    publication["venueShort"] = venue_short

                if not publication.get("paperUrl"):
                    bibtex_url = extract_url_from_bibtex(bibtex)
                    if bibtex_url:
                        publication["paperUrl"] = bibtex_url
                        if is_arxiv_like_url(bibtex_url) and not publication.get("arxivUrl"):
                            publication["arxivUrl"] = bibtex_url
    else:
        for publication in candidates:
            bibtex = _recover_single(publication)
            if not bibtex:
                continue

            publication["bibtex"] = bibtex
            recovered += 1

            if not publication.get("date"):
                year_text = extract_year_from_bibtex(bibtex)
                if year_text:
                    publication["date"] = year_text

            venue, venue_short = extract_venue_from_bibtex(bibtex)
            if venue and not publication.get("venue"):
                publication["venue"] = venue
            if venue_short and not publication.get("venueShort"):
                publication["venueShort"] = venue_short

            if not publication.get("paperUrl"):
                bibtex_url = extract_url_from_bibtex(bibtex)
                if bibtex_url:
                    publication["paperUrl"] = bibtex_url
                    if is_arxiv_like_url(bibtex_url) and not publication.get("arxivUrl"):
                        publication["arxivUrl"] = bibtex_url

    return recovered


def extract_year_from_bibtex(bibtex_text):
    if not bibtex_text:
        return ""
    year_match = re.search(r"year\s*=\s*\{(\d{4})\}", bibtex_text, re.IGNORECASE)
    if year_match:
        return year_match.group(1)
    return ""


def extract_venue_from_bibtex(bibtex_text):
    venue = ""
    venue_short = ""
    if not bibtex_text:
        return venue, venue_short

    journal_match = re.search(r"journal\s*=\s*\{([^}]+)\}", bibtex_text, re.IGNORECASE)
    if journal_match:
        venue_short = journal_match.group(1).replace("{", "").replace("}", "").strip()
        return venue, venue_short

    booktitle_match = re.search(r"booktitle\s*=\s*\{([\s\S]+?)\}\s*,", bibtex_text, re.IGNORECASE)
    if booktitle_match:
        raw_booktitle = re.sub(r"\s+", " ", booktitle_match.group(1)).strip()
        short_match = re.search(r"\{\s*([A-Za-z][A-Za-z0-9/\-&]+)\s*\}\s*(?:'\d{2}|\d{4})", raw_booktitle)
        if short_match:
            venue_short = short_match.group(1).strip()
        elif "{" in raw_booktitle and "}" in raw_booktitle:
            brace_match = re.search(r"\{\s*([^}]+)\s*\}", raw_booktitle)
            if brace_match:
                venue_short = brace_match.group(1).strip()
        cleaned_booktitle = raw_booktitle.replace("{", "").replace("}", "")
        venue = cleaned_booktitle.split(",")[0].strip()
        venue = re.sub(r"^Proceedings of\s+", "", venue, flags=re.IGNORECASE).strip()
        if venue_short:
            venue_short = venue_short.replace("{", "").replace("}", "").strip()

    return venue, venue_short


def extract_url_from_bibtex(bibtex_text):
    if not bibtex_text:
        return ""
    url_match = re.search(r"url\s*=\s*\{([^}]+)\}", bibtex_text, re.IGNORECASE)
    if url_match:
        return url_match.group(1).strip()
    return ""


def extract_doi_from_url(url):
    if not url:
        return ""
    doi_match = re.search(r"doi\.org/(10\.[^\s?#]+/[^\s?#]+)", url, re.IGNORECASE)
    if not doi_match:
        doi_match = re.search(r"/doi/(10\.[^\s?#]+/[^\s?#]+)", url, re.IGNORECASE)
    if not doi_match:
        doi_match = re.search(r"\b(10\.[0-9]{4,9}/[^\s?#]+)\b", url, re.IGNORECASE)
    if doi_match:
        return doi_match.group(1).strip()
    return ""


def parse_crossref_date(message):
    if not isinstance(message, dict):
        return ""

    for key in ("published-print", "published-online", "issued", "created"):
        date_obj = message.get(key, {}) if isinstance(message.get(key), dict) else {}
        date_parts = date_obj.get("date-parts", []) if isinstance(date_obj, dict) else []
        if not date_parts or not isinstance(date_parts, list):
            continue
        first = date_parts[0] if date_parts and isinstance(date_parts[0], list) else []
        if not first:
            continue
        try:
            year = int(first[0]) if len(first) >= 1 else 0
            month = int(first[1]) if len(first) >= 2 else 1
            day = int(first[2]) if len(first) >= 3 else 1
            if year > 0:
                return f"{year:04d}-{month:02d}-{day:02d}"
        except Exception:
            continue
    return ""


def fetch_metadata_from_crossref(paper_url):
    metadata = {"abstract": "", "date": "", "tags": []}
    doi = extract_doi_from_url(paper_url)
    if not doi:
        return metadata

    crossref_url = f"https://api.crossref.org/works/{doi}"
    try:
        response = get_http_session().get(crossref_url, timeout=METADATA_REQUEST_TIMEOUT, headers=REQUEST_HEADERS)
        if response.status_code != 200:
            return metadata

        data = response.json()
        message = data.get("message", {}) if isinstance(data, dict) else {}
        if not isinstance(message, dict):
            return metadata

        abstract = str(message.get("abstract", "") or "").strip()
        if abstract:
            abstract = re.sub(r"<[^>]+>", " ", abstract)
            abstract = re.sub(r"\s+", " ", abstract).strip()
            metadata["abstract"] = abstract

        metadata["date"] = parse_crossref_date(message)

        return metadata
    except Exception:
        return metadata


def reconstruct_abstract_from_inverted_index(inverted_index):
    if not isinstance(inverted_index, dict):
        return ""
    positioned_words = []
    for word, positions in inverted_index.items():
        if not isinstance(positions, list):
            continue
        for pos in positions:
            try:
                positioned_words.append((int(pos), str(word)))
            except Exception:
                continue
    if not positioned_words:
        return ""
    positioned_words.sort(key=lambda item: item[0])
    return re.sub(r"\s+", " ", " ".join(word for _, word in positioned_words)).strip()


def fetch_metadata_from_openalex(paper_url):
    metadata = {"abstract": "", "date": "", "tags": []}
    doi = extract_doi_from_url(paper_url)
    if not doi:
        return metadata

    openalex_url = f"https://api.openalex.org/works/https://doi.org/{doi}"
    last_error = None
    for attempt in range(METADATA_REQUEST_RETRIES):
        try:
            response = get_http_session().get(openalex_url, timeout=METADATA_REQUEST_TIMEOUT, headers=REQUEST_HEADERS)
            if response.status_code != 200:
                if attempt < METADATA_REQUEST_RETRIES - 1 and response.status_code >= 500:
                    time.sleep(METADATA_RETRY_SLEEP_SECONDS)
                    continue
                return metadata

            data = response.json() if response.text else {}
            if not isinstance(data, dict):
                return metadata

            abstract = reconstruct_abstract_from_inverted_index(data.get("abstract_inverted_index", {}))
            metadata["abstract"] = abstract

            publication_date = str(data.get("publication_date", "") or "").strip()
            metadata["date"] = normalize_date(publication_date)

            return metadata
        except Exception as exc:
            last_error = exc
            if attempt < METADATA_REQUEST_RETRIES - 1:
                time.sleep(METADATA_RETRY_SLEEP_SECONDS)
    if last_error:
        print(f"OpenAlex metadata fetch failed for DOI {doi}: {last_error}")
    return metadata


def is_challenge_page(page_text, page_soup):
    title_text = ""
    if page_soup and page_soup.title and page_soup.title.string:
        title_text = page_soup.title.string.strip().lower()
    text = (page_text or "").lower()
    checks = ["just a moment", "cloudflare", "captcha", "access denied", "checking your browser"]
    if any(marker in title_text for marker in checks):
        return True
    return any(marker in text for marker in checks)


def fetch_abstract_from_crossref(paper_url):
    return fetch_metadata_from_crossref(paper_url).get("abstract", "")


def extract_arxiv_abs_url(publication):
    arxiv_url = publication.get("arxivUrl", "")
    if arxiv_url and "arxiv.org/abs/" in arxiv_url:
        return arxiv_url

    paper_url = publication.get("paperUrl", "")
    if paper_url and "arxiv.org/abs/" in paper_url:
        return paper_url

    if paper_url:
        match = re.search(r"10\.48550/arXiv\.(\d{4}\.\d{4,5}(?:v\d+)?)", paper_url, re.IGNORECASE)
        if match:
            return f"https://arxiv.org/abs/{match.group(1)}"

    bibtex = publication.get("bibtex", "")
    if bibtex:
        eprint_match = re.search(r"eprint\s*=\s*\{(\d{4}\.\d{4,5}(?:v\d+)?)\}", bibtex, re.IGNORECASE)
        if eprint_match:
            return f"https://arxiv.org/abs/{eprint_match.group(1)}"

    return ""


def is_arxiv_like_url(url):
    text = str(url or "").strip().lower()
    if not text:
        return False
    if "arxiv.org/abs/" in text or "arxiv.org/pdf/" in text:
        return True
    if "doi.org/10.48550/arxiv." in text:
        return True
    if "arxiv." in text:
        return True
    return False


def resolve_arxiv_abs_url_from_url(url):
    text = str(url or "").strip()
    if not text:
        return ""

    abs_match = re.search(r"arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", text, re.IGNORECASE)
    if abs_match:
        return f"https://arxiv.org/abs/{abs_match.group(1)}"

    pdf_match = re.search(r"arxiv\.org/pdf/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)(?:\.pdf)?", text, re.IGNORECASE)
    if pdf_match:
        return f"https://arxiv.org/abs/{pdf_match.group(1)}"

    doi_match = re.search(r"10\.48550/arxiv\.([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", text, re.IGNORECASE)
    if doi_match:
        return f"https://arxiv.org/abs/{doi_match.group(1)}"

    generic_match = re.search(r"arxiv\.([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", text, re.IGNORECASE)
    if generic_match:
        return f"https://arxiv.org/abs/{generic_match.group(1)}"

    return ""


def fetch_metadata_from_arxiv_url(paper_url):
    metadata = {"abstract": "", "date": "", "tags": []}
    arxiv_abs_url = resolve_arxiv_abs_url_from_url(paper_url)
    if not arxiv_abs_url:
        return metadata

    try:
        response = get_http_session().get(arxiv_abs_url, timeout=8, headers=REQUEST_HEADERS)
        if response.status_code != 200:
            return metadata

        page_text = response.text
        page_soup = BeautifulSoup(page_text, "html.parser")

        abstract_text = ""
        abstract_block = page_soup.find("blockquote", class_=re.compile(r"abstract", re.IGNORECASE))
        if abstract_block:
            abstract_text = abstract_block.get_text(" ", strip=True)
        if not abstract_text:
            meta_description = page_soup.find("meta", attrs={"name": "description"})
            if meta_description and meta_description.get("content"):
                abstract_text = meta_description["content"].strip()
        if abstract_text:
            abstract_text = re.sub(r"^\s*Abstract\s*:\s*", "", abstract_text, flags=re.IGNORECASE).strip()
            metadata["abstract"] = abstract_text

        submitted_date = extract_arxiv_submitted_date(page_text)
        if not submitted_date:
            submitted_match = re.search(r"Submitted on (\d{1,2} \w+ \d{4})", page_text, re.IGNORECASE)
            if submitted_match:
                submitted_date = parse_human_readable_date(submitted_match.group(1))
        metadata["date"] = submitted_date
        metadata["tags"] = []
    except Exception:
        return metadata

    return metadata


def recover_arxiv_metadata_quick(publication):
    arxiv_abs_url = extract_arxiv_abs_url(publication)
    if not arxiv_abs_url:
        return publication

    try:
        response = get_http_session().get(arxiv_abs_url, timeout=8, headers=REQUEST_HEADERS)
        if response.status_code != 200:
            return publication

        page_text = response.text
        page_soup = BeautifulSoup(page_text, "html.parser")

        if not publication.get("arxivUrl"):
            publication["arxivUrl"] = arxiv_abs_url

        if not publication.get("paperUrl") and publication.get("arxivUrl"):
            publication["paperUrl"] = publication["arxivUrl"]

        if not publication.get("abstract"):
            abstract_text = ""
            abstract_block = page_soup.find("blockquote", class_=re.compile(r"abstract", re.IGNORECASE))
            if abstract_block:
                abstract_text = abstract_block.get_text(" ", strip=True)
            if not abstract_text:
                meta_description = page_soup.find("meta", attrs={"name": "description"})
                if meta_description and meta_description.get("content"):
                    abstract_text = meta_description["content"].strip()
            if abstract_text:
                abstract_text = re.sub(r"^\s*Abstract\s*:\s*", "", abstract_text, flags=re.IGNORECASE).strip()
                publication["abstract"] = abstract_text

        if is_coarse_date(publication.get("date", "")):
            submitted_date = extract_arxiv_submitted_date(page_text)
            if submitted_date:
                publication["date"] = submitted_date

        publication["tags"] = []
    except Exception:
        return publication

    return publication


def extract_venue_from_dblp_issue_url(issue_url):
    if not issue_url:
        return ""
    page_text = get_url_text(issue_url)
    if not page_text:
        return ""
    soup = BeautifulSoup(page_text, "html.parser")
    candidate = ""
    header = soup.find("h1")
    if header and header.get_text(strip=True):
        candidate = header.get_text(" ", strip=True)
    if not candidate and soup.title and soup.title.string:
        candidate = soup.title.string.strip()
    if not candidate:
        return ""
    candidate = re.sub(r"^dblp:\s*", "", candidate, flags=re.IGNORECASE)
    candidate = re.sub(r"\s+-\s+dblp.*$", "", candidate, flags=re.IGNORECASE)
    candidate = re.sub(r"\s*\(\s*\d+\s*\)\s*", " ", candidate)
    candidate = re.sub(r",?\s*(Volume|Vol\.|vol\.|Issue|No\.)\b.*$", "", candidate).strip()
    candidate = re.sub(r"\s+\d{4}\s*$", "", candidate).strip()
    return candidate


def fetch_metadata_from_paper_url(paper_url):
    metadata = {"abstract": "", "date": "", "tags": []}
    if not paper_url:
        return metadata

    cached = get_cached_metadata(paper_url)
    if cached is not None:
        return cached

    if is_arxiv_like_url(paper_url):
        metadata = fetch_metadata_from_arxiv_url(paper_url)
        put_cached_metadata(paper_url, metadata)
        return metadata
    try:
        paper_text = get_url_text_with_options(
            paper_url,
            timeout_seconds=METADATA_REQUEST_TIMEOUT,
            retries=METADATA_REQUEST_RETRIES,
            retry_sleep_seconds=METADATA_RETRY_SLEEP_SECONDS,
        )
        if not paper_text:
            crossref_metadata = fetch_metadata_from_crossref(paper_url)
            if not metadata.get("abstract"):
                metadata["abstract"] = crossref_metadata.get("abstract", "")
            if not metadata.get("date"):
                metadata["date"] = crossref_metadata.get("date", "")

            if not metadata.get("abstract"):
                openalex_metadata = fetch_metadata_from_openalex(paper_url)
                if not metadata.get("abstract"):
                    metadata["abstract"] = openalex_metadata.get("abstract", "")
                if not metadata.get("date"):
                    metadata["date"] = openalex_metadata.get("date", "")

            metadata["tags"] = []
            put_cached_metadata(paper_url, metadata)
            return metadata
        paper_soup = BeautifulSoup(paper_text, "html.parser")

        if is_challenge_page(paper_text, paper_soup):
            metadata = fetch_metadata_from_crossref(paper_url)
            if not metadata.get("abstract"):
                openalex_metadata = fetch_metadata_from_openalex(paper_url)
                if not metadata.get("abstract"):
                    metadata["abstract"] = openalex_metadata.get("abstract", "")
                if not metadata.get("date"):
                    metadata["date"] = openalex_metadata.get("date", "")
            metadata["tags"] = []
            put_cached_metadata(paper_url, metadata)
            return metadata

        abstract_text = ""
        if not abstract_text:
            for script_tag in paper_soup.find_all("script", attrs={"type": "application/ld+json"}):
                try:
                    json_text = script_tag.string or script_tag.get_text() or ""
                    if not json_text.strip():
                        continue
                    data = json.loads(json_text)
                    if isinstance(data, list):
                        candidates = data
                    else:
                        candidates = [data]
                    for item in candidates:
                        if isinstance(item, dict) and item.get("@type") in ("ScholarlyArticle", "Article"):
                            description = item.get("description")
                            if description:
                                abstract_text = re.sub(r"\s+", " ", description).strip()
                                break
                    if abstract_text:
                        break
                except Exception:
                    continue
        if not abstract_text:
            abstract_tag = paper_soup.find("blockquote", class_="abstract")
            if abstract_tag:
                abstract_text = abstract_tag.text.strip().replace("Abstract:", "").strip()
        if not abstract_text:
            acm_abstract = paper_soup.select_one("div.abstractSection")
            if acm_abstract:
                abstract_text = acm_abstract.get_text(" ", strip=True)
        if not abstract_text:
            acm_abstract = paper_soup.select_one("div.abstractInFull")
            if acm_abstract:
                abstract_text = acm_abstract.get_text(" ", strip=True)
        if not abstract_text:
            acm_abstract = paper_soup.select_one("section#abstract, div#abstract, div.article__abstract, div.abstract")
            if acm_abstract:
                abstract_text = acm_abstract.get_text(" ", strip=True)
        if not abstract_text:
            meta_abstract = paper_soup.find("meta", attrs={"name": "citation_abstract"})
            if meta_abstract and meta_abstract.get("content"):
                abstract_text = meta_abstract["content"].strip()
        if not abstract_text:
            meta_abstract = paper_soup.find("meta", attrs={"property": "og:description"})
            if meta_abstract and meta_abstract.get("content"):
                abstract_text = meta_abstract["content"].strip()
        if not abstract_text:
            meta_abstract = paper_soup.find("meta", attrs={"name": "description"})
            if meta_abstract and meta_abstract.get("content"):
                abstract_text = meta_abstract["content"].strip()
        if not abstract_text:
            meta_abstract = paper_soup.find("meta", attrs={"name": "dc.description"})
            if meta_abstract and meta_abstract.get("content"):
                abstract_text = meta_abstract["content"].strip()
        if not abstract_text:
            abstract_header = paper_soup.find(["h1", "h2", "h3"], string=re.compile(r"^\s*Abstract\s*$", re.IGNORECASE))
            if abstract_header:
                next_block = abstract_header.find_next(["div", "p", "section"])
                if next_block:
                    abstract_text = next_block.get_text(" ", strip=True)
        if not abstract_text:
            page_text = paper_soup.get_text("\n")
            abstract_match = re.search(
                r"\bAbstract\b\s*(.+?)(?:\n\s*(?:Author Tags|Index Terms|Keywords|References|Formats available|Published:|Publication History)|\n\s*1\s+Introduction|\n\s*1\.|\n\s*Introduction)",
                page_text,
                re.IGNORECASE | re.DOTALL,
            )
            if abstract_match:
                abstract_text = re.sub(r"\s+", " ", abstract_match.group(1)).strip()
        if abstract_text:
            abstract_text = re.sub(r"^Abstract\s*", "", abstract_text, flags=re.IGNORECASE).strip()
            abstract_text = re.sub(r"\s*AI Summary\s*", " ", abstract_text, flags=re.IGNORECASE).strip()
        if not abstract_text:
            abstract_text = fetch_abstract_from_crossref(paper_url)
        metadata["abstract"] = abstract_text

        date_text = ""
        lower_url = (paper_url or "").lower()
        if "arxiv.org" in lower_url or "10.48550/arxiv." in lower_url:
            date_text = extract_arxiv_submitted_date(paper_text)
        if not date_text:
            submitted_match = re.search(r"Submitted on (\d{1,2} \w+ \d{4})", paper_text, re.IGNORECASE)
            if submitted_match:
                date_text = parse_human_readable_date(submitted_match.group(1))
        metadata["date"] = date_text

        metadata["tags"] = []

        if (not metadata.get("abstract")) or (not metadata.get("date")):
            crossref_metadata = fetch_metadata_from_crossref(paper_url)
            if not metadata.get("abstract"):
                metadata["abstract"] = crossref_metadata.get("abstract", "")
            if not metadata.get("date"):
                metadata["date"] = crossref_metadata.get("date", "")

        if not metadata.get("abstract"):
            openalex_metadata = fetch_metadata_from_openalex(paper_url)
            if not metadata.get("abstract"):
                metadata["abstract"] = openalex_metadata.get("abstract", "")
            if not metadata.get("date"):
                metadata["date"] = openalex_metadata.get("date", "")
        metadata["tags"] = []
        put_cached_metadata(paper_url, metadata)
        return metadata
    except Exception:
        return metadata


def build_bibtex_view_url(href, base_url):
    if not href:
        return ""
    if href.startswith("//"):
        href = f"https:{href}"
    href = urljoin(base_url, href)
    if "dblp.org/rec/" not in href:
        return ""
    if "view=bibtex" in href:
        return href
    if href.endswith(".html"):
        return f"{href}?view=bibtex"
    if href.endswith("/"):
        href = href[:-1]
    if ".html" not in href and "?" not in href:
        return f"{href}.html?view=bibtex"
    if "?" in href:
        return f"{href}&view=bibtex"
    return ""


def enrich_publication(publication, include_arxiv=False, start_date=""):
    paper_url = publication.get("paperUrl", "")
    if paper_url and is_arxiv_like_url(paper_url) and not publication.get("arxivUrl"):
        publication["arxivUrl"] = paper_url

    if not include_arxiv and (
        is_arxiv_like_url(publication.get("paperUrl", ""))
        or is_arxiv_like_url(publication.get("arxivUrl", ""))
    ):
        publication["skip"] = True
        return publication

    bibtex_view_url = publication.get("bibtexViewUrl", "")
    if bibtex_view_url and not publication.get("bibtex"):
        is_arxiv_candidate = (
            is_arxiv_like_url(publication.get("paperUrl", ""))
            or is_arxiv_like_url(publication.get("arxivUrl", ""))
        )
        publication["bibtex"] = extract_bibtex_with_fallback(bibtex_view_url, prefer_fast=is_arxiv_candidate)

    venue, venue_short = extract_venue_from_bibtex(publication.get("bibtex", ""))
    if venue:
        publication["venue"] = venue
    if venue_short:
        publication["venueShort"] = venue_short
    is_arxiv_or_corr_entry = (
        is_arxiv_like_url(publication.get("paperUrl", ""))
        or is_arxiv_like_url(publication.get("arxivUrl", ""))
        or str(publication.get("venueShort", "")).strip().lower() == "corr"
    )
    if not publication.get("venue") and not is_arxiv_or_corr_entry:
        issue_url = publication.get("dblpIssueUrl", "")
        issue_venue = extract_venue_from_dblp_issue_url(issue_url)
        if issue_venue:
            publication["venue"] = issue_venue

    if not paper_url:
        bibtex_url = extract_url_from_bibtex(publication.get("bibtex", ""))
        if bibtex_url:
            publication["paperUrl"] = bibtex_url
            if is_arxiv_like_url(bibtex_url) and not publication.get("arxivUrl"):
                publication["arxivUrl"] = bibtex_url
            paper_url = bibtex_url

    if paper_url and is_arxiv_like_url(paper_url) and not publication.get("arxivUrl"):
        publication["arxivUrl"] = paper_url

    if not include_arxiv and paper_url and is_arxiv_like_url(paper_url):
        publication["skip"] = True
        return publication

    year_text = extract_year_from_bibtex(publication.get("bibtex", ""))
    if year_text:
        publication["date"] = year_text
    if start_date and publication.get("date") and not is_on_or_after_start_year(publication.get("date", ""), start_date):
        publication["skip"] = True
        return publication

    needs_abstract = not publication.get("abstract")
    needs_date = not publication.get("date")
    if paper_url and (needs_abstract or needs_date):
        metadata = fetch_metadata_from_paper_url(paper_url)
        if needs_abstract and metadata.get("abstract"):
            publication["abstract"] = metadata.get("abstract", "")
        if needs_date and metadata.get("date"):
            publication["date"] = metadata.get("date", "")
        publication["tags"] = []

    if not publication.get("date"):
        year_text = extract_year_from_bibtex(publication.get("bibtex", ""))
        if year_text:
            publication["date"] = year_text

    if start_date and not is_on_or_after_start_year(publication.get("date", ""), start_date):
        publication["skip"] = True
    return publication


def scrape_dblp_publications(url, include_arxiv=False, start_date=""):
    """
    Scrape publication information from the given DBLP author page URL.

    Args:
        url (str): The URL of the DBLP author page.

    Returns:
        list: A list of dictionaries containing publication information.
    """
    page_text = get_url_text(url)
    if not page_text:
        raise Exception(f"Failed to fetch URL after retries: {url}")

    soup = BeautifulSoup(page_text, 'html.parser')
    author_bibtex_map = build_bibtex_map_for_author(url)

    # Find all publication entries
    publications = []
    bibtex_view_urls = []
    for entry in soup.find_all('li'):
        entry_text = entry.get_text(" ", strip=True)
        if re.match(r"^\s*\[d[^\]]*\]", entry_text, re.IGNORECASE):
            continue

        title_tag = entry.find('span', class_='title')
        if not title_tag:
            continue  # Skip entries without a title

        title = title_tag.text
        authors = [author.text for author in entry.find_all('span', itemprop='author')]

        paper_url = ""
        arxiv_url = ""
        bibtex_view_url = ""

        additional_links = entry.find_all("a")
        issue_url = ""
        for link in additional_links:
            if "href" not in link.attrs:
                continue
            href = link["href"]
            if not issue_url and "dblp.org/db/" in href and ".html#" in href:
                issue_url = href
            if href.startswith("https://doi.org/") and not paper_url:
                paper_url = href
                if "arXiv." in href:
                    arxiv_id_match = re.search(r"arXiv\.(\d{4}\.\d{5}(v\d+)?)", href)
                    if arxiv_id_match:
                        arxiv_id = arxiv_id_match.group(1)
                        arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"
            if not bibtex_view_url:
                candidate_bibtex_url = build_bibtex_view_url(href, url)
                if candidate_bibtex_url:
                    bibtex_view_url = candidate_bibtex_url

        publication = {
            "title": title,
            "authors": authors,
            "date": extract_year_from_entry(entry),
            "venue": "",
            "venueShort": "",
            "tags": [],
            "awards": [],
            "abstract": "",
            "arxivUrl": arxiv_url,
            "paperUrl": paper_url,
            "bibtex": "",
            "bibtexViewUrl": bibtex_view_url,
            "dblpIssueUrl": issue_url,
        }

        map_key = normalize_title_for_key(title)
        if map_key and map_key in author_bibtex_map:
            publication["bibtex"] = author_bibtex_map[map_key]

        if publication.get("paperUrl") and "arxiv" in publication["paperUrl"].lower() and not publication.get("arxivUrl"):
            publication["arxivUrl"] = publication["paperUrl"]

        if start_date and publication.get("date") and not is_on_or_after_start_year(publication.get("date", ""), start_date):
            continue

        publications.append(publication)
        if bibtex_view_url:
            bibtex_view_urls.append(bibtex_view_url)

    def _enrich_single(pub):
        title = pub.get("title", "")
        try:
            if MAX_WORKERS <= 1:
                run_with_publication_timeout(
                    enrich_publication,
                    PER_PUBLICATION_TIMEOUT_SECONDS,
                    pub,
                    include_arxiv,
                    start_date,
                )
            else:
                enrich_publication(pub, include_arxiv, start_date)
        except PublicationTimeout:
            recover_arxiv_metadata_quick(pub)
        except Exception as exc:
            print(f"Fetch exception: {title} -> {exc}")

    progress_started_at = time.time()
    progress_stop_event = threading.Event()
    progress_lock = threading.Lock()
    total_items = len(publications)
    completed_items = 0
    last_progress_line_len = 0

    def _render_progress_line(completed):
        nonlocal last_progress_line_len
        elapsed = max(0.0, time.time() - progress_started_at)
        safe_total = max(1, total_items)
        ratio = min(1.0, max(0.0, completed / safe_total))
        bar_width = 24
        filled = int(bar_width * ratio)
        bar = "#" * filled + "-" * (bar_width - filled)

        avg_seconds_per_item = (elapsed / completed) if completed > 0 else 6.0
        remaining = max(0, total_items - completed)
        eta_seconds = int(remaining * avg_seconds_per_item)
        elapsed_seconds = int(elapsed)

        line_text = f"Progress [{bar}] {completed}/{total_items} elapsed:{elapsed_seconds}s eta:{eta_seconds}s"
        padding = ""
        if last_progress_line_len > len(line_text):
            padding = " " * (last_progress_line_len - len(line_text))
        last_progress_line_len = len(line_text)

        print(
            f"\r{line_text}{padding}",
            end="",
            flush=True,
        )

    def _progress_loop():
        while not progress_stop_event.is_set():
            with progress_lock:
                snapshot_completed = completed_items
            _render_progress_line(snapshot_completed)
            if progress_stop_event.wait(1.0):
                break
        with progress_lock:
            snapshot_completed = completed_items
        _render_progress_line(snapshot_completed)

    progress_thread = threading.Thread(target=_progress_loop, daemon=True)
    progress_thread.start()

    try:
        workers = max(1, int(MAX_WORKERS or 1))
        if workers > 1:
            with ThreadPoolExecutor(max_workers=workers) as executor:
                future_to_publication = {
                    executor.submit(_enrich_single, publication): publication
                    for publication in publications
                }
                for future in as_completed(future_to_publication):
                    publication = future_to_publication[future]
                    try:
                        future.result()
                    except Exception as exc:
                        print(f"Fetch exception: {publication.get('title', '')} -> {exc}")
                    with progress_lock:
                        completed_items += 1
        else:
            for publication in publications:
                _enrich_single(publication)
                with progress_lock:
                    completed_items += 1

        recover_missing_bibtex_fields(publications)
    finally:
        progress_stop_event.set()
        progress_thread.join(timeout=2)
        print()

    for publication in publications:
        publication.pop("bibtexViewUrl", None)
        publication.pop("dblpIssueUrl", None)

    return publications, bibtex_view_urls

def extract_author_name_from_dblp(url):
    page_text = get_url_text(url)
    if not page_text:
        return ""
    soup = BeautifulSoup(page_text, "html.parser")
    name_tag = soup.select_one("span.name")
    if name_tag and name_tag.get_text(strip=True):
        return name_tag.get_text(strip=True)
    header_name = soup.find("h1")
    if header_name and header_name.get_text(strip=True):
        return header_name.get_text(strip=True)
    return ""

def save_to_js(data, filename):
    """
    Save data to a JS file in the required format.

    Args:
        data (list): The data to save.
        filename (str): The name of the JS file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("module.exports = ")
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_js_array(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    if not content:
        return []

    prefix = "module.exports ="
    if content.startswith(prefix):
        content = content[len(prefix):].strip()

    data = json.loads(content)
    if not isinstance(data, list):
        raise ValueError(f"File content is not an array: {filepath}")
    return data


def merge_unique_list(first_list, second_list):
    merged = []
    seen = set()
    for item in (first_list or []) + (second_list or []):
        if not item:
            continue
        normalized = str(item).strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        merged.append(normalized)
    return merged


def prefer_scalar(existing_value, incoming_value):
    existing_text = (existing_value or "").strip() if isinstance(existing_value, str) else existing_value
    incoming_text = (incoming_value or "").strip() if isinstance(incoming_value, str) else incoming_value
    if not existing_text and incoming_text:
        return incoming_value
    if existing_text and incoming_text and isinstance(existing_text, str) and isinstance(incoming_text, str):
        if len(incoming_text) > len(existing_text):
            return incoming_value
    return existing_value


def merge_publication_items(existing_item, incoming_item):
    existing_item["authors"] = merge_unique_list(existing_item.get("authors", []), incoming_item.get("authors", []))
    existing_item["tags"] = merge_unique_list(existing_item.get("tags", []), incoming_item.get("tags", []))
    existing_item["awards"] = merge_unique_list(existing_item.get("awards", []), incoming_item.get("awards", []))

    for key in ["title", "date", "venue", "venueShort", "abstract", "bibtex", "paperUrl", "arxivUrl"]:
        existing_item[key] = prefer_scalar(existing_item.get(key, ""), incoming_item.get(key, ""))

    paper_url = existing_item.get("paperUrl", "")
    if paper_url and isinstance(paper_url, str) and "arxiv" in paper_url.lower() and not existing_item.get("arxivUrl"):
        existing_item["arxivUrl"] = paper_url


def normalize_title_for_key(title):
    text = (title or "").strip().lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def extract_doi(publication):
    paper_url = str(publication.get("paperUrl", "") or "")
    doi_url_match = re.search(r"doi\.org/(10\.\d{4,9}/[^\s?#]+)", paper_url, re.IGNORECASE)
    if doi_url_match:
        return doi_url_match.group(1).strip().rstrip(".,;").lower()

    bibtex = str(publication.get("bibtex", "") or "")
    doi_bib_match = re.search(r"\bdoi\s*=\s*[\{\"]\s*(10\.\d{4,9}/[^\}\",\n]+)", bibtex, re.IGNORECASE)
    if doi_bib_match:
        return doi_bib_match.group(1).strip().rstrip(".,;").lower()
    return ""


def extract_arxiv_id(publication):
    arxiv_url = str(publication.get("arxivUrl", "") or "")
    arxiv_match = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", arxiv_url, re.IGNORECASE)
    if arxiv_match:
        return arxiv_match.group(1).lower()

    paper_url = str(publication.get("paperUrl", "") or "")
    paper_match = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", paper_url, re.IGNORECASE)
    if paper_match:
        return paper_match.group(1).lower()
    return ""


def publication_dedup_key(publication):
    if not isinstance(publication, dict):
        return "invalid:unknown"

    doi = extract_doi(publication)
    if doi:
        return f"doi:{doi}"

    arxiv_id = extract_arxiv_id(publication)
    if arxiv_id:
        return f"arxiv:{arxiv_id}"

    title_key = normalize_title_for_key(publication.get("title", ""))
    if title_key:
        return f"title:{title_key}"

    raw = json.dumps(publication, ensure_ascii=False, sort_keys=True)
    return f"raw:{raw}"


def merge_into_existing_js_file(existing_js_filepath, new_publications):
    existing_publications = load_js_array(existing_js_filepath)

    merged_by_key = {}
    ordered_keys = []
    for item in existing_publications:
        if not isinstance(item, dict):
            continue
        key = publication_dedup_key(item)
        if key not in merged_by_key:
            merged_by_key[key] = item
            ordered_keys.append(key)
        else:
            merge_publication_items(merged_by_key[key], item)

    deduped_titles = []
    added_titles = []
    for item in new_publications:
        if not isinstance(item, dict):
            continue
        key = publication_dedup_key(item)
        title = (item.get("title", "") or "").strip() or "(untitled)"
        if key in merged_by_key:
            deduped_titles.append(title)
            continue
        else:
            merged_by_key[key] = item
            ordered_keys.append(key)
            added_titles.append(title)

    merged_data = [merged_by_key[key] for key in ordered_keys]
    for item in merged_data:
        if not isinstance(item.get("tags"), list):
            item["tags"] = []
        if not isinstance(item.get("awards"), list):
            item["awards"] = []
    save_to_js(merged_data, existing_js_filepath)

    print(f"Merged into existing JS file: added {len(added_titles)}, deduplicated {len(deduped_titles)}.")
    return merged_data


def format_publications(publications, include_arxiv=False, start_date=""):
    """
    Format the scraped publications to match the required JSON and JS structure.

    Args:
        publications (list): List of scraped publication dictionaries.

    Returns:
        list: Formatted list of publications.
    """
    merged_by_title = {}
    title_order = []
    for pub in publications:
        if pub.get("skip"):
            continue

        normalized_venue = pub.get("venue", "") or ""
        normalized_venue_short = pub.get("venueShort", "") or ""
        if isinstance(normalized_venue, str) and normalized_venue.strip().lower() == "corr":
            normalized_venue = ""
        if isinstance(normalized_venue_short, str) and normalized_venue_short.strip().lower() == "corr":
            normalized_venue_short = ""

        paper_url = pub.get("paperUrl", "")
        if not include_arxiv and paper_url and "arxiv" in paper_url.lower():
            continue
        if not include_arxiv and pub.get("arxivUrl", ""):
            continue
        if not is_on_or_after_start_year(pub.get("date", ""), start_date):
            continue
        item = {
            "title": pub.get("title", ""),
            "date": pub.get("date", ""),
            "authors": pub.get("authors", []),
            "venue": normalized_venue,
            "venueShort": normalized_venue_short,
            "abstract": pub.get("abstract", ""),
            "arxivUrl": pub.get("arxivUrl", ""),
            "paperUrl": pub.get("paperUrl", ""),
            "bibtex": pub.get("bibtex", "")
        }

        title_key = (item.get("title", "") or "").strip().lower()
        if not title_key:
            title_key = f"__untitled__{len(title_order)}"

        if title_key not in merged_by_title:
            merged_by_title[title_key] = item
            title_order.append(title_key)
        else:
            merge_publication_items(merged_by_title[title_key], item)

    return [merged_by_title[key] for key in title_order]

def run_scrape_flow(
    url,
    include_arxiv_input,
    start_date_input,
    existing_js_path="",
    max_workers=None,
    per_item_sleep_seconds=None,
    fast_mode=False,
    dblp_request_interval_seconds=None,
    enable_metadata_cache=True,
):
    global MAX_WORKERS, PER_ITEM_SLEEP_SECONDS, DBLP_REQUEST_INTERVAL_SECONDS, ENABLE_METADATA_CACHE
    global METADATA_REQUEST_TIMEOUT, METADATA_REQUEST_RETRIES, METADATA_RETRY_SLEEP_SECONDS
    if max_workers is not None:
        try:
            MAX_WORKERS = max(1, int(max_workers))
        except Exception:
            MAX_WORKERS = 1
    if per_item_sleep_seconds is not None:
        try:
            PER_ITEM_SLEEP_SECONDS = max(0.0, float(per_item_sleep_seconds))
        except Exception:
            PER_ITEM_SLEEP_SECONDS = 1.0
    if dblp_request_interval_seconds is not None:
        try:
            DBLP_REQUEST_INTERVAL_SECONDS = max(0.0, float(dblp_request_interval_seconds))
        except Exception:
            DBLP_REQUEST_INTERVAL_SECONDS = 4.0
    ENABLE_METADATA_CACHE = bool(enable_metadata_cache)

    if bool(fast_mode):
        METADATA_REQUEST_TIMEOUT = 5
        METADATA_REQUEST_RETRIES = 2
        METADATA_RETRY_SLEEP_SECONDS = 0.5
    else:
        METADATA_REQUEST_TIMEOUT = REQUEST_TIMEOUT
        METADATA_REQUEST_RETRIES = REQUEST_RETRIES
        METADATA_RETRY_SLEEP_SECONDS = RETRY_SLEEP_SECONDS

    url = (url or "").strip() or DEFAULT_DBLP_URL
    if not re.match(r"^https://dblp\.org/pid/[^/]+/[^/]+\.html$", url):
        print("Error: Invalid URL format. Example: https://dblp.org/pid/c/SCCheung.html")
        return 1
    print(f"Scraping publications from {url}...")

    include_arxiv = parse_include_arxiv_input(include_arxiv_input)

    start_date_input = (start_date_input or "").strip()
    start_date = ""
    if start_date_input:
        start_date = parse_start_year(start_date_input)
        if not start_date:
            print("Error: Invalid start year format. Please use YYYY")
            return 1

    author_name = extract_author_name_from_dblp(url)
    if not author_name:
        print("Warning: Could not extract author name from URL. Continue scraping.")
    try:
        load_metadata_cache(_METADATA_CACHE_PATH)
        publications, bibtex_view_urls = scrape_dblp_publications(
            url,
            include_arxiv=include_arxiv,
            start_date=start_date,
        )

        # Format publications to match the required JSON and JS structure
        formatted_publications = format_publications(
            publications,
            include_arxiv=include_arxiv,
            start_date=start_date,
        )

        print(f"Found {len(formatted_publications)} publications:")
        keys_to_check = ["date", "authors", "venue", "venueShort", "abstract", "arxivUrl", "paperUrl", "bibtex"]
        for index, item in enumerate(formatted_publications, 1):
            title = str(item.get("title", "") or "(untitled)").strip()
            found_keys = []
            for key in keys_to_check:
                value = item.get(key)
                if value:
                    found_keys.append(key)
            found_text = ", ".join(found_keys) if found_keys else "none"
            print(f"{index}. {title}")
            print(f"   content: {found_text}")

        js_filepath = (existing_js_path or "").strip()
        if not js_filepath:
            print("Error: existing_js_path is required.")
            return 1
        if not os.path.exists(js_filepath):
            print(f"Error: Selected JS file does not exist: {js_filepath}")
            return 1
        merge_into_existing_js_file(js_filepath, formatted_publications)
        print(f"Publications saved to existing file: {js_filepath}")
        save_metadata_cache(_METADATA_CACHE_PATH)
        return 0

    except Exception as e:
        save_metadata_cache(_METADATA_CACHE_PATH)
        print(f"An error occurred: {e}")
        return 1


def _to_yes_no_text(value):
    if isinstance(value, bool):
        return "y" if value else "n"
    text = str(value or "").strip()
    if not text:
        return "n"
    return text


def load_run_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as config_file:
        config_data = json.load(config_file)
    if not isinstance(config_data, dict):
        raise ValueError(f"Config root must be an object: {config_path}")

    return {
        "url": str(config_data.get("url", DEFAULT_DBLP_URL) or DEFAULT_DBLP_URL).strip(),
        "include_arxiv_input": _to_yes_no_text(config_data.get("include_arxiv", "n")),
        "start_date_input": str(config_data.get("start_date", "") or "").strip(),
        "existing_js_path": str(config_data.get("existing_js_path", "") or "").strip(),
        "max_workers": config_data.get("max_workers", MAX_WORKERS),
        "per_item_sleep_seconds": config_data.get("per_item_sleep_seconds", PER_ITEM_SLEEP_SECONDS),
        "fast_mode": bool(config_data.get("fast_mode", False)),
        "dblp_request_interval_seconds": config_data.get("dblp_request_interval_seconds", DBLP_REQUEST_INTERVAL_SECONDS),
        "enable_metadata_cache": bool(config_data.get("enable_metadata_cache", True)),
    }


def main():
    parser = argparse.ArgumentParser(description="Scrape DBLP publications")
    parser.add_argument("--config", default=DEFAULT_CONFIG_FILENAME, help="Path to run config JSON")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.abspath(__file__))
    config_path = args.config
    if not os.path.isabs(config_path):
        config_path = os.path.join(project_root, config_path)

    try:
        run_config = load_run_config(config_path)
    except Exception as exc:
        print(f"Error loading config: {exc}")
        print("Please create or fix config file, e.g. config.json")
        sys.exit(1)

    print(f"Using config file: {config_path}")

    exit_code = run_scrape_flow(
        run_config["url"],
        run_config["include_arxiv_input"],
        run_config["start_date_input"],
        existing_js_path=run_config["existing_js_path"],
        max_workers=run_config["max_workers"],
        per_item_sleep_seconds=run_config["per_item_sleep_seconds"],
        fast_mode=run_config["fast_mode"],
        dblp_request_interval_seconds=run_config["dblp_request_interval_seconds"],
        enable_metadata_cache=run_config["enable_metadata_cache"],
    )
    if exit_code != 0:
        sys.exit(exit_code)

if __name__ == "__main__":
    main()