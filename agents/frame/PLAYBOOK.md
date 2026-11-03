# Frame Playbook: Thumbnails & Covers Operating Manual

> Version 1 · 2026-11-02 · Owner: Frame
> Rules from `LEARNINGS.md` override anything here.

---

## 1. Competitor Research

### Who counts as a competitor
- YouTube and Instagram creators covering **Dubai or Abu Dhabi property** for investors: agents, brokers, advisors, developers' channels and investor-vloggers
- Priority: **Abu Dhabi, branded residences and luxury/off-plan** first, then broader Dubai investment channels
- Include a few **adjacent premium-style channels** (wealth or lifestyle creators with the calm, cinematic look we want), for style only

### How to find them
**With vidIQ (preferred). Costs are per call, so log them in the research log below.**
| Need | Tool | Cost |
|---|---|---|
| Our tracked competitors | `vidiq_list_competitors` (channel UCZqcGRP-DhtaWYUJ9qsfL_Q) | 0 |
| Credits left | `vidiq_balance` | 0 |
| Find channels by niche/country | `vidiq_channel_search` (country AE, language en) | 5 |
| Channels like a known one | `vidiq_similar_channels` | 5 |
| Videos beating their channel average | `vidiq_outliers` (keyword or channelIds) | 5 |
| A channel's top videos | `vidiq_channel_videos` (popular=true) | 5 |
| How common a visual idea is | `vidiq_similar_thumbnails` (description or videoId) | 5 |
| Channel stats | `vidiq_channel_stats` / `vidiq_get_channels_by_ids` | 5 |
| Instagram outliers | `vidiq_instagram_tiktok_outlier_search`, `vidiq_ig_profile_reels` | check before use |

**Without vidIQ:** web search for "[area] real estate YouTube", YouTube search sorted by views, and creator lists (Heepsy, Modash). Check view counts by hand against the channel's recent average.

**Budget:** a research pass is normally ≤ 8 calls (~40 credits). Anything bigger goes to the CEO Agent first. Never call generation tools during research.

**Known limit (2026-11-02):** this cloud session can't load `i.ytimg.com`, so thumbnail images can't be viewed directly here. Patterns are inferred from titles, outlier scores and vidIQ feedback until the domain is allowed in the environment's network settings or Rayan shares screenshots.

