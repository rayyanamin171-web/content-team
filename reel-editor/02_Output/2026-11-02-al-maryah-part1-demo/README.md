# Demo: Abu Dhabi Series – Part 1: Al Maryah Island (15.0 s)

> Reel Editor Agent · 2026-11-02 · **DEMO with placeholder footage.** Not for posting. It shows the style and the toolkit; the real cut waits for Rayan's 2-minute Al Maryah video.
> Built with: `python3 toolkit/build_reel.py configs/al-maryah-part1-demo.json` (free tools only, no credits used).

| File | What |
|---|---|
| `2026-11-02-al-maryah-part1-demo.mp4` | 1080×1920, 30 fps, H.264 + AAC 48 kHz, 15.0 s |
| `cover-frame0.png` | Frame 0 (hook already readable) |
| `contact-sheet.jpg` | 2 frames per second, for review |
| `check.json` | HyperFrames audit: **passes**. 4 advisory warnings say the end card could hold longer (see notes) |

## Beat sheet
| Time | Beat | On screen | Sound |
|---|---|---|---|
| 0.0–2.0 | Hook (placeholder: Rayan on camera) | "ABU DHABI SERIES · PART 1" / "Where does Abu Dhabi **do business?**" | hit |
| 2.0–10.5 | Map fly-in | UAE → Abu Dhabi emirate → Sentinel-2 satellite of Abu Dhabi → Al Maryah in 3D (gold outline) → pins: ADGM Square, The Galleria, Cleveland Clinic → pull back: **≈ 3.6 km straight line** to Louvre Abu Dhabi | whoosh, swooshes, ticks |
| 10.5–12.7 | Talking head (placeholder) + punch-in at 11.55 s | Lower third "Rayan Maniya / RERA BRN 68958"; captions "This is Al Maryah Island." / "Abu Dhabi's financial centre." | whoosh |
| 12.7–15.0 | End card | "Al Maryah Island", **Comment "MARYAH"**: "and I'll send you my branded-residence checklist", name, licence, handle | riser |

## Facts on screen (and why they're safe)
- ADGM, The Galleria and Cleveland Clinic are on Al Maryah Island: OSM/Overture positions; Atlas's script says the same.
- "Abu Dhabi's financial centre": ADGM (Abu Dhabi Global Market) is on the island; this line comes from Atlas's script.
- ≈ 3.6 km is a computed **straight-line** distance, labelled as such. No drive times, prices, yields or AED figures (Atlas's ⚠️ numbers are still unverified, so they're left out).
- Map credit is on screen in every map shot.

## Notes / to do with real footage
- Swap in Rayan's video: save it as `01_Input/footage/al-maryah.mp4`, set each footage segment's `in` (source time) in the config, point `captions` at the video (`time_base: footage`) for auto captions on the Mac, and re-run. The map is cached, so it won't re-render.
- No music in the demo (none licensed). Add a track from Instagram's in-app library when posting, or give us a licensed file.
- The real Part 1 will be longer (Atlas's script is ~60–70 s). The same config just gets more segments.
