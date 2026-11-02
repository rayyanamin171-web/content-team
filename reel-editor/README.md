# Reel Editor: Rayan's Reel toolkit

> Reel Editor Agent · 2026-11-02 · Free tools only (FFmpeg, HyperFrames, MapLibre, open data). Nothing here posts or uploads anywhere.
> Style rules: `../style/rayan-reel-style.md` · Competitor research: `../research/competitor-style-breakdown.md`

**One command** turns a raw vertical clip + a small config into a finished 1080×1920 Reel: hook title, 3D map fly-in, footage with punch-ins, lower third, auto captions, wipes, sound effects and end card.

```bash
cd reel-editor
python3 toolkit/build_reel.py configs/al-maryah-part1-demo.json            # final render
python3 toolkit/build_reel.py configs/al-maryah-part1-demo.json --preview  # fast draft
```
Output: `02_Output/<id>/<id>.mp4` + `cover-frame0.png` + `contact-sheet.jpg` + `check.json`.

## Folder layout (mirrors the Mac master folder)
```
reel-editor/
  01_Input/            Rayan's files: footage/, transcripts/, References/ (see 01_Input/README.md)
  02_Output/           Finished Reels, one folder each
  configs/             One JSON per Reel (what to show, when)
  toolkit/
    build_reel.py      The one command
    brand.json         Name, licence line, handle, colours, fonts (change once → every Reel)
    overlays/          Presets: hook.html, lowerthird.html, captions.html, endcard.html (HyperFrames scenes)
    captions/          transcribe.py: faster-whisper (Mac) or SRT → timed words → caption groups
    map/               Offline map module (below)
    audio/             make_sfx.sh: our own synthesised SFX (hit, whoosh, tick, swoosh, riser)
    fonts/ vendor/     Playfair Display + Inter (OFL), MapLibre GL, GSAP, vendored (no CDNs needed)
    setup.sh           One-time install on the Mac
```

## The map module (`toolkit/map/`)
Offline and deterministic: each frame is rendered by MapLibre GL in headless Chromium, then FFmpeg encodes them.

| Step | Script | What it does |
|---|---|---|
| 1 | `fetch_overture.py` | Downloads OSM-based roads, buildings (with heights), coastline, water, landmarks for a bounding box from Overture Maps on AWS S3 (no key) |
| 2 | `fetch_sentinel.py` | Cuts a cloud-free Sentinel-2 satellite image (10 m) and feathers its edges |
| 3 | `prepare_area.py` | Slims the layers, finds the island outline, records every source + licence for the credit line |
| 4 | `scenes/<name>.json` | The shot: camera keyframes (UAE → city → island 3D), layer fades, labels, pins, distance callouts |
| 5 | `render_map.mjs` | Renders the scene to MP4 (`--frames 0,90,180 --out dir/` for quick stills) |

`build_reel.py` runs step 5 by itself and caches the result (`map/cache/`), so a map only re-renders when its scene changes.
Speed: in this CPU-only cloud box an 8.5 s map takes ~7 min (software WebGL). It should be much faster on a Mac with a GPU.

### New island in ~15 minutes (e.g. Saadiyat)
```bash
cd toolkit/map
# 1. data (bbox = lon/lat box around the island; a city box is already in data/abu-dhabi/)
python3 fetch_overture.py --bbox 54.40,24.52,54.48,24.58 --theme buildings --type building --out data/saadiyat/buildings.geojson
python3 fetch_overture.py --bbox 54.40,24.52,54.48,24.58 --theme transportation --type segment --out data/saadiyat/roads.geojson
python3 fetch_overture.py --bbox 54.40,24.52,54.48,24.58 --theme places --type place --out data/saadiyat/places.geojson   # to look up landmark coordinates
python3 prepare_area.py --city data/abu-dhabi --area data/saadiyat --point <lon,lat inside the island> --ne <natural-earth folder>
# 2. copy scenes/al-maryah-part1.json → scenes/saadiyat-part2.json; change camera targets, pins, callouts
node render_map.mjs --scene scenes/saadiyat-part2.json --out /tmp/stills --frames 30,120,200   # check stills
```
Natural Earth files: `https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/` (`ne_10m_admin_0_countries`, `ne_10m_admin_1_states_provinces`, `ne_10m_land`).

### Route line (optional)
`python3 route.py --roads data/<area>/render/area-roads.geojson data/<area>/render/city-roads.geojson --from <lon,lat> --to <lon,lat> --scene scenes/x.json --callout 0`
writes a road-following path into that callout (drawn solid gold with `"dashed": false`). It's the shortest path on OSM road geometry, **ignoring one-ways and traffic**, so use it for the shape only. Label it "Indicative route", never with km or minutes unless verified. It warns if an end point snaps more than 150 m away (fetch street-level roads there first).

### Map rules
- Pins only at coordinates from OSM/Overture (look them up in `places.geojson` / `buildings.geojson`), never guessed.
- Callout labels use `{km}`, which is computed as a straight line. Label it "Straight line". Drive times only if verified; otherwise `"placeholder": true` shows a red dashed outline so it can't slip through.
- The credit line is generated automatically. Don't remove it. Licences: `toolkit/map/CREDITS.md`.

## Config reference (`configs/*.json`)
```jsonc
{
  "id": "2026-11-02-al-maryah-part1-demo",          // output folder/file name
  "footage": "01_Input/footage/al-maryah.mp4",       // missing → labelled placeholder
  "timeline": [                                      // played in order; wipes between segments
    { "type": "footage", "in": 0.0, "dur": 2.0, "punch": [[0, 1.0], [2.0, 1.04]] },  // in = source time; punch = [t, scale]
    { "type": "map", "scene": "toolkit/map/scenes/al-maryah-part1.json" },           // length from the scene
    { "type": "footage", "in": 2.0, "dur": 2.2, "punch": [[0, 1.0], [1.05, 1.0], [1.06, 1.09]] }, // instant punch-in
    { "type": "endcard", "dur": 2.3 }
  ],
  "hook": { "kicker": "Abu Dhabi Series · Part 1", "text": "Where does Abu Dhabi *do business?*" }, // *gold words*
  "lower_third": { "start": 10.6, "dur": 2.0 },      // name + licence line from brand.json
  "captions": { "src": "01_Input/transcripts/x.srt", "time_base": "reel", "max_words": 5 },
  //   or { "src": "01_Input/footage/al-maryah.mp4", "time_base": "footage" }  → faster-whisper on the Mac
  "end_card": { "kicker": "...", "title": "Al Maryah Island", "cta": "Comment “MARYAH”", "cta_sub": "..." },
  "music": { "src": "01_Input/music/licensed-track.mp3", "volume": 0.2 },  // optional; or add IG library music at upload
  "sfx": true
}
```

## Captions only (any clip)
Make a config with one footage segment covering the clip, plus `captions`, and leave out the hook, map, lower third and end card. That gives a caption burner in the house style. Need just the SRT? `python3 toolkit/captions/transcribe.py clip.mp4 --out words.json --srt clip.srt`.

## Cloud vs Mac
| | Cloud session | Rayan's Mac |
|---|---|---|
| Map data (S3: Overture, Sentinel-2) | ✅ | ✅ |
| Standard tile servers (OSM tiles, Carto…) | ❌ blocked; not needed | — |
| Auto captions (needs model download from Hugging Face) | ❌ blocked → use SRT | ✅ `pip3 install faster-whisper` |
| Instagram (competitor viewing) | ❌ blocked | ✅ (screen-record for reference) |
