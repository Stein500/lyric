# Ghost u see — lyric film 9:16

Production cut for the artist's existing master (`Ghost'u_see- Daïsky.m4a`). The visual direction is an original feature-animation look blending expressive family-film character acting with cinematic anime: a Beninese lead, with Nigerian, Afro-Latina and Haitian characters, through a clear emotional arc from loneliness and hurt to recognition and self-acceptance.

## Locked lyric mode

**B —** original lyrics burned into the image in a decorative blackletter/gothic display face; French translations of English and Spanish lines appear in a karaoke pill. French lines remain untranslated. The exact supplied lyric text is preserved. The image model is used for art only; the precise lettering is laid in by the renderer so spelling, accents, punctuation and timing remain faithful.

## Deliverables

- `../../livrables/GHOST-U-SEE-DAISKY-9x16.mp4` — 1080×1920, 30 fps, original audio, ten sequential visual beats with short cross-dissolves, moving camera crop, lyric overlay and 5-second end card.
- `../../livrables/COVER-GHOST-U-SEE-1080x1920.jpg` — dedicated TikTok cover.
- `verses_map.json` — vocal onsets copied from the supplied timed lyric sheet, French translations, scene schedule.
- `assets/` — six AI-generated, text-free scene plates and font.

## Re-render

Python dependencies: `Pillow`, `mutagen`, `imageio-ffmpeg`. The `imageio-ffmpeg` wheel provides FFmpeg with H.264, libass and loudnorm support.

```sh
python3 -m venv .venv
.venv/bin/pip install pillow mutagen imageio-ffmpeg
.venv/bin/python projects/ghost-u-see/build_map.py
.venv/bin/python projects/ghost-u-see/render.py
```

The renderer performs two-pass loudness normalization on the supplied master, pads only the 5-second visual end card, and never generates or alters the artist's vocal/music content beyond normalization.

The `UnifrakturCook` font is distributed under the SIL Open Font License; see `assets/OFL.txt`.
