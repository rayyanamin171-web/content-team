# Rayan Maniya: Reel Style Guide ("Calm Authority")

> Reel Editor Agent · 2026-11-02 · v1. Builds on Frame's "Abu Dhabi Series" covers (`thumbnails/2026-11-02-al-maryah-reel/` on `agents/frame-setup`).
> **Provisional:** the competitor research is blocked (see `research/competitor-style-breakdown.md`). The "gaps" this guide aims at are hypotheses until we've watched their Reels. The look itself doesn't depend on them.
> Every preset below already exists as code in `reel-editor/toolkit/`. Change `toolkit/brand.json` once and every Reel follows.

## The idea in one line
**The calm expert with the map.** Where other agents shout prices over stock drone shots, Rayan *shows you where it is*, what's around it, and what's true. The style is premium and quiet, and it's built on real geography.

Three signatures that make a Rayan Reel recognisable with the sound off:
1. **The fly-in:** UAE → emirate → island in 3D, gold outline, pins. Every location Reel has one.
2. **Navy + gold + serif:** Playfair headlines over navy glass, never yellow subtitles.
3. **Receipts on screen:** licence number, data credits, "straight line" or "source:" under any number.

## 1. Brand kit

| Token | Value | Use |
|---|---|---|
| Navy | `#0E1A2B` | backgrounds, glass cards (78% opacity), map sea |
| Gold | `#C8A15A` | kickers, rules, active caption word, pins, one highlighted word per title |
| Off-white | `#F5F1E8` | all main text |
| Serif | **Playfair Display** 700 (SIL OFL, free) | hook lines, island names, name in the lower third |
| Sans | **Inter** 500–800 (SIL OFL, free) | kickers, captions, labels, CTA |

No other fonts, and no more than one gold word per title. Font files and licences: `reel-editor/toolkit/fonts/`.

## 2. Safe zones (1080×1920)

```
 y=0    ┌──────────────────────────────┐
        │  IG status / header: no text  │
 y=168  ├──────────────────────────────┤
        │                         │    │
        │   ALL TEXT LIVES HERE   │ no │  ← right 150 px: IG like/comment/share rail
        │   x 64 … 930            │text│     (lower half): no text there
        │                         │    │
 y=1330 ├──────────────────────────────┤
        │  IG caption, handle, audio:   │
        │  texture only, never text     │
 y=1920 └──────────────────────────────┘
```
Key text also sits inside the centre 1080×1350 (y 285–1635), so the 4:5 grid crop keeps it, matching Frame's covers.

## 3. Hook formula (0–2 s)

**Frame 0 is the thumbnail and the hook.** It's never black and never a logo.

`[gold kicker: series + part]` + `[one serif line, max ~7 words, one gold word]` + `[a face or a striking shot behind it]`

| Hook type (from LEARNINGS) | Pattern | Example (no unverified facts) |
|---|---|---|
| Question | Where / why / is it…? | "Where does Abu Dhabi **do business?**" |
| Insider | The thing buyers miss | "The island most visitors **drive past.**" |
| Mistake | Name the risk | "The **service charge** nobody mentions." |
| Number | Only with a verified number + source line | "AED 60bn [VERIFY]" → **not until verified** |

- Words light up 90 ms apart (the line is already readable on frame 0), with one small scale pop on the gold word. Then the title holds **dead still**.
- One "hit" SFX on frame 0. The hook exits by blurring out at ~2 s, into the first wipe.

## 4. Text animation presets

| Preset | Look | Motion | File |
|---|---|---|---|
| **Hook Title** | Gold Inter 600 kicker, 32 px, 7 px tracking, caps · gold rule · Playfair 700 108 px | Rule draws (0.5 s, expo.out), words go from 38% to full ink, gold word pops 1.06×, blur-out exit 0.2 s | `overlays/hook.html` |
| **Lower Third** | Navy glass box, 6 px gold left bar · "Rayan Maniya" Playfair 58 px · "RERA BRN 68958" Inter 600 30 px gold caps | Slides in 40 px (0.45 s), name blurs in, line fades; exit 0.25 s | `overlays/lowerthird.html` |
| **Captions** | Inter 700 60 px, off-white on a navy pill (74%), **active word gold** | Pill pops in (0.16 s), words turn gold as spoken, hard kill at end | `overlays/captions.html` |
| **Map Pin** | Gold pin with a navy dot and a navy card (gold edge), Inter 600 42 px + caps sub | Drops with overshoot (0.55 s), one ring pulse, card slides in | `map/map.html` |
| **Main Pin** | Same, Playfair 60 px, card centred above the pin | — | `map/map.html` |
| **Distance Callout** | Dashed gold line drawing A→B, off-white card "≈ 3.6 km / STRAIGHT LINE" | Line draws (0.8 s), card pops with back-ease | `map/map.html` |
| **End Card** | Navy, kicker, Playfair 128 px place name, gold CTA block, name + licence + handle | Staggered reveal within 0.7 s, then holds | `overlays/endcard.html` |
| **Wipe** | Full-frame navy panel with gold edges sweeping up | 0.62 s, power2.inOut, with a whoosh | `build_reel.py` |

Rules: titles land and then stay still (no floating or breathing). Exits are ~40% shorter than entrances. Nothing readable under 28 px.

## 5. Captions
- Always on when anyone speaks (most people watch muted).
- 3–5 words per group (calm pace). Break on sentence ends and pauses. One group on screen at a time.
- Position: centred, top of the pill at y≈1170 (bottom of the safe band). Never over the face; move up (`captions.top`) if the framing needs it.
- Sentence case, the speaker's own words, correct spelling of places (Al Maryah, Saadiyat, ADGM).
- Source: faster-whisper on the Mac (word-accurate) or an SRT. Always proofread.

