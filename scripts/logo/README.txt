Header logo (site/variant-src/img/logo.png)
- elephant_source.webp: the owner's Titan logo (Nov 12, 2026).
- make.py + comp.js: crop off the TITAN / Air Duct · Chimney · Dryer text, make the background
  transparent, lift the smoke and put the page's flame on the trunk tip.
  Run from this folder:  python3 make.py 6 -78 80  then  node comp.js 3.3 914 220 full.png
  (comp.js needs playwright; then trim, pad 8 px and resize to 132 px tall; a small speck at x 740-860, y 180-245 of full.png was cleared by hand)
- elephant_flame_full.png: the large version. img/logo.png is it at 132 px tall (3x the header size).
