import requests
from bs4 import BeautifulSoup
import json
import re
import argparse
from datetime import datetime
from urllib.parse import urljoin, parse_qs, urlparse
import time
import os
import sys
import subprocess
import signal
import threading
import webbrowser
import uuid
from contextlib import redirect_stdout, redirect_stderr
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

REQUEST_TIMEOUT = 10
REQUEST_RETRIES = 6
RETRY_SLEEP_SECONDS = 2.0
PER_ITEM_SLEEP_SECONDS = 1.0
PER_PUBLICATION_TIMEOUT_SECONDS = 20
MAX_WORKERS = 1
DEFAULT_DBLP_URL = "https://dblp.org/pid/c/SCCheung.html"
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PublicationScraper/1.0; +https://dblp.org)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


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
    last_exception = None
    for attempt in range(REQUEST_RETRIES):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT, headers=REQUEST_HEADERS)
            if response.status_code == 200:
                return response.text
        except Exception as exc:
            last_exception = exc
        if attempt < REQUEST_RETRIES - 1:
            time.sleep(RETRY_SLEEP_SECONDS)
    if last_exception:
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


def is_on_or_after_start_date(date_str, start_date_str):
    if not start_date_str:
        return True

    normalized_start_date = normalize_date(start_date_str)
    if not normalized_start_date:
        return True

    normalized_publication_date = normalize_date(date_str)
    if not normalized_publication_date:
        return False

    try:
        publication_dt = datetime.strptime(normalized_publication_date, "%Y-%m-%d")
        start_dt = datetime.strptime(normalized_start_date, "%Y-%m-%d")
    except ValueError:
        return False

    return publication_dt >= start_dt


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


def extract_bibtex_from_view(bibtex_view_url):
    if not bibtex_view_url:
        return ""
    try:
        bibtex_view_text = get_url_text(bibtex_view_url)
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
        biburl_match = re.search(r"biburl\s*=\s*\{(https?://[^}]+\.bib)\}", bibtex_view_soup.get_text("\n"))
        if biburl_match:
            bib_url = biburl_match.group(1)
        else:
            bib_link = bibtex_view_soup.find("a", href=re.compile(r"\.bib(\?|$)"))
            if bib_link and bib_link.get("href"):
                bib_url = urljoin(bibtex_view_url, bib_link["href"])

        if not bib_url:
            return ""

        bib_text = get_url_text(bib_url)
        if not bib_text:
            return ""
        return bib_text.strip()
    except Exception:
        return ""


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
    if doi_match:
        return doi_match.group(1).strip()
    return ""


def fetch_abstract_from_crossref(paper_url):
    doi = extract_doi_from_url(paper_url)
    if not doi:
        return ""
    crossref_url = f"https://api.crossref.org/works/{doi}"
    try:
        response = requests.get(crossref_url, timeout=REQUEST_TIMEOUT, headers=REQUEST_HEADERS)
        if response.status_code != 200:
            return ""
        data = response.json()
        message = data.get("message", {}) if isinstance(data, dict) else {}
        abstract = message.get("abstract", "")
        if not abstract:
            return ""
        abstract = re.sub(r"<[^>]+>", " ", abstract)
        abstract = re.sub(r"\s+", " ", abstract).strip()
        return abstract
    except Exception:
        return ""


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


