# Ramhan Island cover, Episode 2: real-photo background

> Reel Editor · 2026-11-04 · Status: **PREVIEW.** Real imagery only (no AI). Nothing posted.

**Original cover not found** (not on the Mac master folder or in the repo, per the Files & Media Agent). So the **text and layout here are provisional**: series line / "Episode 2" / "Ramhan Island" in the Abu Dhabi Series style. When the original turns up, match its exact layout in `template.html` and re-render. Only the background changes.

| File | What |
|---|---|
| `ramhan-ep2-cover-PREVIEW-A-topdown-1080x1920.png` | Real Sentinel-2 satellite photo, straight down, island centred |
| `ramhan-ep2-cover-PREVIEW-B-aerial-1080x1920.png` | Same photo tilted for an aerial feel (closest to the original's "aerial with a bridge" look; the E12 highway bridges are visible) |
| `plates/` | Clean 1080×1920 backgrounds (no text) |
| `template.html` + `render.mjs` | `node render.mjs --bg plates/<plate>.jpg --out cover.png [--l1 "..." --l2 "..." --l3 "RAMHAN ISLAND"]` |
| `CREDITS.md` | Sources, licences, credit lines |

Safe area: all text inside y 285–1635 (4:5 grid crop) and below the top 168 px.
Map scenes for the plates: `toolkit/map/scenes/ramhan-cover-*.json` (+ `toolkit/map/data/ramhan/`).

**Recommended:** use the NASA ISS065-E-74286 photo (public domain, sharper) once its upload is approved, with the same template. Keep **A or B** as the "current development" version.