### What to log in `competitors.md` (swipe file)
For each channel: name and handle, subs, market focus, top-performing videos (title, views, **breakout = views ÷ channel's typical views**), thumbnail pattern notes, **why it works**, and what we'd do differently.

**Inspiration only.** Log patterns in words. Never download into the repo, trace, or reuse a competitor's image, face, layout file, logo or brand colours.

### Cadence
- Before each YouTube video: a quick pass on 5–10 outliers for that topic
- Monthly: refresh the competitor table and the pattern scoreboard

---

## 2. Pattern Library

Each concept is tagged with one pattern.

### Layouts
| Code | Layout | When it fits | Our premium version |
|---|---|---|---|
| **L1 Face + Building** | Rayan on one third, hero building or skyline on two thirds | Area/project explainers | Calm expression, golden hour, building we filmed |
| **L2 Before / After** | Left vs right over time (2019 vs 2026, render vs reality) | Growth, handover, "what changed" | Thin divider, same angle both sides, dates verified |
| **L3 Map Pin** | Aerial or stylised map with 1 glowing pin or outline | "Where to buy", islands, location | Satellite or drone base, gold pin, island name ≤2 words |
| **L4 Split Screen / Versus** | Two (max three) options side by side | Comparisons: brand vs brand, Dubai vs Abu Dhabi | Equal halves, one subtle "winner" glow, question mark |
| **L5 Big Number** | One verified number dominates | Data videos | Only Market-Research-verified numbers, with the unit (AED, %, sqft) |
| **L6 Luxury Close-up** | Tight detail: lobby, marble, view from a balcony, a key | Branded residences, lifestyle | Shallow depth of field, warm light, 2–3 words |
| **L7 Question Card** | A short question over a moody hero image | "Is it worth it?", "Still a good time?" | Text in a clean block, Rayan small or absent |

### Text rules
- **≤ 4 words**, ideally 2–3. Never repeat the title; the thumbnail asks, the title answers.
- **Huge:** cap height ≥ 12% of thumbnail height (≥ 86 px on 1280×720).
- **High contrast:** white or off-white on dark, or ink on light; ≥ 4.5:1. Use a soft shadow or a solid panel if the background is busy.
- One weight (heavy), one font, sentence case or caps (be consistent). A question mark is fine. Exclamation marks are banned.
- Keep text out of the **bottom-right** corner (YouTube timestamp) and the edges (≥ 5% margin).
- Numbers only if verified, with their unit.

### Colour and lighting
- **Provisional palette** until Rayan's brand kit arrives [ASK RAYAN]:
  - Ink navy `#0E1A2B` (backgrounds, panels)
  - Warm gold `#C8A15A` (one accent: underline, pin, glow)
  - Off-white `#F5F1E8` (text)
  - Sea teal `#2F6F73` (Abu Dhabi water, secondary only)
- Golden hour or blue hour. Lift shadows on faces. Warm highlights, cooler backgrounds for separation.
- Saturation slightly up, never neon. One accent colour per thumbnail.

### Emotion and face direction
- Allowed: calm confidence, slight smile, serious/thoughtful, raised eyebrow (curious), looking at the subject (guides the eye).
- Banned: shock face, open-mouth surprise, pointing at money, fake crying.
- Eyes in the upper third. Face big enough that the eyes are visible at 160 px (face ≥ 25% of frame height).
- The face looks toward the text or subject, never out of frame.

### Branding placement
- Consistent position: Rayan on the **right third** by default (text left), so the series becomes recognisable.
- Optional small tag "RAYAN MANIYA" or logo top-left at ≤ 4% height [ASK RAYAN]. Never bottom-right.
- No third-party hotel or developer logos.

### Mobile legibility test (every concept)
1. Export at 1280×720, then view at **320×180 and 160×90**.
2. Can you read the text in 1 second? Can you tell what the subject is? Is the face's expression clear?
3. Greyscale check: does the text still stand out?
4. Feed check: put it next to 5 competitor thumbnails from the same search. Does it stand out without shouting?

---

## 3. Brief Intake

### Getting Rayan's files (Files & Media Agent, iMac master folder)
- **Reach it:** `send_message` to `session_01KFxVAgqaKGQJw71ooc69JR`. Start with **"FILES REQUEST from Frame"**, then give **Action**, **Path(s)** and **Output**. It replies by cross-session message; I can't answer on that channel, so every request is a new `send_message`. Full rules are in `Team/FOLDER_PROTOCOL.md` on the Mac.
- **Actions:** LIST · READ · SAVE · FRAMES (stills from Rayan's footage at timestamps or every N seconds → `02_Output/Content/Frames/`) · INFO (resolution, duration) · COMPRESS / CONVERT / TRIM (ffmpeg 6.0) · TRANSCRIBE · PULL (fetch my finished thumbnails from the GitHub repo into `02_Output/Content/Thumbnails/`).
- **My area on the Mac:** `02_Output/Content/Thumbnails/`. File names there: `YYYY-MM-DD_topic_frame.ext`. **`01_Input` is Rayan's only:** read, never write.
- **Images can't travel by message.** Ask it to describe frames, give exact paths and metadata, or commit the stills to the repo (e.g. `inputs/<date>-<topic>/`) so I can `git pull` them.
- **Typical flow for a video background:** INFO on the video → FRAMES every 2 s (or at the timestamps I name) → ask for the best 3–5 to be committed to `inputs/` → I render the cover → it can PULL the finished cover to `02_Output/Content/Thumbnails/`.
- Moving files around on Rayan's Mac is internal. Publishing or uploading anywhere still needs Rayan's yes via the CEO Agent.


What I need from Atlas or Rayan for each video (copy into `brief.md`):
```
VIDEO:            title (final + backup) · platform · publish date
SCRIPT:           path in scripts/
PROMISE:          the one thing the viewer gets (one sentence)
HOOK:             first line of the cold open
EMOTION:          curiosity | reassurance | caution | aspiration
FACTS FOR IMAGE:  numbers/claims allowed on the image + verification status
NAMED PROJECTS:   any? → [COMPLIANCE CHECK], no logos
ASSETS:           face photos, footage stills, drone shots (paths + rights)
MUST AVOID:       anything Rayan doesn't want shown
DEADLINE:
```
If PROMISE or ASSETS are missing, I ask before designing. Without assets, I deliver specs + mock-ups with placeholders.

---

## 4. Production

### Per video
- **3 concepts**, each with a different pattern code, plus:
- **A/B variant** of the strongest: change **one thing only** (text, or face expression, or background). YouTube's "Test & Compare" accepts up to 3 thumbnails per video.

### Specs
| Asset | Size | Ratio | Notes |
|---|---|---|---|
| YouTube thumbnail | 1280×720 | 16:9 | JPG or PNG, **< 2 MB**, sRGB |
| Instagram Reel cover | 1080×1920 | 9:16 | Keep all key content in the centre **1080×1350** (4:5) safe area, which the profile grid crops to. Avoid top 250 px and bottom 350 px (UI). |
| Instagram feed post / cover | 1080×1350 | 4:5 | |
| YouTube Shorts cover | 1080×1920 | 9:16 | Same safe-area rules as Reels |

### Tools
- **vidIQ (if connected):** `vidiq_score_thumbnail` (5 credits) for a second opinion on finished thumbnails; `vidiq_generate_thumbnail` (22 credits) and `vidiq_refine_thumbnail` **only with Rayan's approval** via the CEO Agent.
- **Otherwise:** a written design spec + an SVG/HTML mock-up (placeholder imagery, real text and layout), rendered to PNG with the local headless browser for the size tests.
- Final compositing from Rayan's real photos in any editor (Canva, Photoshop, Figma). The spec has to be precise enough that anyone can build it.

### File naming and folders
```
thumbnails/
  2026-11-02-maryah-branded-residences/
    brief.md                    concepts, specs, QA, flags
    yt-concept-a.svg            mock-up
    yt-concept-a-1280.png       render (when available)
    yt-concept-a-160.png        small-size test
    yt-final-a.jpg              final, after approval
    ig-cover-a-1080x1920.jpg
```
Pattern: `<platform>-<concept|final>-<letter>[-<size>].<ext>`. Use lowercase and hyphens.

---

## 5. QA Checklist (every deliverable)
- [ ] Reads at 160×90 (text, subject, face)
- [ ] ≤ 4 words, doesn't repeat the title, no exclamation mark
- [ ] Every number/claim verified by Market Research or supplied by Rayan (source noted)
- [ ] No competitor assets, logos or recognisable layouts; no third-party trademarks
- [ ] All images are ours or licensed (licence noted in brief.md)
- [ ] Brand-consistent: palette, font, face position
- [ ] Contrast ≥ 4.5:1 and passes the greyscale test
- [ ] No "SOLD OUT", "guaranteed", fake scarcity or price claims; nothing that promises returns (team SOUL.md compliance)
- [ ] Named project? → [COMPLIANCE CHECK] flagged for Rayan
- [ ] Specs right (size, < 2 MB, safe areas for Reels)
- [ ] The video pays off the thumbnail's promise (check with Atlas)

---

## 6. Review & Approval Flow
1. Frame saves the drafts in `thumbnails/<date>-<slug>/` on a branch.
2. Frame sends a short summary to the **CEO Agent**: concepts, recommendation, flags, any credits spent or needed.
3. The CEO Agent takes it to **Rayan**. Rayan picks, edits or rejects.
4. Frame builds the final from real assets and runs QA again.
5. **Uploading or setting a thumbnail is done by Rayan, or by an agent only after his explicit yes** for that specific thumbnail.
6. **Credits:** any step that costs vidIQ credits is flagged first with its cost. Generation needs approval every time. Research spends are logged.
7. Merging to `main` is Rayan's call.

---

## 7. Learning Loop
- **After 7 days and 28 days live:** log impressions, CTR, views, and average view duration (from YouTube Studio, vidIQ `vidiq_user_videos` / `vidiq_video_stats`, or Supermetrics), plus the A/B winner if tested.
- Record them in the scoreboard below and in the video's `brief.md`.
- A pattern that wins twice becomes a rule in `LEARNINGS.md` (`YYYY-MM-DD · frame · RULE · (why)`). A pattern that loses twice gets demoted.
- Rayan's feedback ("too busy", "love the face") becomes a rule the same day.

### Pattern scoreboard
| Date | Video | Pattern | Variant | Impr. | CTR | Views (28d) | Verdict |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
