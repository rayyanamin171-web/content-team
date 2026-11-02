#!/usr/bin/env bash
# Generates the reel's sound effects from scratch with FFmpeg (synthesised noise and tones).
# Nothing is sampled from anyone else, so they're ours to use with no licence issues.
set -euo pipefail
cd "$(dirname "$0")/sfx"
A="-ar 48000 -ac 2"
# whoosh: filtered pink noise with a fast swell (transitions)
ffmpeg -loglevel error -y -f lavfi -i "anoisesrc=d=0.7:c=pink:a=0.9" -af "highpass=f=250,lowpass=f=5200,afade=t=in:d=0.38:curve=exp,afade=t=out:st=0.38:d=0.32:curve=qsin,aecho=0.6:0.4:40:0.25,volume=0.55" $A whoosh.wav
# soft whoosh for map moves
ffmpeg -loglevel error -y -f lavfi -i "anoisesrc=d=1.4:c=brown:a=0.9" -af "highpass=f=120,lowpass=f=1800,afade=t=in:d=0.8:curve=qsin,afade=t=out:st=0.8:d=0.6:curve=qsin,volume=0.9" $A swoosh-long.wav
# tick: short bright tone with fast decay (pins, labels)
ffmpeg -loglevel error -y -f lavfi -i "aevalsrc='0.5*sin(2*PI*1760*t)*exp(-38*t)+0.25*sin(2*PI*2640*t)*exp(-55*t)':d=0.35:s=48000" -af "volume=0.7" $A tick.wav
# hit: low sub thump + noise transient (hook text slam)
ffmpeg -loglevel error -y -f lavfi -i "aevalsrc='0.9*sin(2*PI*(52+40*exp(-18*t))*t)*exp(-5.5*t)':d=0.9:s=48000" -f lavfi -i "anoisesrc=d=0.12:c=white:a=0.4" -filter_complex "[1]afade=t=out:d=0.12,highpass=f=2000[n];[0][n]amix=inputs=2:normalize=0,volume=0.9" $A hit.wav
# riser: rising filtered tone into the end card
ffmpeg -loglevel error -y -f lavfi -i "aevalsrc='0.35*sin(2*PI*(180+260*t*t)*t)*(t/1.2)':d=1.2:s=48000" -af "afade=t=out:st=1.05:d=0.15,volume=0.6" $A riser.wav
ls -la
