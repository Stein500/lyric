# 🎬 Vidéo — « I'm not afraid » (Daïsky × TechStein)

Clip lyrics complet **3:35 — 1920×1080 (h264 + AAC stéréo)**, univers « I'm Not Dying » (phénix aux couleurs du Bénin, flammes, fond noir, typographie brush).

> Le fichier est **découpé en 4 parties** (`.part00` → `.part03`) car GitHub refuse les fichiers uniques de plus de 100 Mo.
> Réassemble les parties pour reconstituer le MP4 d'origine.

---

## 1. Réassembler le MP4

Télécharge les **4 parties** (même dossier), puis :

**Linux / macOS :**
```bash
cat im-not-afraid.mp4.part00 im-not-afraid.mp4.part01 im-not-afraid.mp4.part02 im-not-afraid.mp4.part03 > im-not-afraid.mp4
```

**Windows (Invite de commandes `cmd`) :**
```cmd
copy /b im-not-afraid.mp4.part00 + im-not-afraid.mp4.part01 + im-not-afraid.mp4.part02 + im-not-afraid.mp4.part03 im-not-afraid.mp4
```

**Windows (PowerShell) :**
```powershell
Get-Content im-not-afraid.mp4.part00, im-not-afraid.mp4.part01, im-not-afraid.mp4.part02, im-not-afraid.mp4.part03 -Raw | Set-Content -NoNewline im-not-afraid.mp4
```

---

## 2. Vérifier l'intégrité

**Linux / macOS :**
```bash
sha256sum -c SHA256SUMS
```

Le fichier réassemblé doit avoir ce SHA-256 :

```
e1f7b1a31fcd12f9bc961dae6ea356f3b3dc5395d2cd70dac2947bccec63beb4  im-not-afraid.mp4
```

---

## Fichiers

| Fichier | Taille | Rôle |
|---|---|---|
| `im-not-afraid.mp4.part00` | 45 Mo | partie 1/4 |
| `im-not-afraid.mp4.part01` | 45 Mo | partie 2/4 |
| `im-not-afraid.mp4.part02` | 45 Mo | partie 3/4 |
| `im-not-afraid.mp4.part03` | 28 Mo | partie 4/4 |
| `SHA256SUMS` | — | empreintes des 4 parties |

Total après réassemblage : **~162 Mo** (`im-not-afraid.mp4`).
