#!/usr/bin/env bash
# Install graphifyy CLI for knowledge-graph extraction and query.
# Does not mutate global Cursor config — project rule is already in .cursor/rules/graphify.mdc

set -euo pipefail

echo "graphify installer"
echo "Source: https://pypi.org/project/graphifyy/"
echo ""

if command -v graphify >/dev/null 2>&1 && graphify --help >/dev/null 2>&1; then
  echo "graphify already installed."
  graphify --help 2>&1 | head -1 || true
  echo ""
  echo "Build:  make graph   (or: graphify extract .)"
  echo "Query:  make graph-query QUERY=\"your question\""
  echo "Update: make graph-update   (after code edits)"
  exit 0
fi

if command -v uv >/dev/null 2>&1; then
  echo "Installing via uv tool..."
  uv tool install --upgrade graphifyy
elif command -v pip3 >/dev/null 2>&1; then
  echo "Installing via pip..."
  pip3 install --user --upgrade graphifyy
elif command -v pip >/dev/null 2>&1; then
  echo "Installing via pip..."
  pip install --user --upgrade graphifyy
else
  echo "ERROR: Need uv or pip to install graphifyy."
  echo "  curl -LsSf https://astral.sh/uv/install.sh | sh   # recommended"
  exit 1
fi

if ! command -v graphify >/dev/null 2>&1; then
  echo ""
  echo "ERROR: graphify not on PATH after install."
  echo "Add ~/.local/bin to PATH if you used pip --user, or open a new shell after uv tool install."
  exit 1
fi

echo ""
echo "Installed graphify."
echo ""
echo "Optional: export GEMINI_API_KEY=... for semantic extraction on markdown/docs."
echo ""
echo "Next steps:"
echo "  make graph              # build graphify-out/"
echo "  open graphify-out/graph.html"
echo "  make graph-query QUERY=\"How is this project structured?\""