def recover_arxiv_metadata_quick(publication):
    arxiv_abs_url = extract_arxiv_abs_url(publication)
    if not arxiv_abs_url:
        return publication

    try:
        response = requests.get(arxiv_abs_url, timeout=8, headers=REQUEST_HEADERS)
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

        if not publication.get("tags"):
            subject_meta = page_soup.find("meta", attrs={"name": "citation_keywords"})
            if subject_meta and subject_meta.get("content"):
                publication["tags"] = [x.strip() for x in subject_meta["content"].split(",") if x.strip()]
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
    try:
        paper_text = get_url_text(paper_url)
        if not paper_text:
            return metadata
        paper_soup = BeautifulSoup(paper_text, "html.parser")

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

        tags = []
        keywords_meta = paper_soup.find("meta", attrs={"name": "citation_keywords"})
        if keywords_meta and keywords_meta.get("content"):
            tags = [t.strip() for t in keywords_meta["content"].split(",") if t.strip()]
        if not tags:
            keywords_meta = paper_soup.find("meta", attrs={"name": "keywords"})
            if keywords_meta and keywords_meta.get("content"):
                tags = [t.strip() for t in keywords_meta["content"].split(",") if t.strip()]
        if not tags:
            keywords_container = paper_soup.find("div", class_="keywords")
            if keywords_container:
                tags = [kw.text.strip() for kw in keywords_container.find_all("span") if kw.text.strip()]
        metadata["tags"] = tags

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
    if paper_url and "arxiv" in paper_url.lower() and not publication.get("arxivUrl"):
        publication["arxivUrl"] = paper_url

    bibtex_view_url = publication.get("bibtexViewUrl", "")
    if bibtex_view_url:
        publication["bibtex"] = extract_bibtex_from_view(bibtex_view_url)

    venue, venue_short = extract_venue_from_bibtex(publication.get("bibtex", ""))
    if venue:
        publication["venue"] = venue
    if venue_short:
        publication["venueShort"] = venue_short
    if not publication.get("venue"):
        issue_url = publication.get("dblpIssueUrl", "")
        issue_venue = extract_venue_from_dblp_issue_url(issue_url)
        if issue_venue:
            publication["venue"] = issue_venue

    if not paper_url:
        bibtex_url = extract_url_from_bibtex(publication.get("bibtex", ""))
        if bibtex_url:
            publication["paperUrl"] = bibtex_url
            if "arxiv" in bibtex_url.lower() and not publication.get("arxivUrl"):
                publication["arxivUrl"] = bibtex_url
            paper_url = bibtex_url

    if paper_url and "arxiv" in paper_url.lower() and not publication.get("arxivUrl"):
        publication["arxivUrl"] = paper_url

    if not include_arxiv and paper_url and "arxiv" in paper_url.lower():
        publication["skip"] = True
        publication.pop("bibtexViewUrl", None)
        return publication

    year_text = extract_year_from_bibtex(publication.get("bibtex", ""))
    if year_text:
        publication["date"] = year_text
    if start_date and publication.get("date") and not is_on_or_after_start_date(publication.get("date", ""), start_date):
        publication["skip"] = True
        publication.pop("bibtexViewUrl", None)
        publication.pop("dblpIssueUrl", None)
        return publication

    if paper_url:
        metadata = fetch_metadata_from_paper_url(paper_url)
        publication["abstract"] = metadata.get("abstract", "")
        publication["date"] = metadata.get("date", "")
        publication["tags"] = metadata.get("tags", [])

    if not publication.get("date"):
        year_text = extract_year_from_bibtex(publication.get("bibtex", ""))
        if year_text:
            publication["date"] = year_text

    if start_date and not is_on_or_after_start_date(publication.get("date", ""), start_date):
        publication["skip"] = True

    publication.pop("bibtexViewUrl", None)
    publication.pop("dblpIssueUrl", None)
    return publication


def scrape_dblp_publications(url, include_arxiv=False, start_date=""):
    """
    Scrape publication information from the given DBLP author page URL.

    Args:
        url (str): The URL of the DBLP author page.

    Returns:
        list: A list of dictionaries containing publication information.
    """
    session = requests.Session()
    response = session.get(url, timeout=REQUEST_TIMEOUT)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {url}, Status Code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all publication entries
    publications = []
    bibtex_view_urls = []
    for entry in soup.find_all('li'):
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

        if publication.get("paperUrl") and "arxiv" in publication["paperUrl"].lower() and not publication.get("arxivUrl"):
            publication["arxivUrl"] = publication["paperUrl"]

        if start_date and publication.get("date") and not is_on_or_after_start_date(publication.get("date", ""), start_date):
            continue

        publications.append(publication)
        if bibtex_view_url:
            bibtex_view_urls.append(bibtex_view_url)

    for publication in publications:
        title = publication.get("title", "")
        try:
            run_with_publication_timeout(
                enrich_publication,
                PER_PUBLICATION_TIMEOUT_SECONDS,
                publication,
                include_arxiv,
                start_date,
            )
        except PublicationTimeout:
            print(f"抓取超时({PER_PUBLICATION_TIMEOUT_SECONDS}s): {title}")
            recover_arxiv_metadata_quick(publication)
            partial_content = {k: v for k, v in publication.items() if v}
            print("已抓取到的content:")
            print(json.dumps(partial_content, ensure_ascii=False, indent=2))
            publication.pop("bibtexViewUrl", None)
            publication.pop("dblpIssueUrl", None)

        title = publication.get("title", "")
        keys_to_check = ["date", "authors", "venue", "venueShort", "tags", "awards", "abstract", "arxivUrl", "paperUrl", "bibtex"]
        success_keys = []
        empty_keys = []
        for key in keys_to_check:
            value = publication.get(key)
            if value:
                success_keys.append(key)
            else:
                empty_keys.append(key)
        print(f"抓取完成: {title}")
        print(f"成功项: {', '.join(success_keys) if success_keys else '无'}")
        print(f"未成功项: {', '.join(empty_keys) if empty_keys else '无'}")
        time.sleep(PER_ITEM_SLEEP_SECONDS)

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
        raise ValueError(f"文件内容不是数组: {filepath}")
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

    for key in ["title", "date", "venue", "venueShort", "abstract", "bibtex", "paperUrl", "arxivUrl", "projectUrl", "slidesUrl"]:
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


