#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
PARENT_PYTHON_BIN="$ROOT_DIR/../.venv/bin/python"
SCRIPT="$ROOT_DIR/scrape_publications.py"
REQUIREMENTS_FILE="$ROOT_DIR/requirements.txt"

ensure_local_venv() {
  if [[ -x "$PYTHON_BIN" ]]; then
    return
  fi

  if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 not found. Please install Python 3 first."
    exit 1
  fi

  python3 -m venv "$ROOT_DIR/.venv"
  "$PYTHON_BIN" -m pip install --upgrade pip >/dev/null
}

pick_python() {
  if [[ -x "$PYTHON_BIN" ]]; then
    echo "$PYTHON_BIN"
    return
  fi
  if [[ -x "$PARENT_PYTHON_BIN" ]]; then
    echo "$PARENT_PYTHON_BIN"
    return
  fi
  echo "python3"
}

show_help() {
  cat <<'EOF'
Usage:
  ./sp          # run with config.json
  ./sp r        # run with config.json (short)
  ./sp i        # install required python packages (short)

  ./sp run      # run with config.json
  ./sp install  # install required python packages
  ./sp --help   # show script help

  ./sp [args]   # pass args directly to scrape_publications.py
EOF
}

install_deps() {
  ensure_local_venv

  if [[ -f "$REQUIREMENTS_FILE" ]]; then
    "$PYTHON_BIN" -m pip install -r "$REQUIREMENTS_FILE"
  else
    "$PYTHON_BIN" -m pip install requests beautifulsoup4
  fi
}

ensure_runtime_deps() {
  local python_exec
  python_exec="$(pick_python)"

  if ! "$python_exec" -c "import requests; from bs4 import BeautifulSoup" >/dev/null 2>&1; then
    echo "Missing required Python packages. Run: ./sp i"
    exit 1
  fi
}

CMD="${1:-}"
case "$CMD" in
  ""|r|run)
    shift || true
    ensure_runtime_deps
    exec "$(pick_python)" "$SCRIPT" "$@"
    ;;
  i|install|deps)
    shift || true
    install_deps
    exit 0
    ;;
  h|help|-h|--help)
    show_help
    exit 0
    ;;
esac

ensure_runtime_deps
exec "$(pick_python)" "$SCRIPT" "$@"
