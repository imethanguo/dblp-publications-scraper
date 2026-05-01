# dblp scraper

`dblp scraper` scrapes publications from a DBLP author page and merges them into an existing JS collection file.

## Features

- Scrape publication data from DBLP author pages.
- Optional inclusion of arXiv papers.
- Filter by start year (`YYYY`).
- Merge into an existing `.js` file.
- Dedup against existing collection files.
- LLM-based `venueShort` generation.
- Skip-cache for hard-blocking specific items.
- Config-driven execution.

## Project Structure

- `config.github.json`: config for GitHub Actions/CI
- `config.json`: local runtime config used by `./sp`
- `scrape_publications.py`: main program
- `sp`: shortcut launcher script
- `requirements.txt`: Python dependencies
- `.metadata_cache.json`: metadata cache (auto-generated)
- `.skip_cache.json`: skip cache (optional, user-managed)
- `.dedup_title_cache.json`: dedup title cache (auto-generated)

## Requirements

- macOS / Linux (Windows can run via Python directly)
- Python 3
- Network access to DBLP

## Quick Start

Install dependencies:

```bash
./sp i
```

Edit `config.json`, then run:

```bash
./sp
```

## Config Files

`config.json` and `config.github.json` share the same fields:

- `url`: DBLP author URL
- `include_arxiv`: `y`/`n` (or `true`/`false`)
- `start_date`: empty or `YYYY`
- `existing_js_path`: required
- `fast_mode`: `true`/`false` (reduce metadata timeout/retries)
- `venue_short_llm_base_url`: OpenAI-compatible base URL (DeepSeek: `https://api.deepseek.com/v1`)
- `venue_short_llm_api_key`: API key for the model provider (local config only)
- `venue_short_llm_model`: model name (DeepSeek: `deepseek-chat`)
- `venue_short_llm_timeout_seconds`: request timeout (seconds)
- `venue_short_llm_temperature`: model temperature
- `venue_short_reference_js_path`: reference JS file for learning venue->venueShort patterns
- `skip_cache_enabled`: `true`/`false`, enable skip cache
- `skip_cache_path`: path to a JSON array of skip keys (title:/doi:/arxiv:/url:)
- `scrape_run_retries`: retry count for the whole scrape run
- `scrape_run_retry_delay_seconds`: delay between retries (seconds)

`venueShort` generation rule (LLM):

- If BibTeX starts with `@article`, generate journal abbreviation as `venueShort`.
- If BibTeX starts with `@inproceedings`, generate conference abbreviation as `venueShort`.
- Prompt style is aligned using venue mappings extracted from `venue_short_reference_js_path`.

## Skip Cache

- File is a JSON array of strings (see `skip_cache_path`).
- Supported keys: `title:`, `doi:`, `arxiv:`, `url:`. If no prefix is provided, it is treated as a title.
- When a scraped entry matches any key, it is skipped before enrichment.

Example `.skip_cache.json`:

```json
[
  "title:Proceedings of the 15th Asia-Pacific Symposium on Internetware, Internetware 2024, Macau, SAR, China, July 24-26, 2024.",
  "doi:10.1145/3671016",
  "arxiv:2401.01234",
  "url:https://doi.org/10.1145/1234567.8901234"
]
```
Or
```json
[
  "Proceedings of the 15th Asia-Pacific Symposium on Internetware, Internetware 2024, Macau, SAR, China, July 24-26, 2024.",
]
```

## Command Reference

- `./sp` or `./sp run`: run scraping using `config.json`
- `./sp i`: install dependencies
- `./sp --help`: show help

Generate one `venueShort` from input venue name:

```bash
./sp --venue-short "International Conference on Machine Learning"
```

DeepSeek recommended usage (avoid writing API key to `config.json`):

```bash
export VENUE_SHORT_LLM_API_KEY="sk-your-real-key"
./sp --venue-short "International Conference on Machine Learning"
```

You can also configure LLM credentials via environment variables:

- `VENUE_SHORT_LLM_BASE_URL`
- `VENUE_SHORT_LLM_API_KEY`
- `VENUE_SHORT_LLM_MODEL`
- `VENUE_SHORT_LLM_TIMEOUT_SECONDS`
- `VENUE_SHORT_LLM_TEMPERATURE`

## Dedup Behavior

- Dedup reference source is the `collection` directory by default.
- `collection/auto-collected` is excluded from dedup reference scanning.
- If an incoming publication is duplicate, scraper skips it and does not mutate existing fields.

## Troubleshooting

### 1) `ModuleNotFoundError: No module named requests`

Run:

```bash
./sp i
```

### 2) `sp: command not found`

Use commands with `./` from the project root, such as `./sp` and `./sp i`.

### 3) `bash: ./sp: Permission denied`

`sp` is a script and needs execute permission. In the project root, run:

```bash
chmod +x ./sp
```

Then run your command again:

```bash
./sp
```

## Contact

yguocn@connect.ust.hk