def merge_into_merged_collection(merged_filepath, new_publications):
    existing_publications = load_js_array(merged_filepath)

    merged_by_key = {}
    ordered_keys = []
    for item in existing_publications:
        key = publication_dedup_key(item)
        if key not in merged_by_key:
            merged_by_key[key] = item
            ordered_keys.append(key)
        else:
            merge_publication_items(merged_by_key[key], item)

    deduped_titles = []
    added_titles = []
    for item in new_publications:
        key = publication_dedup_key(item)
        title = (item.get("title", "") or "").strip() or "(无标题)"
        if key in merged_by_key:
            merge_publication_items(merged_by_key[key], item)
            deduped_titles.append(title)
        else:
            merged_by_key[key] = item
            ordered_keys.append(key)
            added_titles.append(title)

    merged_data = [merged_by_key[key] for key in ordered_keys]
    save_to_js(merged_data, merged_filepath)

    print(f"并入 merged_collection.js 完成：新增 {len(added_titles)} 条，去重 {len(deduped_titles)} 条。")
    print("以下条目已去重（已存在于 merged_collection.js）:")
    if deduped_titles:
        for title in deduped_titles:
            print(f"  - {title}")
    else:
        print("  - 无")

    print("以下条目为新增并入（未命中去重）:")
    if added_titles:
        for title in added_titles:
            print(f"  - {title}")
    else:
        print("  - 无")

    return merged_data


def merge_into_existing_js_file(existing_js_filepath, new_publications):
    existing_publications = load_js_array(existing_js_filepath)

    merged_by_key = {}
    ordered_keys = []
    for item in existing_publications:
        key = publication_dedup_key(item)
        if key not in merged_by_key:
            merged_by_key[key] = item
            ordered_keys.append(key)
        else:
            merge_publication_items(merged_by_key[key], item)

    deduped_titles = []
    added_titles = []
    for item in new_publications:
        key = publication_dedup_key(item)
        title = (item.get("title", "") or "").strip() or "(untitled)"
        if key in merged_by_key:
            merge_publication_items(merged_by_key[key], item)
            deduped_titles.append(title)
        else:
            merged_by_key[key] = item
            ordered_keys.append(key)
            added_titles.append(title)

    merged_data = [merged_by_key[key] for key in ordered_keys]
    save_to_js(merged_data, existing_js_filepath)

    print(f"Merged into existing JS file: added {len(added_titles)}, deduplicated {len(deduped_titles)}.")
    return merged_data


def sanitize_js_filename(filename, fallback_name="scraped_publications"):
    raw = (filename or "").strip()
    if not raw:
        raw = fallback_name
    raw = re.sub(r"[^A-Za-z0-9._-]+", "_", raw)
    if not raw.lower().endswith(".js"):
        raw += ".js"
    return raw


def pick_path_from_file_manager(mode):
    if mode == "existing":
        script = 'POSIX path of (choose file with prompt "Select an existing .js file")'
    elif mode == "folder":
        script = 'POSIX path of (choose folder with prompt "Select a destination folder for new .js file")'
    else:
        raise ValueError("Unsupported picker mode")

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        stderr_text = (result.stderr or "").strip() or "Picker cancelled or failed"
        raise Exception(stderr_text)

    selected_path = (result.stdout or "").strip()
    if not selected_path:
        raise Exception("No path selected")
    return selected_path


