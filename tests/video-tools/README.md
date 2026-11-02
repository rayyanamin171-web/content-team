# Video Tools: Smoke Test

> Frame · 2026-11-02 · Rayan's decision: **free tools only.** HyperFrames (open source) + FFmpeg. **Remotion is not used** (it needs a paid company licence above 3 people).

## Versions (installed in the Claude cloud container)
| Tool | Version | How |
|---|---|---|
| FFmpeg | 6.1.1 (preinstalled) | `ffmpeg -version` |
| HyperFrames CLI | 0.9.2 | `npm i -g hyperframes` |
| yt-dlp | 2026.10.26 | `pip3 install --user --break-system-packages yt-dlp`, with `~/.local/bin` on PATH. **Rayan's own videos or reference viewing only. Never re-post others' content.** |
| Remotion | not installed | skipped by Rayan's decision |

Cloud containers are reset between sessions, so a new session has to reinstall these. A repo setup script could do that if it becomes routine.

## Result
`hyperframes-smoke.mp4`: **render worked.** 5.0 s, 1080×1920, H.264, 30 fps, 334 KB, rendered in about 10 s. It's an "Abu Dhabi Series – Part 1 / Al Maryah Island" title card in the Reel cover's palette and fonts. `hyperframes check` passed (layout, motion, and WCAG AA contrast on 9/9 text checks).

Source: `hyperframes-smoke/index.html`. To re-render: `cd hyperframes-smoke && hyperframes render -o ../hyperframes-smoke.mp4`

## Notes
- **Network:** this session blocks `cdn.jsdelivr.net`, so the first render failed when it tried to load GSAP from the CDN. The fix was to vendor GSAP 3.15.0 locally (`vendor/gsap.min.js`, from npm, under GSAP's free "no charge" standard licence). Do the same in future compositions.
- **First frame = cover:** HyperFrames warns when frame 0 is empty, because social players use it as the thumbnail. The series label is on screen from 0 s.
- **Do not use** `hyperframes publish` (it uploads to HeyGen's hosting) or `hyperframes billing`. Render locally only. Nothing gets posted anywhere without Rayan's approval.
