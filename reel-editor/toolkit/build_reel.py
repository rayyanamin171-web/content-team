#!/usr/bin/env python3
"""One command: raw vertical clip + config  ->  finished 1080x1920 Reel.

  python3 toolkit/build_reel.py configs/al-maryah-part1.json            (run from reel-editor/)
  python3 toolkit/build_reel.py configs/al-maryah-part1.json --preview   (fast draft render)
  python3 toolkit/build_reel.py configs/al-maryah-part1.json --no-render (build the HyperFrames project only)

What it does
  1. Normalises the footage to 1080x1920 / 30 fps (or makes a labelled placeholder if there's none yet).
  2. Renders each map scene with the offline map module (cached; re-renders only when the scene changes).
  3. Turns the transcript (SRT now; faster-whisper on the Mac) into timed caption groups.
  4. Writes a HyperFrames project (hook, map, footage, lower third, captions, transitions, end card, sound effects).
  5. Runs `hyperframes check`, then `hyperframes render` -> 02_Output/<id>/<id>.mp4 (+ cover frame + contact sheet).
Never uploads or posts anything.
"""
import argparse, hashlib, html, json, os, re, shutil, subprocess, sys

TK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TK)  # reel-editor/
sys.path.insert(0, os.path.join(TK, "captions"))
from transcribe import get_words, group_words  # noqa: E402

FPS = 30
# one Studio lane per sound type so sounds never stack on one track
SFX_TRACK = {"whoosh": 20, "tick": 21, "riser": 22, "hit": 23, "swoosh-long": 24}
SFX_MAX = {"tick": 0.25}


def run(cmd, **kw):
    print("  $", " ".join(str(c) for c in cmd)[:220])
    r = subprocess.run(cmd, **kw)
    if r.returncode != 0:
        sys.exit(f"command failed ({r.returncode}): {cmd[0]}")
    return r


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
                          "-of", "json", path], capture_output=True, text=True).stdout
    d = json.loads(out)
    return float(d["format"]["duration"]), any(s["codec_type"] == "audio" for s in d.get("streams", []))


def fontface(brand):
    css = []
    for key in ("serif", "sans"):
        f = brand["fonts"][key]
        for w, file in f["files"].items():
            style = "italic" if w.endswith("i") else "normal"
            css.append(f'@font-face {{ font-family: "{f["family"]}"; src: url("assets/fonts/{file}") format("woff2"); '
                       f'font-weight: {w.rstrip("i")}; font-style: {style}; }}')
    return "\n    ".join(css)


def fill(template, **kv):
    s = open(os.path.join(TK, "overlays", template)).read()
    for k, v in kv.items():
        s = s.replace("{{" + k + "}}", str(v))
    left = re.findall(r"\{\{[A-Z_]+\}\}", s)
    if left:
        sys.exit(f"{template}: unfilled {left}")
    return s


# ---------------------------------------------------------------- footage
def prepare_footage(cfg, need, build):
    dst = os.path.join(build, "assets", "footage.mp4")
    src = cfg.get("footage")
    if src and os.path.exists(os.path.join(ROOT, src)):
        src = os.path.join(ROOT, src)
        print(f"footage: {src}")
        # cover-crop to 9:16, 30 fps, keyframe every second (smooth seeking), keep audio
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf",
             "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p",
             "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", dst])
        return dst, probe(dst)[1], False
    label = cfg.get("placeholder_label", "Rayan's footage goes here")
    print(f"footage: none found at {src!r} -> making a labelled placeholder ({need:.1f}s)")
    font = os.path.join(TK, "fonts", "Inter-Placeholder.ttf")
    fontopt = f":fontfile={font}" if os.path.exists(font) else ":font=Inter"
    txt = lambda t, y, size, col="0xF5F1E8": (f"drawtext=text='{t}'{fontopt}:fontsize={size}:fontcolor={col}:"
                                            f"x=(w-text_w)/2:y={y}")
    vf = ",".join([
        "format=yuv420p",
        txt("PLACEHOLDER FOOTAGE", 1380, 64, "0xC8A15A"),
        txt(label.replace("'", ""), 1470, 38),
        txt("%{eif\\:t\\:d}.%{eif\\:mod(t*10\\,10)\\:d}s", 1540, 34, "0xF5F1E8@0.6"),
    ])
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
         f"gradients=s=1080x1920:d={need + 1}:r=30:c0=0x0E1A2B:c1=0x22355A:c2=0x7A5A48:c3=0x2F6F73:nb_colors=4:speed=0.012:type=linear",
         "-vf", vf, "-c:v", "libx264", "-crf", "20", "-g", "30", "-pix_fmt", "yuv420p", dst])
    return dst, False, True


