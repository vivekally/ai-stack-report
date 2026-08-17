#!/usr/bin/env bash
#
# deploy.sh — publish the current canonical to GitHub Pages.
#
# This repo does NOT serve from main. GitHub Pages is configured to serve the
# `gh-pages` branch, which contains a single index.html. Pushing to main
# updates the source and changes nothing that a visitor sees. That gap is how
# gh-pages was once left three refreshes behind main.
#
#   Usage:  bash scripts/deploy.sh [path-to-canonical]
#   Default canonical: src/ai_stack_full_r2026-09.html
#
set -euo pipefail

CANON="${1:-src/ai_stack_full_r2026-09.html}"
WT="$(mktemp -d)/ghp"

GREEN='\033[0;32m'; RED='\033[0;31m'; BLUE='\033[0;34m'; NC='\033[0m'
info() { echo -e "${BLUE}[info]${NC}  $*"; }
ok()   { echo -e "${GREEN}[ok]${NC}    $*"; }
fail() { echo -e "${RED}[fail]${NC}  $*" >&2; exit 1; }

[ -f "$CANON" ] || fail "canonical not found: $CANON"
git diff --quiet && git diff --cached --quiet || fail "main has uncommitted changes; commit them first"

info "Canonical: $CANON ($(wc -c < "$CANON" | tr -d ' ') bytes)"

# Sanity-check that the file actually carries the current feature set, so a
# truncated or stale build cannot be published silently.
for marker in 'id="chartpack"' 'id="crosscutting"' 'id="adoption"' 'id="methodology"' 'window.STACK_DB'; do
  grep -q "$marker" "$CANON" || fail "canonical is missing '$marker' — refusing to deploy a partial build"
done
ok "canonical passed marker checks"

info "Preparing gh-pages worktree..."
git fetch -q origin gh-pages
git worktree add -q "$WT" gh-pages
trap 'git worktree remove --force "$WT" >/dev/null 2>&1 || true' EXIT
git -C "$WT" pull -q --ff-only origin gh-pages

cp "$CANON" "$WT/index.html"

if git -C "$WT" diff --quiet; then
  ok "gh-pages already matches the canonical; nothing to deploy"
  exit 0
fi

REFRESH=$(grep -o 'Refreshed August [0-9]*, 2026' "$CANON" | head -1 || echo "current build")
git -C "$WT" add index.html
git -C "$WT" commit -q -m "Deploy $(basename "$CANON" .html) (${REFRESH})"
git -C "$WT" push -q origin gh-pages
ok "deployed to gh-pages"

echo
echo "  Live in ~1-2 min: https://vivekally.github.io/ai-stack-report/"
echo "  Verify with:      curl -s https://vivekally.github.io/ai-stack-report/ | grep -c 'id=\"chartpack\"'"