def build_commit_message(author_name, publications):
    titles = [pub.get("title", "").strip() for pub in publications if pub.get("title", "").strip()]
    if not titles:
        return f"增加了{author_name}的publication"
    preview_count = min(5, len(titles))
    numbered_titles = [f"{index + 1}. {titles[index]}" for index in range(preview_count)]
    suffix = "；..." if len(titles) > preview_count else ""
    return f"增加了{author_name}的publication: {'；'.join(numbered_titles)}{suffix}"


def run_git_auto_flow(repo_root, filepaths, commit_message):
    relpaths = []
    for filepath in filepaths:
        if not filepath:
            continue
        relpaths.append(os.path.relpath(filepath, repo_root))
    if not relpaths:
        return

    subprocess.run(["git", "add", *relpaths], cwd=repo_root, check=True)
    diff_result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=repo_root)
    if diff_result.returncode == 0:
        print("没有检测到变更，已跳过 git commit / git push --force")
        return
    subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_root, check=True)
    subprocess.run(["git", "push", "--force"], cwd=repo_root, check=True)

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
        if not is_on_or_after_start_date(pub.get("date", ""), start_date):
            continue
        item = {
            "title": pub.get("title", ""),
            "date": pub.get("date", ""),
            "authors": pub.get("authors", []),
            "venue": normalized_venue,
            "venueShort": normalized_venue_short,
            "tags": pub.get("tags", []),
            "awards": pub.get("awards", []),
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
    storage_mode="",
    existing_js_path="",
    new_js_dir="",
    new_js_filename="",
):
    url = (url or "").strip() or DEFAULT_DBLP_URL
    if not re.match(r"^https://dblp\.org/pid/[^/]+/[^/]+\.html$", url):
        print("错误：网址格式不正确，示例：https://dblp.org/pid/c/SCCheung.html")
        return 1
    print(f"Scraping publications from {url}...")

    include_arxiv = parse_include_arxiv_input(include_arxiv_input)

    storage_mode = (storage_mode or "").strip().lower()
    if not storage_mode:
        print("错误：请先选择储存方式，再开始抓取。")
        return 1
    if storage_mode not in {"existing", "new"}:
        print("错误：储存方式无效，请重新选择。")
        return 1

    start_date_input = (start_date_input or "").strip()
    start_date = ""
    if start_date_input:
        start_date = normalize_date(start_date_input)
        if not start_date:
            print("错误：起始时间格式无效，请输入 YYYY 或 YYYY-MM-DD")
            return 1

    author_name = extract_author_name_from_dblp(url)
    if not author_name:
        print("错误：无法从该网址提取作者姓名")
        return 1
    safe_name = re.sub(r"[^A-Za-z0-9]+", "_", author_name.strip()).strip("_")
    if not safe_name:
        print("错误：作者姓名无法用于生成文件名")
        return 1

    try:
        publications, bibtex_view_urls = scrape_dblp_publications(
            url,
            include_arxiv=include_arxiv,
            start_date=start_date,
        )
        print(f"Successfully scraped {len(publications)} publications.")
        if bibtex_view_urls:
            print("BibTeX view URLs found:")
            for bibtex_url in bibtex_view_urls:
                print(bibtex_url)

        # Format publications to match the required JSON and JS structure
        formatted_publications = format_publications(
            publications,
            include_arxiv=include_arxiv,
            start_date=start_date,
        )
        print(f"筛选后保留 {len(formatted_publications)} 条 publication。")

        if storage_mode == "existing":
            js_filepath = (existing_js_path or "").strip()
            if not js_filepath:
                print("Error: Existing JS mode selected but no file path provided.")
                return 1
            if not os.path.exists(js_filepath):
                print(f"Error: Selected JS file does not exist: {js_filepath}")
                return 1
            merge_into_existing_js_file(js_filepath, formatted_publications)
            print(f"Publications saved to existing file: {js_filepath}")
            print("Skipped merged_collection update and git auto flow for custom target mode.")
            return 0

        if storage_mode == "new":
            target_dir = (new_js_dir or "").strip()
            if not target_dir:
                print("Error: New JS mode selected but no target folder provided.")
                return 1
            os.makedirs(target_dir, exist_ok=True)
            default_name = f"{safe_name}.js" if safe_name else "scraped_publications.js"
            js_filename = sanitize_js_filename(new_js_filename, fallback_name=default_name.replace(".js", ""))
            js_filepath = os.path.join(target_dir, js_filename)
            save_to_js(formatted_publications, js_filepath)
            print(f"Publications saved to new file: {js_filepath}")
            print("Skipped merged_collection update and git auto flow for custom target mode.")
            return 0

        return 1

    except Exception as e:
        print(f"An error occurred: {e}")
        return 1


