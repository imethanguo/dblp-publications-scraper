# dblp scraper

`dblp scraper` is a tool for scraping publications from DBLP author pages, with both GUI and CLI workflows.

## Features

- Scrape publication data from DBLP author pages.
- Optional inclusion of arXiv papers.
- Filter by start date (`YYYY` or `YYYY-MM-DD`).
- Two save modes:
  - Merge into an existing `.js` file
  - Create a new `.js` file
- Real-time logs in GUI mode.

## Project Structure

- `scrape_publications.py`: main program (scraping, formatting, GUI server, save logic)
- `sp`: shortcut launcher script
- `requirements.txt`: Python dependencies

## Requirements

- macOS / Linux (Windows can run via Python directly)
- Python 3
- Network access to DBLP

## Quick Start

Run in the project root:

```bash
./sp i
```

Notes:
- `./sp i` automatically creates and uses the local `.venv` to install dependencies (avoids system Python package restrictions).

After installation, start the GUI:

```bash
./sp g
```

Start the CLI:

```bash
./sp c
```

## GUI Workflow

1. Run `./sp g` to open the page.
2. Enter a DBLP author URL.
3. Optional: set a start date (`YYYY` or `YYYY-MM-DD`).
4. Optional: enable arXiv inclusion.
5. **You must choose a Save destination before starting**, otherwise scraping will be blocked.
6. Fill fields based on selected save mode:
   - Existing: choose an existing `.js` file
   - New: choose a folder, optionally set a filename
7. Start scraping and monitor progress in the live log page.

## Save Modes

### 1) Existing .js file

- Merges results into your selected existing `.js` file.
- Does not update `merged_collection.js`.
- Does not trigger automatic git flow.

### 2) Create new .js file

- Creates a new `.js` file in your selected folder.
- Filename is optional; defaults to the author name if empty.
- Does not update `merged_collection.js`.
- Does not trigger automatic git flow.

## CLI Usage

Run:

```bash
./sp c
```

CLI prompts for:
- DBLP URL
- Include arXiv or not
- Start date
- Save mode (`existing` or `new`)
- Corresponding file/folder path inputs

## Command Reference

- `./sp g`: start GUI
- `./sp c`: start CLI
- `./sp x`: stop GUI (and try to free port 8765)
- `./sp i`: install dependencies
- `./sp --help`: show help

Long-form equivalents:
- `./sp gui` / `./sp cli` / `./sp stop` / `./sp install`

## Troubleshooting

### 1) `ModuleNotFoundError: No module named requests`

Run:

```bash
./sp i
```

### 2) `sp: command not found`

Use commands with `./` from the project root, such as `./sp g` and `./sp i`.

### 3) `OSError: [Errno 48] Address already in use`

The GUI port is occupied. Run:

```bash
./sp x
```

Then start again:

```bash
./sp g
```


