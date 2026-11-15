#!/bin/bash
# Rebuilds Variation B from the original page. Run from anywhere: bash build.sh
set -e
D="$(cd "$(dirname "$0")" && pwd)"; S="$D/scripts"; T="$D/tmp"; mkdir -p "$T"
python3 "$S/rebuild.py" "$D/site/original/index.html" "$T/s0.html"   # new page sections
python3 "$S/gen.py"     "$T/s0.html" "$T/s1.html"                     # PNW scenes + motion
python3 "$S/polish.py"  "$T/s1.html" "$T/s2.html" "$S"                # icons, logo, fonts link
python3 "$S/local.py"   "$T/s2.html" "$T/s2b.html"                    # local copy, map, symbols, mural, reviews
python3 "$S/minify.py"  "$T/s2b.html" "$T/s3m.html"
python3 "$S/inject.py"  "$T/s3m.html" "$T/s3.html"                    # map library + map data
cp "$T/s3.html" "$D/site/variant-src/index.html"
python3 "$S/build2.py"  "$D/site/variant-src/index.html" "$D/site/variant-built/index.html"   # embeds img/ for the preview
ls -la "$D/site/variant-built/index.html"
python3 "$S/prod.py" "$D/site/variant-src" "$D/site/production"

# Main page: chimney & fireplace (wood, gas, pellet), made from the gas page
mkdir -p "$D/site/main-src" "$D/site/main-built"
[ -e "$D/site/main-src/img" ] || ln -s ../variant-src/img "$D/site/main-src/img"
python3 "$S/mainpage.py" "$D/site/variant-src/index.html" "$D/site/main-src/index.html"
python3 "$S/build2.py"  "$D/site/main-src/index.html" "$D/site/main-built/index.html"       # preview, photos built in
python3 "$S/prod.py" "$D/site/main-src" "$D/site/production-main" main

# DRAFT roofing page (separate company; placeholders in [brackets] until the owner sends real info)
mkdir -p "$D/site/roofing-built"
python3 "$S/roofpage.py" "$D/site/main-src/index.html" "$D/site/roofing-built/index.html"
