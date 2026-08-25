from __future__ import annotations

import textwrap
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BilingualCue:
    start: float
    end: float
    original: str
    french: Optional[str]
    style: str
    section: str


STYLE_FR_MAP = {
    "IntroSerif": "IntroSerifFr",
    "VerseMono": "VerseMonoFr",
    "VerseSans": "VerseSansFr",
    "RefrainGold": "RefrainGoldFr",
    "FinalRefrainGold": "FinalRefrainGoldFr",
    "BridgeSerifCenter": "BridgeSerifCenterFr",
    "HookGold": "HookGoldFr",
    "OutroSerif": "OutroSerifFr",
}


def wrap_text(text: str, width: int) -> str:
    parts = textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False)
    if not parts:
        return text
    if len(parts) <= 2:
        return "\\N".join(parts)
    first = " ".join(parts[: len(parts) // 2])
    second = " ".join(parts[len(parts) // 2 :])
    return f"{first}\\N{second}"


def build_ass_text(cue: BilingualCue, width_main: int, width_fr: int) -> str:
    main = wrap_text(cue.original, width_main)
    if cue.french:
        fr = wrap_text(cue.french, width_fr)
        return f"{main}\\N{{\\r{STYLE_FR_MAP[cue.style]}}}{fr}"
    return main


def get_bilingual_cues() -> List[BilingualCue]:
    return [
        BilingualCue(0.00, 2.20, "Wolof TechStein beat wê!", None, "HookGold", "intro"),
        BilingualCue(2.40, 13.60, "Non vivi o - o nvi gboon mavomavo.", "L'amour d'une mère - c'est la lumière éternelle.", "IntroSerif", "intro"),
        BilingualCue(14.00, 17.00, "Hwenu e mon non ji gbonton o ji", "Le jour où tu m'as tenu dans tes bras", "VerseMono", "verse1"),
        BilingualCue(17.00, 20.00, "Before the world could call my name", "Avant que le monde ne prononce mon nom", "VerseMono", "verse1"),
        BilingualCue(20.00, 23.90, "Le jour où tu m'as tenu dans tes bras", None, "VerseMono", "verse1"),
        BilingualCue(23.90, 27.90, "You already knew my soul", "Tu connaissais déjà mon âme", "VerseMono", "verse1"),
        BilingualCue(27.90, 31.00, "Azoon lon bo - wo a toln kpo", "Toutes les nuits - tu as veillé", "VerseMono", "verse1"),
        BilingualCue(31.00, 35.00, "Every storm, you stood in the rain", "Dans chaque tempête, tu es restée sous la pluie", "VerseMono", "verse1"),
        BilingualCue(35.00, 37.00, "Toutes les nuits - tu as veillé", None, "VerseMono", "verse1"),
        BilingualCue(37.00, 41.90, "So I could stay warm, so I could remain", "Pour que je reste au chaud, pour que je reste en vie", "VerseMono", "verse1"),
        BilingualCue(41.90, 45.00, "Non vivi o - a non da nu mi", "Ton amour - tu me l'as donné", "VerseMono", "verse1"),
        BilingualCue(45.00, 48.00, "Ton amour - tu me l'as donné", None, "VerseMono", "verse1"),
        BilingualCue(48.00, 52.00, "No words can hold what you gave", "Aucun mot ne peut contenir ce que tu as donné", "VerseMono", "verse1"),
        BilingualCue(52.00, 54.00, "A love too wide, too deep for the grave", "Un amour trop vaste, trop profond pour la tombe", "VerseMono", "verse1"),
        BilingualCue(54.00, 58.00, "Mama tche - you are my one", "Ma mère - tu es mon unique", "RefrainGold", "refrain1"),
        BilingualCue(58.00, 62.00, "Mama tche - my only sun", "Ma mère - mon seul soleil", "RefrainGold", "refrain1"),
        BilingualCue(62.00, 65.00, "Gboon ce o - tu es ma vie", "Ma mère unique - tu es ma vie", "RefrainGold", "refrain1"),
        BilingualCue(65.00, 68.00, "Ma mère unique - forever with me", "Ma mère unique - pour toujours avec moi", "RefrainGold", "refrain1"),
        BilingualCue(68.00, 72.00, "Even if the sky forgets my name", "Même si le ciel oublie mon nom", "RefrainGold", "refrain1"),
        BilingualCue(72.00, 76.00, "Even if I'm lost, you guide my way", "Même si je suis perdu, tu guides mon chemin", "RefrainGold", "refrain1"),
        BilingualCue(76.00, 80.00, "Mama tche - mi non no fi", "Ma mère - je t'entends dire", "RefrainGold", "refrain1"),
        BilingualCue(80.00, 86.00, "I hear you say - I'm here, I'll stay", "Je t'entends dire - je suis là, je resterai", "RefrainGold", "refrain1"),
        BilingualCue(86.00, 87.60, "Wolof TechStein beat wê!", None, "HookGold", "hook_break"),
        BilingualCue(87.60, 90.00, "Hwenu e a yi - nyi ma se o", "Le jour où tu es partie - je n'entendais plus", "VerseSans", "verse2"),
        BilingualCue(90.00, 94.00, "The silence you left was a kind of sound", "Le silence que tu as laissé était comme un son", "VerseSans", "verse2"),
        BilingualCue(94.00, 97.00, "Le jour où tu es partie - je n'entendais pas", None, "VerseSans", "verse2"),
        BilingualCue(97.00, 101.00, "Like a bell that rings with no one around", "Comme une cloche qui sonne, sans personne autour", "VerseSans", "verse2"),
        BilingualCue(101.00, 104.00, "Non e a do mi - o non no nyi mon", "Ce que tu m'as laissé - vit encore en moi", "VerseSans", "verse2"),
        BilingualCue(104.00, 107.80, "In every choice, in every step I take", "Dans chaque choix, dans chaque pas que je fais", "VerseSans", "verse2"),
        BilingualCue(107.80, 111.00, "Ce que tu m'as laissé - vit encore en moi", None, "VerseSans", "verse2"),
        BilingualCue(111.00, 115.00, "I carry your heart - it will never break", "Je porte ton cœur - il ne se brisera jamais", "VerseSans", "verse2"),
        BilingualCue(115.00, 118.00, "Non vivi o - o ku kpoonon", "Ton amour - il ne meurt jamais", "VerseSans", "verse2"),
        BilingualCue(118.00, 122.00, "Ton amour - il ne meurt jamais", None, "VerseSans", "verse2"),
        BilingualCue(122.00, 125.00, "Death could not take what you gave", "La mort n'a pas pu reprendre ce que tu as donné", "VerseSans", "verse2"),
        BilingualCue(125.00, 128.00, "A flame still burning beyond the grave", "Une flamme brûle encore au-delà de la tombe", "VerseSans", "verse2"),
        BilingualCue(128.00, 131.00, "Mama tche - you are my one", "Ma mère - tu es mon unique", "RefrainGold", "refrain2"),
        BilingualCue(131.00, 135.00, "Mama tche - my only sun", "Ma mère - mon seul soleil", "RefrainGold", "refrain2"),
        BilingualCue(135.00, 138.00, "Gboon ce o - tu es ma vie", "Ma mère unique - tu es ma vie", "RefrainGold", "refrain2"),
        BilingualCue(138.00, 142.00, "Ma mère unique - forever with me", "Ma mère unique - pour toujours avec moi", "RefrainGold", "refrain2"),
        BilingualCue(142.00, 145.00, "Even if the sky forgets my name", "Même si le ciel oublie mon nom", "RefrainGold", "refrain2"),
        BilingualCue(145.00, 149.00, "Even if I'm lost, you guide my way", "Même si je suis perdu, tu guides mon chemin", "RefrainGold", "refrain2"),
        BilingualCue(149.00, 153.80, "Mama tche - mi non no fi", "Ma mère - je t'entends dire", "RefrainGold", "refrain2"),
        BilingualCue(153.80, 160.00, "I hear you say - I'm here, I'll stay", "Je t'entends dire - je suis là, je resterai", "RefrainGold", "refrain2"),
        BilingualCue(160.00, 162.00, "Mama...", None, "BridgeSerifCenter", "bridge"),
        BilingualCue(162.00, 164.00, "A non no nyi sisi mon.", "Tu vis dans mon souffle.", "BridgeSerifCenter", "bridge"),
        BilingualCue(164.00, 167.00, "Tu vis dans mon souffle.", None, "BridgeSerifCenter", "bridge"),
        BilingualCue(167.00, 170.00, "You never left.", "Tu n'es jamais partie.", "BridgeSerifCenter", "bridge"),
        BilingualCue(170.00, 174.00, "Mon e nyi non - o nyi jon mawu.", "Celle qui est mère - est un don du ciel.", "BridgeSerifCenter", "bridge"),
        BilingualCue(174.00, 181.00, "Celle qui est mère - est un don du ciel.", None, "BridgeSerifCenter", "bridge"),
        BilingualCue(181.00, 185.00, "MAMA TCHE - you are my one", "MA MÈRE - tu es mon unique", "FinalRefrainGold", "final_refrain"),
        BilingualCue(185.00, 189.00, "MAMA TCHE - my only sun", "MA MÈRE - mon seul soleil", "FinalRefrainGold", "final_refrain"),
        BilingualCue(189.00, 192.00, "Gboon ce o - tu es ma vie", "Ma mère unique - tu es ma vie", "FinalRefrainGold", "final_refrain"),
        BilingualCue(192.00, 195.90, "Ma mère unique - forever with me", "Ma mère unique - pour toujours avec moi", "FinalRefrainGold", "final_refrain"),
        BilingualCue(195.90, 199.00, "A yi - koonon non vivi o no fi", "Tu es partie - mais l'amour reste ici", "FinalRefrainGold", "final_refrain"),
        BilingualCue(199.00, 203.00, "Tu es partie - mais l'amour reste ici", None, "FinalRefrainGold", "final_refrain"),
        BilingualCue(203.00, 210.00, "Every morning your voice still finds me", "Chaque matin, ta voix me retrouve encore", "FinalRefrainGold", "final_refrain"),
        BilingualCue(210.00, 216.00, "Mama tche - eternally", "Ma mère - éternellement", "FinalRefrainGold", "final_refrain"),
        BilingualCue(216.00, 220.00, "Wolof TechStein beat wê!", None, "HookGold", "outro_hook"),
        BilingualCue(220.00, 224.00, "Mama tche... Mama tche...", None, "HookGold", "outro_hook"),
        BilingualCue(224.00, 229.00, '"Mon e nyi non - o nyi gboon mavomavo."', '"Celle qui est mère - est lumière pour toujours."', "OutroSerif", "outro"),
        BilingualCue(229.00, 234.00, '"Celle qui est mère - est lumière pour toujours."', None, "OutroSerif", "outro"),
    ]
