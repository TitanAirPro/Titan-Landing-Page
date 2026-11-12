# Titan Gas Fireplace — handoff for the next session

Last updated: Nov 12, 2026. Ads are approved, launch is close. The goal now is ads and a landing page that turn clicks into calls.

## 1. Where things are

- **Variation B preview (latest, version 35):** https://claude.ai/artifact/WJaoKgT5RbftBo6TeX39Lg
- **The other chat's preview** is a separate version. Nothing done here touched it.
- **This zip (`titan-build.zip`)** holds everything needed to rebuild Variation B from scratch. The build reproduces version 35 byte for byte.
  - `site/original/index.html`: the original page from your first zip (the starting point).
  - `site/variant-src/`: the Variation B page plus `img/` (job photos, testimonial video, poster, reviewer photos).
  - `site/production/`: the LIVE build (index.html + img/ + js/ + README.txt for the campaigner). Made by `scripts/prod.py` at the end of `build.sh`. Sent to the campaigner as `titan-gas-fireplace-live.zip` on Nov 12, 2026. Private view: https://claude.ai/artifact/VvHwykt9bgp3h3pKUuVVWm
  - `site/variant-built/index.html`: the preview build, with all photos built in (about 11 MB). **Preview only. Do not put this file live.**
  - `scripts/`: the build steps (see section 5).
  - `research/Washington chimney competitor teardown.md`: the competitor report and plan.

## 2. Standing rules (from you, never break)

1. Treat the current version as exact. Change only what you ask for, keep everything else identical, and update the same preview link.
2. Phone calls only: no forms, no "leave your info".
3. Offer: free gas fireplace inspection. CTA: "Call now to get scheduled".
4. No timing promises (no "same-day", no "within days").
5. Phone (425) 307-9165. Hours Sun–Fri 7:30 AM – 10:30 PM, closed Saturday. Owner: Zachary.
6. Phone-first layout. The hero is centered on phones and left-aligned on desktop.
7. Photos are always shown full, never cropped.
8. Preview pages must have the photos built in so they show in the iPhone app.

## 3. What Variation B has now (top to bottom)

- **Header:** logo, "★★★★★ 4.9 from 849 reviews · Licensed & insured" (desktop), call button.
- **Hero:**
  - 4.9 · 849 reviews badge
  - "Seattle-Area Gas Fireplace Repair"
  - "Gas Fireplace Won't Light? Get It Working Again Without a Surprise Bill."
  - call button
  - live "Open now till 10:30 PM" status, in Seattle time
  - Jessica B. quote
- Rainier dusk scene → trust strip → problems → "Free Means Free" with booking steps → video testimonials → amber band → Puget Sound scene (ferry, floatplane, salmon) → "You See the Price Before Anything Gets Touched" → services + brands list → crew photo slideshow → **Where We Work** (job map) → owner → **morning shoreline mural** (orcas, heron, rhododendrons) → FAQ (includes area, condo, fall smell and gas smell questions) → twilight lighthouse → final call → footer (Washington outline, city list).
- **Reviews:** Jessica Brown, Mohit Parul, Ashley Scheer and Elizabeth Phelps, with photos. The pairing with each review is assumed from the order you sent; you haven't confirmed it.
- **Job map:**
  - real coastline and highways, zoom and tap, numbers that total **2,012**
  - zoom-out locked to the job area at any screen size
  - the numbers are your 2,012 spread by the locations of 341 jobs in the older data copy, and the note under the map says so
- **Type:** Zilla Slab headlines with Public Sans body (default). The preview bar has a font switcher and an ad-version switcher for testing only.

## 4. Decisions already made

- Separate landing pages per service, not keyword swapping on one page.
- No made-up data. Map counts come from real job locations (scaled to the 2,012 total you gave).
- Washington symbols live inside the scenes, not as stickers on sections.
- "Watch our year" was removed: keep it simple.

## 5. How to rebuild in the next session

1. Attach `titan-build.zip` to the new chat.
2. Say: "Unzip it to /home/claude/titan-build and run `bash build.sh`".
3. The result is `site/variant-built/index.html`. To update the same preview link, publish it to https://claude.ai/artifact/WJaoKgT5RbftBo6TeX39Lg (read the artifact first, then publish with that URL).
4. Change content in `scripts/local.py` (most of the page copy, map, reviews, symbols), `scripts/rebuild.py` (core sections), `scripts/mapui2.py` (the job map) and `scripts/mural.py` (the shoreline mural).
5. For test screenshots, the next session needs `npm install leaflet@1.9.4 leaflet.markercluster@1.5.3 @fontsource/zilla-slab @fontsource/public-sans playwright` inside `scripts/`. The map library files are already included.

## 6. Launch checklist: do these before turning on ad spend

