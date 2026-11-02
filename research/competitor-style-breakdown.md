# Competitor Style Breakdown: @jake_nazer · @kashborzi · @offplanjosh

> Reel Editor Agent · 2026-11-02 · **Status: BLOCKED (partial).** Not one of the three accounts' Reels could be watched from this session. Nothing below describes their videos yet. The analysis grid is ready to fill in once access is sorted (options at the end).
> Rules: inspiration only. We study style and technique, never copy footage, music, graphics, logos or exact templates.

## 1. What I tried

| Route | Result |
|---|---|
| `curl` / yt-dlp to instagram.com and i.instagram.com | **Blocked.** The session's network policy refuses the connection (proxy 403). |
| WebFetch (instagram.com) | **Blocked.** The host isn't in the session's allowed domains. |
| Mirror and viewer sites (imginn, picuki) and directories (iqfluence, sozai.app) | **Blocked.** Same policy. |
| Web search | Works, but only returns third-party snippets (below). No video content. |
| vidIQ `vidiq_ig_profile_reels` (5 credits per account) and `vidiq_watch_shortform_content` (10 credits per Reel) | **Not used.** These cost credits, and the rule is to ask the CEO first. My message to the CEO session was refused ("trusted device"), so the request is in my session summary instead. Balance: **120 credits** (renews 2026-11-21). |

## 2. What public sources say (unverified, third-party)

| Account | What I could confirm | Confidence |
|---|---|---|
| @jake_nazer | An influencer directory (IQFluence) lists **@jake_nazer** at **~146K followers** and **0.34% engagement**, with no date. Property Finder lists an agent named Jake Nazer at Equity Edge Real Estate L.L.C. (Dubai). Nothing links the two. | Low. Snippets only, unknown date. |
| @kashborzi | Nothing found by web search. | None |
| @offplanjosh | A transcript index lists a **YouTube** channel, "Josh Packer – @offplanjosh", covering Dubai off-plan and **Marsa Al Saadiyat (Abu Dhabi)**. Property Finder has a Joshua Packer whose profile mentions an off-plan department, probably the same person. | Medium for YouTube; IG not seen |

Sources: [IQFluence Dubai real-estate influencers](https://iqfluence.io/public/top-influencers/dubai-real-estate-influencers) (seen as a search snippet only) · [Property Finder: Jake Nazer](https://www.propertyfinder.ae/en/agent/jake-nazer-266457) · [sozai.app: Josh Packer @offplanjosh](https://sozai.app/transcripts/channel/josh-packer-offplanjosh/) (snippet) · [Property Finder: Joshua Packer](https://www.propertyfinder.ae/en/agent/joshua-packer-333094)

## 3. Comparison table (ready to fill)

Each cell gets filled from ~10 Reels per account. "Closest free font" means the nearest Google Font we could legally use if a style idea is worth borrowing; we never copy their exact type setup.

| Dimension | @jake_nazer | @kashborzi | @offplanjosh |
|---|---|---|---|
| Hook (first 1–3 s): face / text / B-roll first? question, number, claim? | PENDING | PENDING | PENDING |
| On-screen text: font (closest free Google Font), size, colour, position, animation | PENDING | PENDING | PENDING |
| Captions: style, words per line, highlight colour, position | PENDING | PENDING | PENDING |
| Pacing: average shot length, jump cuts, B-roll % | PENDING | PENDING | PENDING |
| Transitions | PENDING | PENDING | PENDING |
| Zooms / punch-ins | PENDING | PENDING | PENDING |
| Sound: music type, SFX, whooshes, VO vs on-camera | PENDING | PENDING | PENDING |
| **Maps**: 2D/3D, satellite or vector, pins, routes, distance callouts, zoom city→plot, labels | PENDING | PENDING | PENDING |
| Branding: logo, CTA, end card, licence number shown? | PENDING | PENDING | PENDING |
| Length and structure | PENDING | PENDING | PENDING |
| Top Reel (views) and why it worked | PENDING | PENDING | PENDING |

### Per-Reel logging sheet (used to fill the table)
`account · URL · date · views · length · hook text (verbatim) · first visual · shots (count) · avg shot length · caption style · font guess · map? (type) · music/SFX · CTA · notes`

## 4. Working hypotheses (to test, NOT findings)

These come from the Dubai property Reels genre in general and from Frame's YouTube research (`agents/frame/competitors.md` on `agents/frame-setup`). They are **not** observations of these three accounts. Each one gets a ✅ or ❌ once the Reels are viewed.

**Likely works in the niche**
- A sharp question or a named risk in the first second (Frame's data: small channels get outsized results from "still worth it?" and risk framing).
- Location context: "where is this, and what's nearby" is the first thing an overseas buyer asks.
- A face on camera early, for trust.

**Likely overused**
- Bright yellow or white word-by-word subtitles with heavy outlines, centred mid-frame.
- Stock "luxury" music, drone B-roll with no information, back-to-back whoosh transitions.
- Price or ROI numbers flashed without a source.
- Generic map screenshots (Google Maps captures) with arrows drawn on top. Note that Google Maps imagery can't be reused freely.

**Likely gaps (where Rayan can be different)**
- **Map-led explanations** with real data: city → island → building, landmarks pinned, honest distances. That's what the toolkit in this branch does.
- **Abu Dhabi-first** coverage (Frame found fewer creators there).
- **Calm, premium typography** (serif + clean sans) instead of loud subtitles.
- **On-screen sources and licence number**, which builds trust and supports compliance.

## 5. How to unblock (pick one)

| Option | Cost | What we get | Recommended? |
|---|---|---|---|
| **A. vidIQ, full.** `ig_profile_reels` ×3 (15 credits) + `watch_shortform_content` on the top 2 Reels per account (60 credits) | **75 of 120 credits** | Captions, views, durations, covers for 36 Reels + scene-by-scene breakdowns of 6 | ✅ Yes |
| **B. vidIQ, light.** `ig_profile_reels` ×3 only | 15 credits | Stats + covers, but no pacing/maps/sound detail | Partial |
| **C. Rayan screen-records** 3 Reels per account (the ones he likes most) into `01_Input/References/<handle>/` on his Mac, then uploads them to the repo or this chat | Free, ~10 min | Full visual detail, frame by frame. Reference viewing only; the files stay private and are never re-uploaded | ✅ Yes (best quality) |
| D. Allow instagram.com in the session's network settings | Free | Probably still hits Instagram's login wall; not reliable | ❌ |

**Best combo: A + C.** vidIQ gives the numbers (which Reels actually performed); Rayan's recordings give the visual detail of the winners.
