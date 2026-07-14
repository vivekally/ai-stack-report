#!/usr/bin/env bash
#
# push_to_github.sh
# One-command: initialize git, create GitHub repo via `gh` CLI, and push.
#
# Usage:
#   bash push_to_github.sh                              # defaults: repo name "ai-stack-report", private
#   bash push_to_github.sh my-repo-name                 # custom name, private
#   bash push_to_github.sh my-repo-name public          # custom name, public
#
# Prerequisites (all checked below):
#   - git (`brew install git` or system package manager)
#   - gh  (`brew install gh` or https://cli.github.com)
#   - authenticated to GitHub: run `gh auth login` once before this script
#
# Safe to re-run: script fails fast if any prerequisite is missing or if the
# working directory already has a git repo initialized.

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────
REPO_NAME="${1:-ai-stack-report}"
VISIBILITY="${2:-private}"      # 'private' or 'public'
DESCRIPTION="Definitive landscape report on the AI technology stack. 12 layers, 97 companies, interactive search + knowledge graph."

# ── Color helpers ─────────────────────────────────────────────────
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()  { echo -e "${BLUE}[info]${NC}  $*"; }
ok()    { echo -e "${GREEN}[ok]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[warn]${NC}  $*"; }
fail()  { echo -e "${RED}[fail]${NC}  $*" >&2; exit 1; }

# ── Preflight ─────────────────────────────────────────────────────
info "Preflight checks..."

command -v git >/dev/null 2>&1 || fail "git is not installed. Install via: brew install git (macOS) or apt-get install git (Linux)."
ok "git is installed ($(git --version | head -1))"

command -v gh >/dev/null 2>&1 || fail "gh CLI is not installed. Install via: brew install gh, or see https://cli.github.com"
ok "gh CLI is installed ($(gh --version | head -1))"

gh auth status >/dev/null 2>&1 || fail "gh is not authenticated. Run: gh auth login"
GH_USER=$(gh api user -q .login 2>/dev/null || echo "unknown")
ok "gh authenticated as: $GH_USER"

if [ "$VISIBILITY" != "private" ] && [ "$VISIBILITY" != "public" ]; then
  fail "Visibility must be 'private' or 'public'. Got: $VISIBILITY"
fi

if [ -d ".git" ]; then
  fail "This directory already has a .git folder. Delete it first or run this script from a fresh copy."
fi

if [ ! -f "README.md" ] || [ ! -d "src" ]; then
  fail "This script must be run from the root of the ai-stack-report folder (needs README.md and src/)."
fi

# ── Confirm plan ──────────────────────────────────────────────────
echo
info "About to create GitHub repo:"
echo "         name: $REPO_NAME"
echo "   visibility: $VISIBILITY"
echo "        owner: $GH_USER"
echo "         path: $(pwd)"
echo
read -r -p "Proceed? [y/N] " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
  warn "Aborted by user. No changes made."
  exit 0
fi

# ── Initialize git ────────────────────────────────────────────────
info "Initializing git..."
git init -b main >/dev/null
git add .
ok "Staged $(git diff --cached --name-only | wc -l | tr -d ' ') files"

git commit -m "Initial commit: AI Stack Landscape Report

- 12-layer stack map with 70 sub-layers
- 97-company interactive database with 252 mapped connections
- Sub-layer collapsible panels, update banner with inline corrections
- Company search modal + D3 knowledge graph in unified file
- Build scripts and design system documented in CLAUDE.md" >/dev/null
ok "Initial commit created"

# ── Create GitHub repo and push ───────────────────────────────────
info "Creating GitHub repo and pushing..."
gh repo create "$REPO_NAME" \
  --"$VISIBILITY" \
  --description "$DESCRIPTION" \
  --source=. \
  --remote=origin \
  --push

# ── Done ──────────────────────────────────────────────────────────
REPO_URL="https://github.com/$GH_USER/$REPO_NAME"
echo
ok "Done. Repo is live at:"
echo "         $REPO_URL"
echo
info "Next steps:"
echo "   1. Open the repo:              gh browse"
echo "   2. Preview the canonical file: open src/ai_stack_unified_search_r2026-07b.html"
echo "   3. Enable GitHub Pages if you want a hosted URL:"
echo "                                  gh api -X POST repos/$GH_USER/$REPO_NAME/pages -f source[branch]=main -f source[path]=/src"
echo