**A. The page that goes live**
1. Pick which version goes live: this chat's Variation B or the other chat's version.
2. ~~Make a **production build**~~ DONE Nov 12 (`site/production/`; real PageSpeed score still unchecked until it is live):
   - separate image files, compressed
   - testimonial video loads only when tapped
   - remove the yellow preview bar (font and ad switchers)
   - remove the keyword-swap script
   - load only the chosen font
   - Target: under 2 seconds on a phone. Check with PageSpeed Insights.
3. Domain and hosting: tell me where it lives. Link the Google Business Profile website to it.

**B. Tracking (without it you can't tell which ads make calls)**
1. Google Ads conversion: **"Calls from ads"**, counted from 60 seconds.
2. Google Ads conversion: **"Calls from website"**, using a Google forwarding number swapped onto the page for ad visitors, counted from 60 seconds. The page's phone links are all `tel:+14253079165`, so a swap script can find them.
3. Later: send booked or sold results from Titan Office back to Google Ads (offline conversion import), so Google bids toward booked jobs, not just calls.

**C. Ads that match the page**
1. Ad schedule: Sun–Fri 7:30 AM – 10:30 PM only. Calls outside those hours are wasted money.
2. Location: "Presence: people in or regularly in" your area, Marysville area to Tacoma area (the 60 cities on the page).
3. Every ad group's headlines should use the words its landing page uses: free inspection, written price, the problem (won't light, pilot, clicking, smell). Each service ad group should point to its own service page once those pages exist.
4. Add call assets, sitelinks to the service pages, callouts (Free inspection, Written price first, 4.9★ from 849 reviews, Licensed & insured) and structured snippets (Services: Repair, Pilot light, Annual service, Inserts, Conversions).
5. Negative keywords from day one: jobs, salary, DIY, how to, manual, parts, Home Depot, Lowe's, used, for sale, rent, wood stove (if you don't do those) and electric fireplace (if you don't do those).
6. Spend ramp: about $400/day for the first week, $800/day the second, then $1,333/day if cost per booked call holds. Check in Keyword Planner that Washington gas fireplace searches can absorb $1,333/day.

**D. Page accuracy (fix before ads, or reviewers and customers will catch it)**
1. **Who does repairs:** your techs inspect and clean (access panel and glass), and installs are done by insured subcontractors. The page says "we fix," which is fine for the company, but don't claim your own techs do installs. Add one line if you want: "Installs done by licensed, insured partners."
2. **849 reviews / 2,012 jobs** are company-wide, all services. The report recommends a small "all services" label so a gas fireplace page doesn't overstate.
3. **Free-inspection promise block** (top recommendation in the report), placed under the offer:
   - what the inspection checks
   - photos of anything wrong, taken in your fireplace
   - written price first, with no work or payment unless you say yes
   - second opinions welcome
   - your WA L&I license number

## 7. Inputs still needed from you

1. Domain and hosting for the live site.
2. WA L&I contractor license number.
3. Warranty length on work (the report recommends a written term; most competitors have none).
4. Can (425) 307-9165 receive texts? (A "call or text" option lifts calls.)
5. Confirm the review-to-name pairing (Jessica / Mohit / Ashley / Elizabeth).
6. ~~City list~~ confirmed Nov 12 (60 cities, Snohomish / King / Pierce). Confirm the brands list (Heat & Glo, Lennox, Majestic, Napoleon, Regency, Mendota, Travis, Valor, Heatilator, Kozy Heat).
7. Google review link (for "See all reviews") and the Google-only count, if you want it shown separately.
8. The final ad copy and keywords you got approved, so the next session can check that ads and page match.
9. Optional: a Titan Office backup, to rebuild the map from all 2,012 real jobs. Not required: the current map already totals 2,012.

## 8. What to build next (in order)

1. Production build + tracking (sections 6A and 6B): needed before spend.
2. Promise block + license number + "all services" label (6D).
3. Six service pages built from Variation B: `/gas-fireplace-repair`, `/pilot-light-repair`, `/gas-fireplace-service`, `/gas-fireplace-inspection`, `/gas-insert-installation`, `/wood-to-gas-conversion`. Each gets its own headline, problems, FAQ and title tag.
4. Ad copy check against the pages (message match), plus a phone booking script for whoever answers the calls.
5. After 2 weeks of data: cut keywords with no booked calls and test a second hero headline.

## 9. Paste this to start the next session

> Continue the Titan Gas Fireplace landing page. I'm attaching titan-build.zip. Read HANDOFF.md inside it first and follow its standing rules. Unzip to /home/claude/titan-build and run `bash build.sh`. It should reproduce the Variation B preview: https://claude.ai/artifact/WJaoKgT5RbftBo6TeX39Lg. Ads are approved and launching soon. Start with the launch checklist in section 6: production build, call tracking, and ads-to-page message match.
