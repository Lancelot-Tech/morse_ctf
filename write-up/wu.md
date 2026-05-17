# Write-up — Morse from Lyoko

**Flag :** `HSR{Notre_seul_espoir_est_de_tout_reprogrammer}`

---

## Contexte

On reçoit un unique fichier : `challenge.wav`. À l'écoute, on entend le générique 8-bit de Code Lyoko. Rien d'autre... en apparence.

---

## Étape 1 — Analyser le fichier audio

Ouvrir `challenge.wav` dans **Audacity** (`File → Open`).

À première vue, la forme d'onde semble normale — de la musique. Mais en regardant de plus près, Audacity affiche **deux pistes séparées** : c'est un fichier **stéréo** (canal gauche + canal droit).

```
Canal gauche  ████████████████████████████  ← musique (Code Lyoko)
Canal droit   ▂▂▂▄▂▄▄▂▄▂▂▂▂▄▂▂▂▄▄▄▂▄▂▂▂▂  ← signal très faible, mais distinct
```

Le canal droit a une amplitude bien plus faible, mais sa **forme d'onde est irrégulière et structurée** — ce n'est pas du bruit.

---

## Étape 2 — Séparer et extraire le canal droit

Dans Audacity :

1. Cliquer sur le nom de la piste → `Split Stereo Track`
2. Fermer (ou muter) la piste gauche
3. Zoomer sur la piste droite

On distingue clairement des **impulsions courtes** et des **impulsions longues** séparées par des silences réguliers.

Ce motif est immédiatement reconnaissable : c'est du **code morse**.

Pour exporter uniquement le canal droit :
`File → Export → Export Selected Audio` → format WAV

---

## Étape 3 — Décoder le morse

### Option A — Décodeur audio en ligne

Plusieurs outils décodent un fichier audio morse directement :

- [morsecodetranslator](https://themorsecodetranslator.net/morse-code-audio-decoder/)
  → importer le WAV du canal droit, lancer l'analyse

- [Morse Code Adaptive Audio Decoder](https://www.dcode.fr/morse-code) (dcode.fr)

Le décodeur retourne une chaîne de caractères hexadécimaux :

```
4e6f747265207365756c206573706f69722065737420646520746f757420726570726f6772616d6d6572
```

### Option B — Décodage à l'oreille / à la main

En écoutant le canal droit après amplification (`Effect → Amplify` dans Audacity), on entend distinctement les bips courts (`.`) et longs (`-`).

Chaque groupe de symboles séparés par une pause courte forme **une lettre**, et les groupes séparés par une pause longue forment des **séquences de caractères hex**.

---

## Étape 4 — Décoder l'hexadécimal

La chaîne obtenue n'est pas du texte clair — c'est de **l'hexadécimal**. Il faut la décoder en ASCII.

### Avec CyberChef

1. Ouvrir [CyberChef](https://gchq.github.io/CyberChef/)
2. Recette : `From Hex`
3. Coller la chaîne → le résultat s'affiche

### Avec Python

```python
bytes.fromhex("4e6f747265207365756c206573706f69722065737420646520746f757420726570726f6772616d6d6572").decode()
# → 'Notre seul espoir est de tout reprogrammer'
```

### Avec CyberChef en ligne de commande

```bash
echo "4e6f747265207365756c206573706f69722065737420646520746f757420726570726f6772616d6d6572" | xxd -r -p
# → Notre seul espoir est de tout reprogrammer
```

---

## Flag

```
HSR{Notre_seul_espoir_est_de_tout_reprogrammer}
```

---

## Résumé de la chaîne de décodage

```
challenge.wav (stéréo)
  │
  ├─ Canal gauche → Code Lyoko 8-bit (leurre)
  │
  └─ Canal droit  → code morse (gain 1%, quasi-inaudible)
                        │
                        └─ décodage morse
                                │
                                └─ chaîne hexadécimale
                                        │
                                        └─ décodage hex → ASCII → flag
```
