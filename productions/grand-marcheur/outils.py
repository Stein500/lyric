#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Amorce les outils Python locaux, HORS Git.

Le sandbox peut purger .tools/ entre deux tours : on réinstalle à la demande.
Aucun binaire ni paquet n'est ajouté au dépôt (.gitignore : .tools/).
"""
import os
import sys

TOOLS = "/home/user/lyric/.tools"


def _ensure(package, marker):
    if os.path.isdir(os.path.join(TOOLS, marker)):
        return
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir",
                           "--disable-pip-version-check", "--target", TOOLS, package],
                          stdout=subprocess.DEVNULL)


_ensure("Pillow", "PIL")
sys.path.insert(0, TOOLS)


def ffmpeg_exe():
    """Retourne (chemin ffmpeg, version) ; installe imageio-ffmpeg si besoin."""
    _ensure("imageio-ffmpeg", "imageio_ffmpeg")
    sys.path.insert(0, TOOLS)
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe(), imageio_ffmpeg.get_ffmpeg_version()
