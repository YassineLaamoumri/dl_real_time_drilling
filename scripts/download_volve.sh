#!/usr/bin/env bash
set -euo pipefail

BASE_URL="https://www.ux.uis.no/~atunkiel"
OUT_DIR="data/raw"
mkdir -p "$OUT_DIR"

echo "📥 Downloading selected Volve archives to $OUT_DIR (edit script to add more)."
urls=(
  "file_list.html?utm_source=chatgpt.com"
)
for u in "${urls[@]}"; do
  echo "🔗 $BASE_URL/$u"
  curl -fSL "$BASE_URL/$u" -o "$OUT_DIR/$(basename "$u")"
done

echo "✅ Done. Manually add specific zip URLs you want to fetch."

