# Morse from Lyoko — Challenge CTF

Challenge de stéganographie audio où les participants doivent isoler une voie cachée dans un fichier stéréo, décoder un signal morse, puis convertir le résultat hexadécimal pour obtenir le flag.

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Fichiers du challenge](#fichiers-du-challenge)
3. [Générer le challenge](#générer-le-challenge)
4. [Ce qui est donné aux participants](#ce-qui-est-donné-aux-participants)
5. [Vérifier le challenge](#vérifier-le-challenge)
6. [Hints progressifs](#hints-progressifs)
7. [Contacts](#contacts)

---

## Vue d'ensemble

Le participant reçoit un fichier audio stéréo `challenge.wav`. À l'écoute, on entend presque exclusivement le générique 8-bit de **Code Lyoko**. Cependant, le canal droit contient en réalité un signal de **code morse**, rendu quasi-inaudible par son gain très faible (1 %).

Le morse encode une chaîne **hexadécimale** ; une fois décodée en ASCII, elle donne le flag.

**Chaîne de décodage complète :**

```
challenge.wav
  └─ canal droit → morse
       └─ décodage morse → chaîne hex
                └─ décodage hex → flag
```

**Chaîne hex encodée dans le morse :**
```
4e6f747265207365756c206573706f69722065737420646520746f757420726570726f6772616d6d6572
```
→ décode en ASCII : `Notre seul espoir est de tout reprogrammer`

**Niveau estimé :** easy/medium

**Durée estimée :** 30 min – 1h30

---

## Fichiers du challenge

```
morse-ctf/
├── out.wav             ← audio morse brut (canal secret)
├── code_lyoko_8bits.mp4← générique source (non distribué)
├── merge_audio.py        ← script de génération du challenge
├── challenge.wav       ← fichier à distribuer aux participants
└── write-up/
    └── wu.md           ← write-up complet de référence
```

---

## Générer le challenge

### Prérequis

```bash
pip install scipy numpy
sudo apt install ffmpeg   # ou équivalent
```

### Regénérer challenge.wav

```bash
python3 merge_audio.py
```

Le script :
1. Extrait et resample le générique en mono 44 100 Hz
2. Resample `out.wav` (le morse) en 44 100 Hz
3. Normalise le morse puis l'atténue à **1 % du volume** (gain = 0.01)
4. Produit un WAV stéréo : **gauche = générique**, **droite = morse**

### Modifier le flag / le message encodé

Le fichier `out.wav` doit être regénéré avec le nouveau message en hex morse. Remplacer `out.wav` puis relancer `merge_audio.py`.

---

## Ce qui est donné aux participants

**Uniquement :** `challenge.wav`

> *On a intercepté une étrange transmission audio. À première écoute, rien d'anormal... mais quelque chose cloche.*

Ne rien dire sur la stéréo, le morse, ni l'hexadécimal.

---

## Vérifier le challenge

### Propriétés du WAV

```bash
python3 -c "
import wave
with wave.open('challenge.wav') as w:
    dur = w.getnframes() / w.getframerate()
    print(f'Durée : {dur:.1f}s | Canaux : {w.getnchannels()} | Fréq. : {w.getframerate()} Hz')
"
```

Valeurs attendues : ~47 s, **2 canaux (stéréo)**, 44 100 Hz.

### Vérifier la présence du morse dans le canal droit

```bash
python3 -c "
from scipy.io import wavfile
import numpy as np
_, data = wavfile.read('challenge.wav')
left, right = data[:, 0], data[:, 1]
print(f'Peak gauche  : {np.max(np.abs(left))}')
print(f'Peak droite  : {np.max(np.abs(right))}')
print(f'Ratio L/R    : {np.max(np.abs(left)) / np.max(np.abs(right)):.0f}x')
"
```

Le canal droit doit avoir un peak ~100x plus faible que le gauche — mais sa forme d'onde doit être clairement visible dans Audacity.

---

## Hints progressifs

À ne délivrer **qu'en cas de blocage prolongé**, de façon progressive.

### Hint 1 — Il y a plus qu'il n'y paraît

Le fichier est un WAV stéréo. Ouvre-le dans un logiciel audio (Audacity, Sonic Visualizer…) et regarde les **deux canaux séparément**.

### Hint 2 — Que voit-on dans le canal droit ?

Le canal droit présente une forme d'onde très caractéristique : des bouffées courtes et longues séparées par des silences. Ce motif régulier est celui d'un **code morse**.

### Hint 3 — Comment décoder le morse ?

Des outils en ligne permettent de décoder un fichier audio en morse directement :
- [morsecodetranslator](https://themorsecodetranslator.net/morse-code-audio-decoder/)

Tu peux aussi l'écouter et le retranscrire à la main (#long).

### Hint 4 — Le résultat du morse n'est pas lisible directement

Le texte obtenu après décodage morse n'est pas du texte clair — c'est une chaîne de chiffres et de lettres (a–f). C'est de **l'hexadécimal**. Utilise un convertisseur hex → ASCII (CyberChef, Python, etc.).

---

## Contacts

- Discord : Lanceløt
