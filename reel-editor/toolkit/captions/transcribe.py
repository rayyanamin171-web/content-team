#!/usr/bin/env python3
"""Word timings for captions.

Two ways in:
  1. Audio/video file -> faster-whisper (free, local, open source) with word timestamps.
     Install on the Mac once:  pip3 install faster-whisper   (first run downloads the model from Hugging Face)
     The cloud session can't download models (Hugging Face is blocked there), so use option 2 in the cloud.
  2. An .srt or .vtt file -> words spread across each subtitle's time by character length.

Output: JSON list [{"id": "w0", "text": "This", "start": 0.12, "end": 0.31}, ...]

  python3 transcribe.py 01_Input/footage/al-maryah.mp4 --out words.json [--model small.en]
  python3 transcribe.py 01_Input/transcripts/demo.srt --out words.json
Always read the result before using it: whisper can invent words over silence or music.
"""
import argparse, json, re, sys


def ts(s):
    s = s.strip().replace(",", ".")
    parts = s.split(":")
    if len(parts) == 2:
        parts = ["0"] + parts
    h, m, sec = parts
    return int(h) * 3600 + int(m) * 60 + float(sec)


def from_subtitles(path):
    text = open(path, encoding="utf-8-sig").read().replace("\r", "")
    words = []
    for block in re.split(r"\n\s*\n", text):
        m = re.search(r"(\d[\d:.,]*)\s*-->\s*(\d[\d:.,]*)", block)
        if not m:
            continue
        a, b = ts(m.group(1)), ts(m.group(2))
        lines = block[m.end():].strip().splitlines()
        body = " ".join(l.strip() for l in lines if l.strip())
        body = re.sub(r"<[^>]+>", "", body)
        toks = body.split()
        if not toks:
            continue
        weights = [len(t) + 2 for t in toks]
        total, acc = sum(weights), a
        for t, wgt in zip(toks, weights):
            d = (b - a) * wgt / total
            words.append({"text": t, "start": round(acc, 3), "end": round(acc + d, 3)})
            acc += d
    return words


def from_media(path, model):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper is not installed. On the Mac: pip3 install faster-whisper. Or pass an .srt file instead.")
    m = WhisperModel(model, device="auto", compute_type="int8")
    segs, _ = m.transcribe(path, word_timestamps=True, vad_filter=True, language="en" if model.endswith(".en") else None)
    words = []
    for s in segs:
        for w in s.words or []:
            t = w.word.strip()
            if t and not set(t) <= set("♪�"):
                words.append({"text": t, "start": round(w.start, 3), "end": round(w.end, 3)})
    return words


def get_words(path, model="small.en"):
    words = from_subtitles(path) if path.lower().endswith((".srt", ".vtt")) else from_media(path, model)
    for i, w in enumerate(words):
        w["id"] = f"w{i}"
    return words


def to_srt(words, path, max_words=4):
    """Write grouped words back out as an SRT (handy for IG's own caption upload)."""
    def f(t):
        h, r = divmod(t, 3600); m, s = divmod(r, 60)
        return f"{int(h):02}:{int(m):02}:{s:06.3f}".replace(".", ",")
    out, i = [], 0
    for n, g in enumerate(group_words(words, max_words), 1):
        out.append(f"{n}\n{f(g['start'])} --> {f(g['end'])}\n{' '.join(w['text'] for w in g['words'])}\n")
    open(path, "w").write("\n".join(out))


def group_words(words, max_words=4, gap=0.15):
    """Caption groups: break at sentence end, a pause >= 150 ms, or the word limit."""
    groups, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        end_sentence = re.search(r"[.!?]$", w["text"])
        pause = nxt is not None and nxt["start"] - w["end"] >= gap
        if len(cur) >= max_words or end_sentence or pause or nxt is None:
            groups.append({"start": cur[0]["start"], "end": cur[-1]["end"], "words": cur})
            cur = []
    # hold each group until the next starts (max +0.4 s) so captions don't flicker
    for a, b in zip(groups, groups[1:]):
        a["end"] = round(min(b["start"], a["end"] + 0.4), 3)
    if groups:
        groups[-1]["end"] = round(groups[-1]["end"] + 0.3, 3)
    return groups


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="small.en")
    ap.add_argument("--srt", help="also write grouped captions as SRT")
    a = ap.parse_args()
    ws = get_words(a.src, a.model)
    json.dump(ws, open(a.out, "w"), indent=1)
    if a.srt:
        to_srt(ws, a.srt)
    print(f"{len(ws)} words -> {a.out}")
