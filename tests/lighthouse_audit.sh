#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p docs/lighthouse
export CHROME_PATH="${CHROME_PATH:-/usr/bin/chromium}"
CLI="${LIGHTHOUSE_CLI:-lighthouse}"
ORIGIN="${TEST_ORIGIN:-http://127.0.0.1:3000}"
for entry in 'home:/' 'features:/features' 'auto:/auto' 'guide:/guide?system=auto' 'faq:/faq' 'contact:/contact'; do
  name="${entry%%:*}"; route="${entry#*:}"
  echo "Lighthouse mobile: $name"
  "$CLI" "$ORIGIN$route" --chrome-flags='--headless --no-sandbox --disable-dev-shm-usage' --only-categories=performance,accessibility,best-practices,seo --output=html --output=json --output-path="docs/lighthouse/$name-mobile" --quiet
  echo "Completed $name"
done
echo 'Lighthouse desktop: home'
"$CLI" "$ORIGIN/" --preset=desktop --chrome-flags='--headless --no-sandbox --disable-dev-shm-usage' --only-categories=performance,accessibility,best-practices,seo --output=html --output=json --output-path=docs/lighthouse/home-desktop --quiet
echo 'All Lighthouse reports completed.'