# ---------------------------------------------------------------- map
def render_map(scene_rel, build, idx, args):
    scene_path = os.path.join(ROOT, scene_rel)
    scene = json.load(open(scene_path))
    h = hashlib.sha1()
    for p in (scene_path, os.path.join(TK, "map", "map.html")):
        h.update(open(p, "rb").read())
    cache = os.path.join(TK, "map", "cache", f"{h.hexdigest()[:12]}.mp4")
    if not os.path.exists(cache):
        print(f"map: rendering {scene_rel} (slow on CPU-only machines; cached afterwards)")
        run(["node", os.path.join(TK, "map", "render_map.mjs"), "--scene", scene_path, "--out", cache,
             "--workers", str(args.workers)])
    else:
        print(f"map: cached {cache}")
    dst = os.path.join(build, "assets", f"map{idx}.mp4")
    shutil.copy(cache, dst)
    return dst, scene


# ---------------------------------------------------------------- build
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--preview", action="store_true", help="draft-quality render")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    cfg_path = os.path.abspath(args.config)
    cfg = json.load(open(cfg_path))
    brand = json.load(open(os.path.join(TK, "brand.json")))
    B = brand["colors"]
    rid = cfg["id"]
    out_dir = os.path.join(ROOT, "02_Output", rid)
    build = os.path.join(out_dir, "build")
    shutil.rmtree(build, ignore_errors=True)
    for d in ("assets/fonts", "assets/sfx", "assets/vendor", "compositions"):
        os.makedirs(os.path.join(build, d), exist_ok=True)
    for f in os.listdir(os.path.join(TK, "fonts")):
        shutil.copy(os.path.join(TK, "fonts", f), os.path.join(build, "assets", "fonts"))
    for f in os.listdir(os.path.join(TK, "audio", "sfx")):
        shutil.copy(os.path.join(TK, "audio", "sfx", f), os.path.join(build, "assets", "sfx"))
    shutil.copy(os.path.join(TK, "vendor", "gsap.min.js"), os.path.join(build, "assets", "vendor"))
    FF = fontface(brand)

    # ---- timeline: absolute start of every segment
    segs, t = [], 0.0
    for i, s in enumerate(cfg["timeline"]):
        s = dict(s, idx=i)
        if s["type"] == "map":
            s["dur"] = json.load(open(os.path.join(ROOT, s["scene"])))["duration"]
        s["start"] = round(t, 3)
        t += s["dur"]
        segs.append(s)
    total = round(t, 3)
    foot_need = max([s.get("in", 0) + s["dur"] for s in segs if s["type"] == "footage"] + [1])
    foot, foot_audio, placeholder = prepare_footage(cfg, foot_need, build)

    body, audio, tweens = [], [], []
    z = 1
    # footage segments (one source, trimmed per segment)
    for s in segs:
        if s["type"] != "footage":
            continue
        snd = 'data-has-audio="true"' if foot_audio else "muted"
        body.append(f'      <video id="foot{s["idx"]}" class="clip" src="assets/footage.mp4" playsinline {snd} '
                    f'data-start="{s["start"]}" data-duration="{s["dur"]}" data-media-start="{s.get("in", 0)}" '
                    f'data-track-index="1" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;z-index:{z}"></video>')
        # punch-ins: scale the wrapper (never the timed video)
        for k, (pt, sc) in enumerate(s.get("punch", [])):
            at = s["start"] + pt
            if k == 0:
                tweens.append(f'tl.set("#footwrap", {{ scale: {sc} }}, {at:.3f});')
            else:
                prev = s["punch"][k - 1]
                d = max(0.001, pt - prev[0])
                ease = "power2.inOut" if d > 0.2 else "none"
                tweens.append(f'tl.fromTo("#footwrap", {{ scale: {prev[1]} }}, {{ scale: {sc}, duration: {d:.3f}, ease: "{ease}" }}, {s["start"] + prev[0]:.3f});')
    foot_html = "\n".join(body)
    body = [f'    <div id="footwrap" data-layout-ignore style="position:absolute;inset:0;transform-origin:50% 42%;z-index:1">\n{foot_html}\n    </div>']

    # map segments
    pins_sfx = []
    for s in segs:
        if s["type"] != "map":
            continue
        _, scene = render_map(s["scene"], build, s["idx"], args)
        body.append(f'    <video id="map{s["idx"]}" class="clip" src="assets/map{s["idx"]}.mp4" muted playsinline '
                    f'data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="2" '
                    f'style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:3"></video>')
        for p in scene.get("pins", []):
            pins_sfx.append(("tick", s["start"] + p["t"][0] + 0.05, 0.35))
        for c in scene.get("callouts", []):
            pins_sfx.append(("tick", s["start"] + c["t"][0] + c.get("draw", 1.1), 0.35))
        pins_sfx.append(("swoosh-long", s["start"] + 1.0, 0.5))
        pins_sfx.append(("swoosh-long", s["start"] + 3.0, 0.45))

    # ---- scenes
    hosts = []

    def host(sid, start, dur, kind="graphics", zi=10):
        hosts.append(f'    <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-kind="{kind}" data-width="1080" data-height="1920" '
                     f'style="z-index:{zi}"></div>')

    hk = cfg.get("hook")
    if hk:
        dur = hk.get("dur", segs[0]["dur"])
        parts = re.split(r"(\*[^*]+\*)", hk["text"])
        words, hl_index, n = [], None, 0
        for part in parts:
            hl = part.startswith("*")
            for w in part.strip("*").split():
                if hl and hl_index is None:
                    hl_index = n
                words.append(f'<span class="w{" hl" if hl else ""}">{html.escape(w)}</span>')
                n += 1
        stagger = 0.09
        open(os.path.join(build, "compositions", "hook.html"), "w").write(fill(
            "hook.html", FONTFACE=FF, GOLD=B["gold"], PAPER=B["paper"], TOP=hk.get("top", 300), SIZE=hk.get("size", 108),
            KICKER=html.escape(hk.get("kicker", "")), WORDS=" ".join(words), STAGGER=stagger,
            HL_AT=round(0.04 + (hl_index or 0) * stagger + 0.25, 3), DUR=dur))
        host("hook", 0, dur, zi=12)
        audio.append(("hit", 0.03, 0.8))

    lt = cfg.get("lower_third")
    if lt:
        open(os.path.join(build, "compositions", "lowerthird.html"), "w").write(fill(
            "lowerthird.html", FONTFACE=FF, GOLD=B["gold"], PAPER=B["paper"], GLASS=B["navy_glass"], TOP=lt.get("top", 960),
            NAME=html.escape(lt.get("name", brand["name"])), LINE=html.escape(lt.get("line", brand["licence_line"])), DUR=lt["dur"]))
        host("lowerthird", lt["start"], lt["dur"], zi=13)

    cap = cfg.get("captions")
    if cap:
        words = get_words(os.path.join(ROOT, cap["src"]), cap.get("model", "small.en"))
        if cap.get("time_base", "reel") == "footage":  # map source-time words onto the edit
            mapped = []
            for s in segs:
                if s["type"] != "footage":
                    continue
                a, b = s.get("in", 0), s.get("in", 0) + s["dur"]
                for w in words:
                    if a <= w["start"] < b:
                        mapped.append(dict(w, start=round(w["start"] - a + s["start"], 3), end=round(min(w["end"], b) - a + s["start"], 3)))
            words = mapped
        groups = group_words(words, cap.get("max_words", 4))
        gh, gj = [], []
        for gi, g in enumerate(groups):
            spans = []
            gw = []
            for w in g["words"]:
                wid = f"cw{gi}_{len(gw)}"
                spans.append(f'<span class="cw" id="{wid}">{html.escape(w["text"])}</span>')
                gw.append({"id": wid, "start": w["start"], "end": w["end"]})
            gs, ge = max(0.1, g["start"] - 0.05), g["end"]
            gh.append(f'    <div id="cg{gi}" class="cg clip" data-start="{gs:.3f}" data-duration="{ge - gs:.3f}"><div class="cg-pill">{"".join(spans)}</div></div>')
            gj.append({"id": f"cg{gi}", "start": round(gs, 3), "end": round(ge, 3), "words": gw})
        open(os.path.join(build, "compositions", "captions.html"), "w").write(fill(
            "captions.html", FONTFACE=FF, GOLD=B["gold"], PAPER=B["paper"], TOP=cap.get("top", 1170), SIZE=cap.get("size", 60),
            GROUPS="\n".join(gh), GROUP_JSON=json.dumps(gj)))
        host("captions", 0, total, kind="captions", zi=14)

    ec = next((s for s in segs if s["type"] == "endcard"), None)
    if ec:
        e = cfg.get("end_card", {})
        meta = e.get("meta", f'{brand["licence_line"]} · {brand["handle"]}')
        open(os.path.join(build, "compositions", "endcard.html"), "w").write(fill(
            "endcard.html", FONTFACE=FF, GOLD=B["gold"], PAPER=B["paper"], NAVY=B["navy"],
            KICKER=html.escape(e.get("kicker", "")), TITLE=html.escape(e.get("title", "")), CTA=html.escape(e.get("cta", "")),
            CTA_SUB=html.escape(e.get("cta_sub", "")), NAME=html.escape(brand["name"]), META=html.escape(meta)))
        host("endcard", ec["start"], ec["dur"], zi=11)
        audio.append(("riser", ec["start"] - 1.05, 0.5))

    # ---- transitions: navy/gold wipe across every change of segment type
    for a, b in zip(segs, segs[1:]):
        cut = b["start"]
        tweens.append(f'tl.set("#wipe", {{ y: 1920 }}, {cut - 0.32:.3f});')
        tweens.append(f'tl.to("#wipe", {{ y: -3900, duration: 0.62, ease: "power2.inOut" }}, {cut - 0.31:.3f});')
        audio.append(("whoosh", cut - 0.3, 0.7))
    audio += pins_sfx if cfg.get("sfx", True) else []

    aud_html = []
    for i, (name, at, vol) in enumerate(sorted(audio, key=lambda x: x[1])):
        at = max(0.0, at)
        d, _ = probe(os.path.join(TK, "audio", "sfx", f"{name}.wav"))
        d = min(d, total - at, SFX_MAX.get(name, 9))
        if d <= 0.05:
            continue
        aud_html.append(f'    <audio id="sfx{i}" class="clip" src="assets/sfx/{name}.wav" data-start="{at:.3f}" data-duration="{d:.3f}" data-volume="{vol}" data-track-index="{SFX_TRACK.get(name, 20)}"></audio>')
    mus = cfg.get("music")
    if mus and os.path.exists(os.path.join(ROOT, mus["src"])):
        shutil.copy(os.path.join(ROOT, mus["src"]), os.path.join(build, "assets", "music" + os.path.splitext(mus["src"])[1]))
        aud_html.append(f'    <audio id="music" class="clip" src="assets/music{os.path.splitext(mus["src"])[1]}" data-start="0" data-duration="{total}" '
                        f'data-volume="{mus.get("volume", 0.22)}" data-fade-out="0.8" data-track-index="21"></audio>')

    index = f"""<!doctype html>
<!-- Generated by toolkit/build_reel.py from {os.path.relpath(cfg_path, ROOT)}. Edit the config, not this file. -->
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1080, height=1920" />
  <script src="assets/vendor/gsap.min.js"></script>
  <style>
    {FF}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {B["navy"]}; }}
    #bg {{ position: absolute; inset: 0; background: {B["navy"]}; }}
    #wipe {{ position: absolute; left: 0; top: 0; width: 1080px; height: 3840px; z-index: 30;
      background: linear-gradient(180deg, {B["gold"]} 0, {B["gold"]} 10px, {B["navy"]} 10px, {B["navy"]} calc(100% - 10px), {B["gold"]} calc(100% - 10px)); }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
    <div id="bg" data-layout-ignore></div>
{chr(10).join(body)}
{chr(10).join(hosts)}
    <div id="wipe" data-layout-ignore></div>
{chr(10).join(aud_html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.set("#wipe", {{ y: 1920 }}, 0);
    {chr(10).join("    " + x for x in tweens).strip()}
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
"""
    open(os.path.join(build, "index.html"), "w").write(index)
    json.dump({"id": rid, "name": rid}, open(os.path.join(build, "meta.json"), "w"))
    json.dump({"paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
               "media": {"autoProxy": False}}, open(os.path.join(build, "hyperframes.json"), "w"), indent=1)
    print(f"built HyperFrames project: {build}  ({total}s, {len(segs)} segments{', PLACEHOLDER footage' if placeholder else ''})")

    chk = subprocess.run(["hyperframes", "check", build, "--json"], capture_output=True, text=True)
    open(os.path.join(out_dir, "check.json"), "w").write(chk.stdout)
    try:
        cj = json.loads(chk.stdout)
        print(f"hyperframes check: {cj.get('summary') or {k: cj[k] for k in cj if k in ('ok', 'errors', 'warnings')}}")
    except Exception:
        print("hyperframes check output saved to check.json")
    if args.no_render:
        return
    out = os.path.join(out_dir, f"{rid}{'-preview' if args.preview else ''}.mp4")
    run(["hyperframes", "render", build, "-o", out, "-q", "draft" if args.preview else "delivery", "--fps", str(FPS)])
    if foot_audio:  # Instagram plays around -14 LUFS; bring speech up to that, peaks capped at -1 dBTP
        tmp = out.replace(".mp4", ".tmp.mp4")
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1:LRA=11",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", tmp])
        os.replace(tmp, out)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-frames:v", "1", os.path.join(out_dir, "cover-frame0.png")])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-vf", "fps=2,scale=216:384,tile=10x3", "-frames:v", "1",
         os.path.join(out_dir, "contact-sheet.jpg")])
    print(f"done: {out}")


if __name__ == "__main__":
    main()
