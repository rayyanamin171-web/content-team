# CREDITS: Al Maryah Reel Cover v2

> Every image used on the cover is logged here: source URL, author, licence and the credit line the caption needs.

## Skyline photo (web): USED in v2 A
Sourced and approved by Rayan via the CEO Agent (originals + `CREDITS.txt` in `inputs/2026-11-02-al-maryah/web-skyline/` at the repo root).

| Field | Value |
|---|---|
| File | `al-maryah-night-waterfront_pexels-naeem-alterawy-16136072.jpeg` (5760×3840) |
| Source URL | https://www.pexels.com/photo/a-city-by-the-river-in-the-evening-16136072/ |
| Author | Naeem Alterawy (Pexels) |
| Licence | Pexels License (https://www.pexels.com/license/): free for commercial use |
| Attribution needed? | **No** (optional) |
| Caption credit line (optional) | Photo by Naeem Alterawy on Pexels |
| Changes made | Vertical 9:16 crop centred on the ADGM towers; night sky extended upward with a matching dark gradient (no buildings added or changed); slight desaturation and navy grade; text and Rayan's cut-out composited on top. Prepared file: `inputs/skyline-web-a-naeem-1080x1920.jpg` |

### Candidates not used
| File | Licence | Why not |
|---|---|---|
| `al-maryah-lightning-night_pexels-eslam-mohammed-abdelmaksoud-28718190.jpeg` | Pexels License, credit optional | Stormy and dramatic, which is off-brand for "calm, not hype". A 9:16 crop can't hold both the lightning and the towers. |
| `al-maryah-day-waterfront_wikimedia-mavariz-cc-by-sa-4.0.jpg` | CC BY-SA 4.0, **credit required, share-alike** | Daytime (series look is blue hour/night). Share-alike would make the cover CC BY-SA and require the credit, so avoid it for commercial use. If it's ever used, the caption must carry: "Al Mariah Island- Abudhabi" by MAVARIZ, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0/>, via Wikimedia Commons |

## Rayan's photo
Rayan's own photos, supplied by him (`inputs/2026-11-02-al-maryah/` at the repo root). No credit needed.
- Used: `rayan-headshot-white-bg-469x600.jpeg` → `inputs/rayan-headshot-cutout.png`
- Tried, not used: `rayan-emaar-quarterly-broker-awards-2025-960x1280.jpeg`, cropped chest-up above the plaque so that no Emaar logo or award text is included → `inputs/rayan-awards-cutout.png`

## Video frame (alternative background)
A frame from Rayan's own Al Maryah video. No credit needed.

## Fonts
Playfair Display and Inter: SIL Open Font Licence (licence files in `../fonts/`).

## Tools
- Background removal: `@imgly/background-removal-node` 1.4.5 (AGPL-3.0, free/open source, run locally; the model is bundled, so no uploads)
- FFmpeg 6.1.1 (frame grabs), Playwright/Chromium (render)
