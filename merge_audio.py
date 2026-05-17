#!/usr/bin/env python3
"""
CTF Challenge builder:
  Left channel  → Code Lyoko 8-bit theme (full volume)
  Right channel → Morse code (low volume, nearly inaudible in the mix)

In Audacity the two waveforms are clearly visible and extractable.
"""

import subprocess
import numpy as np
from scipy.io import wavfile
import os

WORKDIR   = os.path.dirname(os.path.abspath(__file__))
MP4_IN    = os.path.join(WORKDIR, "code_lyoko_8bits.mp4")
MORSE_IN  = os.path.join(WORKDIR, "out.wav")
MUSIC_TMP = os.path.join(WORKDIR, "_music_tmp.wav")
MORSE_TMP = os.path.join(WORKDIR, "_morse_tmp.wav")
OUT_FILE  = os.path.join(WORKDIR, "challenge.wav")

TARGET_SR = 44100
MORSE_GAIN = 0.01   # morse at 1 % → inaudible in the mix, clearly visible in Audacity

# ── 1. Extract + resample music to mono 44100 ────────────────────────────────
print("[1/4] Extracting music audio …")
subprocess.run([
    "ffmpeg", "-y", "-i", MP4_IN,
    "-vn",
    "-ar", str(TARGET_SR),
    "-ac", "1",          # mix stereo → mono so left ≠ right only because of morse
    "-sample_fmt", "s16",
    MUSIC_TMP,
], check=True, capture_output=True)

# ── 2. Resample morse to 44100 ───────────────────────────────────────────────
print("[2/4] Resampling morse …")
subprocess.run([
    "ffmpeg", "-y", "-i", MORSE_IN,
    "-ar", str(TARGET_SR),
    "-ac", "1",
    "-sample_fmt", "s16",
    MORSE_TMP,
], check=True, capture_output=True)

# ── 3. Load, align lengths, build stereo ────────────────────────────────────
print("[3/4] Building stereo file …")
_, music = wavfile.read(MUSIC_TMP)
_, morse = wavfile.read(MORSE_TMP)

music = music.astype(np.float32)
morse = morse.astype(np.float32)

# Trim music to morse length (morse is the CTF payload — keep it intact)
music = music[: len(morse)]

# Normalise morse to full scale before attenuating so the waveform is clean
peak = np.max(np.abs(morse))
if peak > 0:
    morse = morse / peak * 32767.0

# Apply gain: music full, morse quiet
left  = music
right = morse * MORSE_GAIN

# Clip to int16 range
left  = np.clip(left,  -32768, 32767).astype(np.int16)
right = np.clip(right, -32768, 32767).astype(np.int16)

stereo = np.column_stack([left, right])
wavfile.write(OUT_FILE, TARGET_SR, stereo)

# ── 4. Cleanup temp files ────────────────────────────────────────────────────
os.remove(MUSIC_TMP)
os.remove(MORSE_TMP)


