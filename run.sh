#!/usr/bin/env bash
set -e

BASEDIR="$(cd "$(dirname "$0")"/../Resources && pwd)"
cd "$BASEDIR"

if [ ! -d .venv ]; then
  echo "🛠️  Setting up Python environment (one‑time)…"
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install streamlit pandas rapidfuzz
else
  source .venv/bin/activate
fi

# <-- change is here -->
exec python -m streamlit run "$BASEDIR/app.py"
