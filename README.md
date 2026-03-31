# dblp scraper

`dblp scraper` is a tool for scraping publications from DBLP author pages.

## Features

- Scrape publication data from DBLP author pages.
- Optional inclusion of arXiv papers.
- Filter by start year (`YYYY`).
- Save mode: merge into an existing `.js` file.
- Config-driven execution.

## Project Structure

- `scrape_publications.py`: main program
- `sp`: shortcut launcher script
- `config.json`: runtime config used by `./sp`
- `requirements.txt`: Python dependencies

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

## Config File

`config.json` fields:

- `url`: DBLP author URL
- `include_arxiv`: `y`/`n` (or `true`/`false`)
- `start_date`: empty or `YYYY`
- `existing_js_path`: required
- `max_workers`: parallel workers for enrichment
- `per_item_sleep_seconds`: pause after each item log
- `fast_mode`: `true`/`false`, reduce metadata timeout/retries for faster runs
- `venue_short_llm_enabled`: whether to enable LLM for venueShort (`true`/`false`)
- `venue_short_llm_base_url`: OpenAI-compatible base URL (DeepSeek: `https://api.deepseek.com/v1`)
- `venue_short_llm_api_key`: API key for the model provider
- `venue_short_llm_model`: model name (DeepSeek: `deepseek-chat`)
- `venue_short_llm_timeout_seconds`: request timeout (seconds)
- `venue_short_llm_temperature`: model temperature
- `venue_short_reference_js_path`: reference JS file for learning venue->venueShort patterns in prompt

`venueShort` generation rule (LLM):

- If BibTeX starts with `@article`, generate journal abbreviation as `venueShort`.
- If BibTeX starts with `@inproceedings`, generate conference abbreviation as `venueShort`.
- Prompt style is aligned using venue mappings extracted from `venue_short_reference_js_path`.

Example:

```json
{
  "url": "https://dblp.org/pid/257/0002.html",
  "include_arxiv": "N",
  "start_date": "2025",
  "existing_js_path": "/Users/guoyiheng/dblp-publications-scraper/my.js",
  "max_workers": 4,
  "per_item_sleep_seconds": 0,
  "fast_mode": true,
  "venue_short_llm_enabled": true,
  "venue_short_llm_base_url": "https://api.deepseek.com/v1",
  "venue_short_llm_api_key": "",
  "venue_short_llm_model": "deepseek-chat",
  "venue_short_llm_timeout_seconds": 20,
  "venue_short_llm_temperature": 0,
  "venue_short_reference_js_path": "../collection/merged_collection(updateVenueShort&sorted).js"
}
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

- `VENUE_SHORT_LLM_ENABLED`
- `VENUE_SHORT_LLM_BASE_URL`
- `VENUE_SHORT_LLM_API_KEY`
- `VENUE_SHORT_LLM_MODEL`
- `VENUE_SHORT_LLM_TIMEOUT_SECONDS`
- `VENUE_SHORT_LLM_TEMPERATURE`



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


