# Abu Dhabi Series: Reel Cover Template (Part 1, Al Maryah Island)

> Frame · 2026-11-02 · Status: **DRAFT for Rayan.** Built free (HTML → PNG). No vidIQ credits used. Nothing uploaded.

## Files
| File | What |
|---|---|
| `ig-cover-part1-a-1080x1920.png` | **Recommended.** Full-bleed photo, gold series label top, big serif island name bottom |
| `ig-cover-part1-b-1080x1920.png` | Variant B: adds a large outlined "01" as the series marker, no tagline |
| `ig-cover-part1-c-1080x1920.png` | Variant C: photo top, solid navy panel bottom. The most consistent grid, and it works with any photo |
| `template.html` | Source. One file for all 7 parts |
| `render.js` | Renders the template to PNG |
| `fonts/` | Playfair Display + Inter (SIL Open Font Licence, files included) |

## The photo is a placeholder
The skyline in these PNGs is drawn shapes, marked **PHOTO PLACEHOLDER**. It isn't a real photo and it doesn't show any real building. No licensed photo was reachable from this session, and we don't use competitor or copyrighted images.

**Photo to drop in (from Rayan's own footage):** Al Maryah skyline **from the water or across the channel (e.g. from Al Reem)** at **blue hour**, with the towers lit and some sky left above them. Vertical 9:16, at least 1080×1920. The towers should sit in the **middle third**, because the top and bottom are darkened for text. A drone shot or a phone shot on a tripod both work. A frame from the Reel's own hook shot (skyline at blue hour) is ideal.

Save it as `photos/al-maryah.jpg` in this folder, then run:
```
node render.js --part 1 --island "Al Maryah Island" --img photos/al-maryah.jpg --layout a --out ig-cover-part1-a-1080x1920.png
```

## Parts 2–7
Only three things change: `--part`, `--island` and `--img`. Example:
```
node render.js --part 2 --island "Saadiyat Island" --img photos/saadiyat.jpg --out ig-cover-part2-a-1080x1920.png
```
Use the **same layout letter for every part** so the profile grid reads as one series. Add `--safe 1` to see the 1080×1350 safe area outlined.

## Design
- **Layout:** 1080×1920. The gold label "ABU DHABI SERIES – PART 1" sits at the top of the safe area with a short gold rule under it. "Al Maryah / Island" is set in two large lines at the bottom of the safe area, with an optional 3-word tagline "Abu Dhabi, honestly." (Atlas's series sign-off) under it. Navy gradients darken the top and bottom of the photo so the text reads. Everything is inside the centre 1080×1350, so the profile-grid crop keeps it. Nothing sits in the top 250 px or bottom 350 px where Instagram's UI covers the image.
- **Colours:** navy `#0E1A2B`, gold `#C8A15A`, off-white `#F5F1E8` (provisional palette until Rayan's brand colours arrive).
- **Fonts:** Playfair Display Bold 168 px for the island name (Atlas's series style calls for a big clean serif), Inter SemiBold for the label and tagline.
- **Rules followed:** no facts or numbers, no logos, no competitor imagery, extra text ≤ 3 words.

## Checks
- [x] Required text present: "Abu Dhabi Series – Part 1", "Al Maryah Island"
- [x] Legible in the profile-grid crop at 216×270 px
- [x] Template tested with another island (Part 4, Saadiyat)
- [ ] Real photo (pending Rayan's footage)

## Flag for Rayan / Atlas
Atlas's original plan numbered Al Maryah as island 5 ("Island 4 of 6"). This cover says **Part 1**, as the brief asked, since Maryah was posted first (2026-10-29). Please confirm the order of Parts 2–7 so the numbering stays consistent.
