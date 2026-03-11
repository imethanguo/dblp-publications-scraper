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

Example:

```json
{
  "url": "https://dblp.org/pid/257/0002.html",
  "include_arxiv": "N",
  "start_date": "2025",
  "existing_js_path": "/Users/guoyiheng/dblp-publications-scraper/my.js"
}
```

## Command Reference

- `./sp` or `./sp run`: run scraping using `config.json`
- `./sp i`: install dependencies
- `./sp --help`: show help



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


