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
