# Al Maryah Reel Cover v2: Presenter Style (Rayan + Skyline)

> Frame · 2026-11-02 · Status: **v2 A FINAL DRAFT for Rayan:** licensed Pexels skyline (Naeem Alterawy, credit optional) + Rayan's headshot cut-out. Variant B (video frame) waits for the video. Free tools only. Nothing posted.

## Latest
- **`ig-cover-v2-A-1080x1920.png`**: Rayan's headshot cut-out (background removed offline, 2x Lanczos upscale + light sharpen, colour-matched, gold edge light, shadow) over the licensed Al Maryah night skyline (`inputs/skyline-web-a-naeem-1080x1920.jpg`: 9:16 crop on the ADGM towers, sky extended upward, navy grade). Render: `node render.js --bg inputs/skyline-web-a-naeem-1080x1920.jpg --person inputs/rayan-headshot-cutout.png --ph 1000 --pright -150 --bright 0.86 --sat 0.88 --warm 0.03 --out ig-cover-v2-A-1080x1920.png`
- **No variant C:** the other two web photos didn't fit (stormy lightning shot; daytime CC BY-SA shot needs a credit and share-alike). See `CREDITS.md`.
- **`cutout-comparison-headshot-vs-awards.jpg`**: both of Rayan's photos tried. **Headshot chosen:** it's sharp at full size (face ≈ 260 px wide in the source). The awards photo had to be cropped above the trophy plaque, which carries Emaar/award text, leaving a face only ≈ 80 px wide. At cover size it's visibly soft, with JPEG blocking and a light halo from the glowing ring behind. No Emaar logo or award-wall text survives in either cut-out.
- **Best next photo:** a sharper, waist-up shot turned slightly left (spec below) would beat both. The headshot is front-facing and only 600 px tall.

## What's here
| File | What |
|---|---|
| `ig-cover-v2-A-1080x1920.png` | **v2 A:** Rayan cut-out + licensed web skyline |
| `inputs/skyline-web-a-naeem-1080x1920.jpg` | Prepared 9:16 skyline background |
| `cutout-comparison-headshot-vs-awards.jpg` | Headshot vs awards-photo cut-out, side by side |
| `inputs/rayan-*-cutout.png` | Transparent cut-outs ready to reuse |
| `ig-cover-v2-placeholder-1080x1920.png` | Layout preview with placeholders for the skyline and for Rayan |
| `template.html` | v2 source: v1 style (gold label, Playfair title, navy gradients) + Rayan cut-out layer |
| `render.js` | Renders the template to PNG |
| `tools/cutout.mjs` | Offline background removal (tested, works) |
| `tools/grab-frames.sh` | FFmpeg: pulls 9:16 frames from a video + a numbered contact sheet (tested) |
| `CREDITS.md` | Image sources and licences (web photo pending) |

## Layout
- **Top-left:** gold label "ABU DHABI SERIES – PART 1", gold rule, then "Al Maryah / Island" in Playfair Display Bold 158 px, tagline "Abu Dhabi, honestly."
- **Background:** skyline full-bleed, with the towers in the middle band. Navy gradient at the top behind the text.
- **Right/lower:** Rayan waist-up, turned slightly left, looking toward the title and skyline (presenter style). His head sits inside the 4:5 grid crop, and his body runs off the bottom edge into a navy fade.
- **Cut-out treatment:** colour-matched to blue hour (`--bright`, `--sat`, `--warm`), a subtle gold edge light on the left (the side facing the skyline glow) and a soft drop shadow.
- Everything key sits inside the centre 1080×1350. Size 1080×1920.

## Inputs needed (drop into `inputs/2026-11-02-al-maryah/` at the repo root, or attach in chat)

### 1. Rayan's photo
- **Pose:** waist-up (head to belt), body turned about 30° to *his* left, face toward the camera or eyes looking slightly left (toward where the title sits). Calm, confident, slight smile or neutral. Hands relaxed or one hand in a pocket.
- **Outfit:** what he wore in the Al Maryah Reel (suit or smart, dark jacket reads best on navy).
- **Background:** plain and evenly lit (a wall or sky), not busy, and not the same colour as his clothes.
- **Light:** soft, from his left or the front. Avoid harsh overhead sun. A shot at blue hour or in shade will colour-match best.
- **Resolution:** at least **1500 px tall** for the head-to-belt area (any modern phone in portrait is fine). Send the original file, not a WhatsApp-compressed copy.
- **Ideal:** 3–5 options, so we can pick the best expression.

### 2. The Al Maryah video
The original file (MOV/MP4). Frame will pull candidate frames of the skyline at blue hour.

### 3. Web skyline photo
Blocked by the session's network policy. See `CREDITS.md` for the domains to allow.

## When inputs arrive (commands)
```
# one-time: install the cut-out tool (~130 MB, model included, runs offline)
cd tools && npm install && cd ..
# 1) cut out Rayan
node tools/cutout.mjs ../../../inputs/2026-11-02-al-maryah/rayan.jpg inputs/rayan-cutout.png
# 2) candidate frames from the video, then pick one from inputs/frames/contact-sheet.jpg
tools/grab-frames.sh ../../../inputs/2026-11-02-al-maryah/al-maryah.mp4 2 inputs/frames
# 3) A/B renders
node render.js --bg inputs/skyline-web.jpg --person inputs/rayan-cutout.png --out ig-cover-v2-A-web-1080x1920.png
node render.js --bg inputs/frames/frame-012.jpg --person inputs/rayan-cutout.png --out ig-cover-v2-B-video-1080x1920.png
```
Tune the colour match per photo, e.g. `--bright 0.9 --sat 0.9 --warm 0.08`, and the skyline crop with `--bgpos "50% 40%"`.

## A/B plan
- **A, web skyline:** professional photo quality, but it needs a credit if the licence requires one.
- **B, video frame:** Rayan's own footage, so no credit needed, and it matches the Reel exactly.
Frame will recommend one after seeing both.