## 6. Cut rhythm

| Beat | Shots | Rule |
|---|---|---|
| Hook | 1 shot, 1.5–2.2 s | face or hero shot + Hook Title |
| Map fly-in | 6–9 s, one continuous move | the "where", then the pins (one beat each) |
| Talking / VO + B-roll | shots of **1.5–3 s** | B-roll cut on the sentence, never mid-word |
| Honest part | 1 longer shot on camera (3–5 s) | no music swell, no effects: this is the trust beat |
| CTA / end card | 2–3 s | exactly one CTA |

- **Punch-ins:** 1.00 → 1.08–1.10 scale on the key word (a hard cut-in, not a slow creep). Max one per 4 s.
- **Jump cuts:** remove breaths and "umm"s inside talking shots. Fine, but they must be clean.
- **B-roll ratio:** 40–60% for VO Reels, 20–30% for to-camera Reels.
- **Transitions:** the navy/gold **wipe only between chapters** (footage ↔ map ↔ end card). Hard cuts inside a chapter. No spins, glitches or flashes.
- **Length:** let the idea decide. 15–30 s for one-point Reels, 45–70 s for the island explainers (Atlas's scripts).

## 7. Sound
- **Voice first.** Final mix at **−14 LUFS**, peaks ≤ −1 dBTP (`build_reel.py` normalises automatically when there's voice).
- **Music:** calm, minimal, low (≈ −20 dB under the voice). Use **Instagram's in-app music library** when posting (licensed for IG), or a track Rayan has a licence for. Never rip music from other creators.
- **SFX (ours, synthesised in `toolkit/audio/`):** *hit* on the hook, *whoosh* on wipes, *tick* on each pin, *swoosh* on big map moves, *riser* into the end card. Subtle: if you notice them, they're too loud.

## 8. Map look: "satellite to blueprint"
1. **Country:** stylised vector UAE (Natural Earth), emirate outlined in gold, big serif "UAE".
2. **City:** real **Sentinel-2 satellite** (10 m), graded down toward navy, with feathered edges.
3. **Island:** cross-fade to a **navy blueprint**: OSM roads in faint gold, surrounding buildings in navy, **the island's own towers rising in warm off-white 3D**, island outline glowing gold.
4. **Pins:** one main pin (island), then max 3 landmark pins, one beat each.
5. **Context:** pull back with a **distance callout** to a famous landmark.

Data rules (non-negotiable):
- Only licensed open data: OpenStreetMap via Overture (ODbL), Natural Earth (public domain), Copernicus Sentinel-2 (free, credit required). **The credit line is always on screen** during map shots (generated automatically).
- **Distances:** only straight-line distances computed from coordinates, labelled "STRAIGHT LINE". **Drive times only when verified** (e.g. timed by Rayan, or from a cited source); otherwise leave them out. Never Google Maps screenshots.
- Landmark positions come from OSM/Overture with their source kept. No invented POIs.

## 9. Lower third
"**Rayan Maniya**" / "**RERA BRN 68958**". Shown once per Reel, 2–3 s, the first time Rayan is on camera after the hook. Left-aligned at y≈960, above the captions.

> **[COMPLIANCE CHECK]** RERA BRN is Dubai's broker registration. For Abu Dhabi projects, ask the brokerage whether an Abu Dhabi licence or permit reference (ADREC / DARI) must also be shown, and whether specific-project ads need a permit number (Dubai: Trakheesi). Add it to `licence_line` in `brand.json` if so.

## 10. CTA and end card
- One CTA per Reel (LEARNINGS rule): usually "Comment **WORD**" tied to a lead magnet that exists (e.g. MARYAH → branded-residence checklist).
- End card: series kicker, place name, gold CTA block, one line of benefit, "Rayan Maniya · RERA BRN 68958 · @rayyanmaniya". Hold at least 2 s.

## 11. Do / Don't

| Do | Don't |
|---|---|
| Put the hook line on frame 0 | Open on a logo, black frame or slow drone |
| Use one gold word per title | Highlight every other word, or use yellow/green subtitles |
| Show where it is (map) before what it costs | Flash prices or ROI without a source line |
| Keep numbers to verified facts + a source line | Round up, extrapolate or "up to" numbers |
| Keep text inside y 168–1330 | Put text under the IG UI or the right rail |
| Credit map data on screen | Use Google/Apple Maps screenshots or others' footage |
| Let titles land and hold | Float, pulse or slowly zoom text |
| Use calm music, low | Use trending "luxury" stock music over the voice |
| One CTA | Stack "follow + comment + DM + link in bio" |
| Free/OFL fonts only | Paid fonts, or copying a competitor's template |

## 12. Checklist before a Reel goes to Rayan
- [ ] Every number is verified, with a source line or caption source; ⚠️ items are removed or verified
- [ ] Frame 0 reads as the hook (check `cover-frame0.png`)
- [ ] `hyperframes check` passes (the build runs it; see `check.json`)
- [ ] Captions proofread; place names spelled right
- [ ] Map credit visible on every map shot
- [ ] Lower third + licence line present; compliance check done for the emirate
- [ ] One CTA, and the lead magnet exists
- [ ] Loudness ≈ −14 LUFS; music licensed (or added in IG at upload)
- [ ] Nothing posted: Rayan uploads himself
