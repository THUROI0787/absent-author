#!/usr/bin/env bash
# Replace the OWNER placeholder with your GitHub user or org (and optionally the repo name).
#   tools/set_repo.sh your-github-name [repo-name]
# Works with both macOS (BSD) and GNU sed.
set -euo pipefail
OWNER="${1:?usage: tools/set_repo.sh OWNER [REPO]}"; REPO="${2:-absent-author}"
cd "$(dirname "$0")/.."
grep -rlE "OWNER(/|\.github\.io/)absent-author" --include='*.md' --include='*.html' --include='*.js' \
     --include='*.cff' --include='*.yml' --include='*.sh' . | grep -v "tools/set_repo.sh" | while read -r f; do
  sed -i.bak -e "s#OWNER/absent-author#${OWNER}/${REPO}#g" -e "s#OWNER\.github\.io/absent-author#${OWNER}.github.io/${REPO}#g" "$f"
  rm -f "$f.bak"
  echo "updated $f"
done
echo "Links now point to https://github.com/${OWNER}/${REPO} and https://${OWNER}.github.io/${REPO}/"