def _render_gui_page_legacy(default_url=DEFAULT_DBLP_URL, default_start_date=""):
        return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Publication Scraper GUI</title>
    <style>
        body {{ font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; max-width: 980px; margin: 24px auto; padding: 0 16px; }}
        .card {{ border: 1px solid #ddd; border-radius: 10px; padding: 16px; margin-bottom: 16px; }}
        label {{ display: block; margin: 10px 0 6px; font-weight: 600; }}
        input[type=text], select {{ width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }}
        button {{ padding: 10px 14px; border: 0; border-radius: 8px; background: #111; color: #fff; cursor: pointer; }}
        pre {{ background: #0b1020; color: #d6e4ff; padding: 14px; border-radius: 10px; overflow: auto; white-space: pre-wrap; word-break: break-word; }}
        .hint {{ color: #666; font-size: 13px; }}
    </style>
</head>
<body>
    <h2>DBLP Publication Scraper GUI</h2>
    <div class=\"card\">
        <form method=\"post\" action=\"/run\">
            <label>DBLP 作者 URL</label>
            <input type=\"text\" name=\"url\" value=\"{default_url}\" required />
    <title>DBLP Publication Scraper</title>
            <label>起始日期（YYYY 或 YYYY-MM-DD，可空）</label>
            <input type=\"text\" name=\"start_date\" value=\"{default_start_date}\" />

            <label>抓取终点（publication list 按时间倒序，可选）</label>
        input[type=text] {{ width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }}
                <button type=\"button\" onclick=\"loadPublicationList()\">加载 publication list</button>
                <span class=\"hint\" id=\"list_status\">未加载</span>
            </div>
            <select id=\"end_marker_select\" disabled>
                <option value=\"\">抓取全部（不设终点）</option>
            </select>
    <h2>DBLP Publication Scraper</h2>

            <label><input type=\"checkbox\" name=\"include_arxiv\" value=\"y\" /> 包含 arXiv 论文</label>
            <label>DBLP Author URL</label>
            <button type=\"submit\">开始抓取并并入 merged_collection</button>
            <p class=\"hint\">日志中会显示：哪些条目被去重、哪些条目新增。</p>
            <label>Start date (YYYY or YYYY-MM-DD, optional)</label>
    </div>

            <label><input type="checkbox" name="include_arxiv" value="y" /> Include arXiv papers</label>
    statusEl.textContent = '加载中...';
            <button type="submit">Start scraping and merge into merged_collection</button>
            <p class="hint">Logs will show which entries were deduplicated and which were newly added.</p>

    try {{
        const resp = await fetch(`/publication_list?url=${{encodeURIComponent(url)}}`, {{ cache: 'no-store' }});
        if (!resp.ok) throw new Error('加载失败');
        const data = await resp.json();
        const list = data.publications || [];

        for (const item of list) {{
            const opt = document.createElement('option');
            const dateText = item.date || '未知日期';
            opt.value = item.marker;
            opt.textContent = `[${{dateText}}] ${{item.title}}`;
            selectEl.appendChild(opt);
        }}

        selectEl.disabled = false;
        statusEl.textContent = `已加载 ${{list.length}} 条`;
    }} catch (e) {{
        statusEl.textContent = '加载失败，请检查 URL';
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    const form = document.querySelector('form[action="/run"]');
    const selectEl = document.getElementById('end_marker_select');
    const hiddenEl = document.getElementById('end_marker');

    form.addEventListener('submit', () => {{
        hiddenEl.value = selectEl.value || '';
    }});
}});
</script>
</body>
</html>
"""


def render_gui_page(default_url=DEFAULT_DBLP_URL, default_start_date=""):
    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>DBLP Publication Scraper</title>
    <style>
        body {{ font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; max-width: 980px; margin: 24px auto; padding: 0 16px; }}
        .card {{ border: 1px solid #ddd; border-radius: 10px; padding: 16px; margin-bottom: 16px; }}
        label {{ display: block; margin: 10px 0 6px; font-weight: 600; }}
        input[type=text] {{ width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }}
        button {{ padding: 10px 14px; border: 0; border-radius: 8px; background: #111; color: #fff; cursor: pointer; }}
        .hint {{ color: #666; font-size: 13px; }}
        .row {{ display: flex; gap: 8px; align-items: center; margin-bottom: 8px; }}
        .hidden {{ display: none; }}
    </style>
</head>
<body>
    <h2>DBLP Publication Scraper</h2>
    <div class="card">
        <form method="post" action="/run">
            <label>DBLP Author URL</label>
            <input type="text" name="url" value="{default_url}" required />

            <label>Start date (YYYY or YYYY-MM-DD, optional)</label>
            <input type="text" name="start_date" value="{default_start_date}" />

            <label><input type="checkbox" name="include_arxiv" value="y" /> Include arXiv papers</label>

            <label>Save destination</label>
            <div class="row">
                <label><input type="radio" name="storage_mode" value="existing" onchange="toggleStorageMode()" /> Existing .js file</label>
                <label><input type="radio" name="storage_mode" value="new" onchange="toggleStorageMode()" /> Create new .js file</label>
            </div>

            <div id="existing_mode_block">
                <div class="row">
                    <button type="button" onclick="pickExistingJs()">Choose .js file</button>
                    <span id="existing_status" class="hint">No file selected</span>
                </div>
                <input type="text" id="existing_js_path" name="existing_js_path" placeholder="Selected existing .js file path" />
            </div>

            <div id="new_mode_block" class="hidden">
                <div class="row">
                    <button type="button" onclick="pickNewFolder()">Choose folder</button>
                    <span id="new_status" class="hint">No folder selected</span>
                </div>
                <input type="text" id="new_js_dir" name="new_js_dir" placeholder="Selected folder path" />
                <label>New filename (optional, default is author name)</label>
                <input type="text" id="new_js_filename" name="new_js_filename" placeholder="e.g. my_publications.js" />
            </div>

            <button type="submit">Start scraping</button>
            <p class="hint">Please select one save destination mode before starting.</p>
        </form>
    </div>
<script>
function toggleStorageMode() {{
    const selected = document.querySelector('input[name="storage_mode"]:checked');
    const mode = selected ? selected.value : '';
    document.getElementById('existing_mode_block').classList.toggle('hidden', mode !== 'existing');
    document.getElementById('new_mode_block').classList.toggle('hidden', mode !== 'new');
}}

async function pickExistingJs() {{
    const statusEl = document.getElementById('existing_status');
    statusEl.textContent = 'Opening file picker...';
    try {{
        const resp = await fetch('/pick_existing_js', {{ cache: 'no-store' }});
        const data = await resp.json();
        if (!resp.ok || !data.path) throw new Error(data.error || 'Failed to pick file');
        document.getElementById('existing_js_path').value = data.path;
        statusEl.textContent = 'Selected';
    }} catch (e) {{
        statusEl.textContent = 'Selection cancelled or failed';
    }}
}}

async function pickNewFolder() {{
    const statusEl = document.getElementById('new_status');
    statusEl.textContent = 'Opening folder picker...';
    try {{
        const resp = await fetch('/pick_new_js_folder', {{ cache: 'no-store' }});
        const data = await resp.json();
        if (!resp.ok || !data.path) throw new Error(data.error || 'Failed to pick folder');
        document.getElementById('new_js_dir').value = data.path;
        statusEl.textContent = 'Selected';
    }} catch (e) {{
        statusEl.textContent = 'Selection cancelled or failed';
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    toggleStorageMode();
    const form = document.querySelector('form[action="/run"]');
    form.addEventListener('submit', (event) => {{
        const selected = document.querySelector('input[name="storage_mode"]:checked');
        if (!selected) {{
            event.preventDefault();
            alert('Please choose a save destination before starting.');
        }}
    }});
}});
</script>
</body>
</html>
"""


def render_job_page(job_id):
        return f"""<!doctype html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Task Progress</title>
    <style>
        body {{ font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; max-width: 980px; margin: 24px auto; padding: 0 16px; }}
        .card {{ border: 1px solid #ddd; border-radius: 10px; padding: 16px; margin-bottom: 16px; }}
        .status {{ font-weight: 600; margin-bottom: 8px; }}
        pre {{ background: #0b1020; color: #d6e4ff; padding: 14px; border-radius: 10px; overflow: auto; white-space: pre-wrap; word-break: break-word; min-height: 320px; }}
        .ok {{ color: #0a7f2e; }}
        .err {{ color: #b00020; }}
    </style>
</head>
<body>
    <h2>Real-time Task Progress</h2>
    <div class=\"card\">
        <div id="status" class="status">Task started. Scraping in progress...</div>
        <p><a href="/">← Back to Home</a></p>
        <pre id=\"logs\"></pre>
    </div>

<script>
(() => {{
    const jobId = {json.dumps(job_id)};
    const logsEl = document.getElementById('logs');
    const statusEl = document.getElementById('status');
    let offset = 0;
    let done = false;

    async function poll() {{
        if (done) return;
        try {{
            const resp = await fetch(`/job_logs?id=${{encodeURIComponent(jobId)}}&offset=${{offset}}`, {{ cache: 'no-store' }});
            if (!resp.ok) {{
                statusEl.textContent = 'Failed to load logs. Please refresh and try again.';
                statusEl.className = 'status err';
                done = true;
                return;
            }}
            const data = await resp.json();
            if (data.chunk) {{
                logsEl.textContent += data.chunk;
                logsEl.scrollTop = logsEl.scrollHeight;
            }}
            offset = data.next_offset;
            if (data.done) {{
                done = true;
                if (data.exit_code === 0) {{
                    statusEl.textContent = `Completed (exit code: ${{data.exit_code}})`;
                    statusEl.className = 'status ok';
                }} else {{
                    statusEl.textContent = `Failed (exit code: ${{data.exit_code}})`;
                    statusEl.className = 'status err';
                }}
                return;
            }}
            setTimeout(poll, 1000);
        }} catch (e) {{
            statusEl.textContent = 'Network issue. Retrying...';
            statusEl.className = 'status err';
            setTimeout(poll, 1500);
        }}
    }}

    poll();
}})();
</script>
</body>
</html>
"""


def launch_browser_gui(host="127.0.0.1", port=8765):
    jobs = {}
    jobs_lock = threading.Lock()

    class JobLogWriter:
        def __init__(self, job):
            self.job = job

        def write(self, text):
            if not text:
                return 0
            with jobs_lock:
                self.job["logs"] += text
            return len(text)

        def flush(self):
            return

    def run_job(job):
        writer = JobLogWriter(job)
        try:
            with redirect_stdout(writer), redirect_stderr(writer):
                job["exit_code"] = run_scrape_flow(
                    job["url"],
                    job["include_arxiv_input"],
                    job["start_date"],
                    storage_mode=job.get("storage_mode", "default"),
                    existing_js_path=job.get("existing_js_path", ""),
                    new_js_dir=job.get("new_js_dir", ""),
                    new_js_filename=job.get("new_js_filename", ""),
                )
        except Exception as exc:
            with jobs_lock:
                job["logs"] += f"\nGUI task error: {exc}\n"
                job["exit_code"] = 1
        finally:
            with jobs_lock:
                job["done"] = True

    class Handler(BaseHTTPRequestHandler):
        def _write_html(self, content, status=200):
            data = content.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _write_json(self, payload, status=200):
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _redirect(self, location):
            self.send_response(303)
            self.send_header("Location", location)
            self.end_headers()

        def do_GET(self):
            parsed = urlparse(self.path)
            if parsed.path in ["/", "/index.html"]:
                self._write_html(render_gui_page())
                return
            if parsed.path == "/pick_existing_js":
                try:
                    selected_path = pick_path_from_file_manager("existing")
                    self._write_json({"path": selected_path})
                except Exception as exc:
                    self._write_json({"error": str(exc)}, status=400)
                return
            if parsed.path == "/pick_new_js_folder":
                try:
                    selected_path = pick_path_from_file_manager("folder")
                    self._write_json({"path": selected_path})
                except Exception as exc:
                    self._write_json({"error": str(exc)}, status=400)
                return
            if parsed.path == "/job":
                query = parse_qs(parsed.query)
                job_id = (query.get("id", [""])[0] or "").strip()
                with jobs_lock:
                    exists = job_id in jobs
                if not exists:
                    self._write_html("<h3>Task does not exist or has expired</h3>", status=404)
                    return
                self._write_html(render_job_page(job_id))
                return
            if parsed.path == "/job_logs":
                query = parse_qs(parsed.query)
                job_id = (query.get("id", [""])[0] or "").strip()
                offset_raw = (query.get("offset", ["0"])[0] or "0").strip()
                try:
                    offset = max(0, int(offset_raw))
                except ValueError:
                    offset = 0

                with jobs_lock:
                    job = jobs.get(job_id)
                    if not job:
                        self._write_json({"error": "job not found"}, status=404)
                        return
                    logs = job["logs"]
                    next_offset = len(logs)
                    chunk = logs[offset:next_offset] if offset <= next_offset else ""
                    done = bool(job.get("done"))
                    exit_code = job.get("exit_code")

                self._write_json({
                    "chunk": chunk,
                    "next_offset": next_offset,
                    "done": done,
                    "exit_code": exit_code,
                })
                return
            self._write_html("<h3>404 Not Found</h3>", status=404)

        def do_POST(self):
            if self.path != "/run":
                self._write_html("<h3>404 Not Found</h3>", status=404)
                return

            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length).decode("utf-8")
            fields = parse_qs(raw_body, keep_blank_values=True)

            url = fields.get("url", [""])[0]
            start_date = fields.get("start_date", [""])[0]
            include_arxiv_input = "y" if "include_arxiv" in fields else "n"
            storage_mode = (fields.get("storage_mode", [""])[0] or "").strip().lower()
            existing_js_path = fields.get("existing_js_path", [""])[0]
            new_js_dir = fields.get("new_js_dir", [""])[0]
            new_js_filename = fields.get("new_js_filename", [""])[0]

            if not storage_mode:
                self._write_html("<h3>Please choose a save destination before starting.</h3><p><a href='/'>← Back to Home</a></p>", status=400)
                return

            job_id = uuid.uuid4().hex
            job = {
                "id": job_id,
                "url": url,
                "start_date": start_date,
                "include_arxiv_input": include_arxiv_input,
                "storage_mode": storage_mode,
                "existing_js_path": existing_js_path,
                "new_js_dir": new_js_dir,
                "new_js_filename": new_js_filename,
                "logs": "",
                "done": False,
                "exit_code": None,
                "created_at": time.time(),
            }
            with jobs_lock:
                jobs[job_id] = job
                stale_ids = [
                    item_id for item_id, item in jobs.items()
                    if item.get("done") and (time.time() - item.get("created_at", time.time()) > 3600)
                ]
                for item_id in stale_ids:
                    jobs.pop(item_id, None)

            worker = threading.Thread(target=run_job, args=(job,), daemon=True)
            worker.start()
            self._redirect(f"/job?id={job_id}")

        def log_message(self, format_str, *args):
            return

    server = ThreadingHTTPServer((host, port), Handler)
    url = f"http://{host}:{port}"
    print(f"GUI started: {url}")
    print("Press Ctrl+C to stop the server")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description="Scrape DBLP publications")
    parser.add_argument("--gui", action="store_true", help="Start built-in browser GUI")
    args = parser.parse_args()

    if args.gui:
        launch_browser_gui()
        return

    url = input(f"请输入DBLP作者网址 (默认 {DEFAULT_DBLP_URL}): ").strip() or DEFAULT_DBLP_URL
    include_arxiv_input = input("是否包含 arXiv 论文？(y/N，支持输入“要/不要”): ")
    start_date_input = input("从哪一个时间之后开始（可留空，支持 YYYY 或 YYYY-MM-DD）: ").strip()
    storage_mode = input("请选择储存方式（existing/new）: ").strip().lower()
    existing_js_path = ""
    new_js_dir = ""
    new_js_filename = ""
    if storage_mode == "existing":
        existing_js_path = input("请输入已有 .js 文件路径: ").strip()
    elif storage_mode == "new":
        new_js_dir = input("请输入新建 .js 的目录路径: ").strip()
        new_js_filename = input("请输入新文件名（可留空，默认作者名）: ").strip()

    exit_code = run_scrape_flow(
        url,
        include_arxiv_input,
        start_date_input,
        storage_mode=storage_mode,
        existing_js_path=existing_js_path,
        new_js_dir=new_js_dir,
        new_js_filename=new_js_filename,
    )
    if exit_code != 0:
        sys.exit(exit_code)

if __name__ == "__main__":
    main()