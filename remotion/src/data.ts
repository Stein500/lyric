export type LineKind =
  | 'hook' // mots qui claquent, flash blanc
  | 'verse' // ligne monte du bas, reste
  | 'quote' // citation extérieure : italique, gris, en retrait
  | 'paren' // effet "pensée" : plus petit, en retrait, légèrement flou->net
  | 'title' // typo brush graffiti
  | 'cta' // appel à l'action avec icône
  | 'stamp' // tampon signature
  | 'bridge' // flotte / dérive, halo doré
  | 'echo' // dernier écho, fondu lent
  | 'final' // refrain final apothéose
  | 'logo'; // logo de fin

export interface LyricLine {
  start: number;
  end: number;
  main: string;
  sub?: string;
  kind: LineKind;
  emphasis?: string[]; // mots-clés mis en or
  note?: string;
  fx?: 'key' | 'crack' | 'fracture' | 'rise';
  icon?: string; // pour les CTA
  y?: number; // position verticale en % (0 = haut)
}

export interface Scene {
  id: string;
  label: string;
  start: number;
  end: number;
  lines: LyricLine[];
}

export const SCENES: Scene[] = [
  /* 1 — Intro (0:00–0:13) */
  {
    id: 'intro',
    label: 'Intro',
    start: 0,
    end: 13,
    lines: [
      { start: 4.0, end: 7.4, main: 'ABONNE-TOI — pour ne rien manquer', kind: 'cta', icon: 'bell', y: 34 },
      { start: 6.6, end: 10.0, main: 'LIKE — si le message te touche', kind: 'cta', icon: 'heart', y: 50 },
      { start: 9.0, end: 12.2, main: 'COMMENTE — ton mot ou ta phrase préférée', kind: 'cta', icon: 'comment', y: 66 },
      { start: 9.6, end: 12.9, main: "I'M NOT AFRAID", sub: 'Daïsky (prod. TechStein)', kind: 'title', y: 46 },
    ],
  },

  /* 2 — Ad-lib + mini-hook (0:13–0:34) */
  {
    id: 'adlib',
    label: 'Ad-lib + mini-hook',
    start: 13,
    end: 34,
    lines: [
      { start: 13.0, end: 20.0, main: "Yeah... I'm not afraid anymore...", sub: "Ouais... je n'ai plus peur...", kind: 'hook' },
      { start: 20.0, end: 24.0, main: 'To stand up, to break the chains', sub: 'Me relever, briser les chaînes', kind: 'hook' },
      { start: 24.0, end: 30.0, main: "I'm not afraid, I'm not afraid — To rise again, through the pain", sub: "Je n'ai pas peur, je n'ai pas peur — Renaître encore, malgré la douleur", kind: 'paren' },
    ],
  },

  /* 3 — Tag signature ×3 (0:34–0:50) */
  {
    id: 'tag1',
    label: 'Tag signature ×3',
    start: 34,
    end: 50,
    lines: [
      { start: 34.6, end: 37.2, main: 'Wolof TechStein beat wê!', kind: 'stamp', note: 'red' },
      { start: 39.4, end: 42.0, main: 'Wolof TechStein beat wê!', kind: 'stamp', note: 'gold' },
      { start: 44.2, end: 47.0, main: 'Wolof TechStein beat wê!', kind: 'stamp', note: 'green' },
    ],
  },

  /* 4 — Couplet 1 « La chute » (0:50–1:13) */
  {
    id: 'verse1',
    label: 'Couplet 1 — La chute',
    start: 50,
    end: 73,
    lines: [
      { start: 50.0, end: 52.0, main: "J'ai touché le fond, j'ai vu le vide en face", kind: 'verse' },
      { start: 52.0, end: 54.0, main: "Les doutes m'ont bouffé, j'ai perdu ma trace", kind: 'verse' },
      { start: 54.0, end: 55.5, main: "Mais dans le noir, j'ai trouvé une flamme", kind: 'verse', emphasis: ['flamme'] },
      { start: 55.5, end: 58.2, main: "Petite mais brûlante, elle a ravivé mon âme", kind: 'verse', emphasis: ['brûlante', 'âme'] },
      { start: 58.2, end: 60.0, main: "On m'a dit « t'y arriveras pas, laisse tomber »", kind: 'quote' },
      { start: 60.0, end: 64.5, main: "Mais j'ai transformé leurs mots en carburant, en vérité", kind: 'verse', emphasis: ['carburant'] },
      { start: 64.5, end: 68.0, main: "Chaque chute m'a forgé, chaque larme m'a lavé", kind: 'verse', emphasis: ['forgé'], fx: 'crack' },
      { start: 68.0, end: 73.0, main: "Maintenant je marche sur l'eau, j'ai plus peur de me noyer", kind: 'verse', emphasis: ['marche'], fx: 'rise' },
    ],
  },

  /* 5 — Pré-refrain 1 « Le sursaut » (1:13–1:29.9) */
  {
    id: 'pre1',
    label: 'Pré-refrain 1 — Le sursaut',
    start: 73,
    end: 89.9,
    lines: [
      { start: 73.0, end: 76.5, main: "I've been down, I've been low", sub: "J'ai touché le fond, j'étais si bas", kind: 'hook', emphasis: ['down', 'low'] },
      { start: 76.5, end: 80.5, main: "But I'm ready, I'm ready to go", sub: 'Mais je suis prêt, prêt à avancer', kind: 'hook', emphasis: ['ready'] },
      { start: 80.5, end: 84.5, main: "I've been broken, I've been scarred", sub: "J'ai été brisé, j'ai été marqué", kind: 'hook', emphasis: ['broken', 'scarred'] },
      { start: 84.5, end: 89.9, main: "But I'm rising, I'm reaching the stars", sub: "Mais je m'élève, j'atteins les étoiles", kind: 'hook', emphasis: ['rising', 'stars'] },
    ],
  },

  /* 6 — Refrain 1 (1:29.9–1:48.8) */
  {
    id: 'chorus1',
    label: 'Refrain 1',
    start: 89.9,
    end: 108.8,
    lines: [
      { start: 89.9, end: 94.0, main: "I'm not afraid, I'm not afraid", sub: "Je n'ai pas peur, je n'ai pas peur", kind: 'hook', emphasis: ['afraid'] },
      { start: 94.0, end: 98.0, main: 'To stand up, to break the chains', sub: 'Me relever, briser les chaînes', kind: 'hook', emphasis: ['chains'] },
      { start: 98.0, end: 102.5, main: "I'm not afraid, I'm not afraid", sub: "Je n'ai pas peur, je n'ai pas peur", kind: 'hook', emphasis: ['afraid'] },
      { start: 102.5, end: 106.8, main: 'To rise again, through the pain', sub: 'Renaître encore, malgré la douleur', kind: 'hook', emphasis: ['rise'] },
      { start: 106.8, end: 108.8, main: 'Wolof TechStein beat wê!', kind: 'stamp', note: 'red' },
    ],
  },

  /* 7 — Couplet 2 « Le combat » (1:48.8–2:04.8) */
  {
    id: 'verse2',
    label: 'Couplet 2 — Le combat',
    start: 108.8,
    end: 124.8,
    lines: [
      { start: 108.8, end: 110.9, main: 'Ils voulaient me voir à genoux, mendier, supplier', kind: 'verse' },
      { start: 110.9, end: 112.8, main: "Mais j'ai choisi de me battre, de me réveiller", kind: 'verse', emphasis: ['battre'] },
      { start: 112.8, end: 114.9, main: "J'ai rêvé de succès, j'ai sué, j'ai pleuré", kind: 'verse', emphasis: ['succès'] },
      { start: 114.9, end: 116.8, main: 'Mais chaque pas en avant est une victoire, une clé', kind: 'verse', emphasis: ['clé'], fx: 'key' },
      { start: 116.8, end: 119.0, main: 'La route est longue, les obstacles sont grands', kind: 'verse' },
      { start: 119.0, end: 120.0, main: "Mais j'ai la foi, j'ai le feu, j'ai le temps", kind: 'verse', emphasis: ['foi', 'feu', 'temps'] },
      { start: 120.0, end: 122.8, main: "Je réussirai, quoi qu'il arrive, quoi qu'on dise", kind: 'verse', emphasis: ['réussirai'] },
      { start: 122.8, end: 124.8, main: 'Ma réussite sera ma plus belle cicatrice', kind: 'verse', emphasis: ['cicatrice'], fx: 'fracture' },
    ],
  },

  /* 8 — Pré-refrain 2 (2:04.8–2:20) */
  {
    id: 'pre2',
    label: 'Pré-refrain 2',
    start: 124.8,
    end: 140,
    lines: [
      { start: 124.8, end: 127.8, main: "I've been down, I've been low", sub: "J'ai touché le fond, j'étais si bas", kind: 'hook', emphasis: ['down', 'low'] },
      { start: 127.8, end: 131.0, main: "But I'm ready, I'm ready to go", sub: 'Mais je suis prêt, prêt à avancer', kind: 'hook', emphasis: ['ready'] },
      { start: 131.0, end: 135.0, main: "I've been broken, I've been scarred", sub: "J'ai été brisé, j'ai été marqué", kind: 'hook', emphasis: ['broken', 'scarred'] },
      { start: 135.0, end: 140.0, main: "But I'm rising, I'm reaching the stars", sub: "Mais je m'élève, j'atteins les étoiles", kind: 'hook', emphasis: ['rising', 'stars'] },
    ],
  },

  /* 9 — Pont « La libération » (2:20–2:40) */
  {
    id: 'bridge',
    label: 'Pont — La libération',
    start: 140,
    end: 160,
    lines: [
      { start: 145.8, end: 149.0, main: "I'm not afraid of the fall", sub: "Je n'ai pas peur de tomber", kind: 'bridge', emphasis: ['fall'] },
      { start: 149.0, end: 152.9, main: "I'm not afraid of it all", sub: "Je n'ai pas peur de tout ça", kind: 'bridge', emphasis: ['all'] },
      { start: 152.9, end: 157.2, main: "I've survived the worst of me", sub: "J'ai survécu au pire de moi-même", kind: 'bridge', emphasis: ['survived'] },
      { start: 157.2, end: 160.0, main: "Now I'm finally free", sub: 'Maintenant je suis enfin libre', kind: 'bridge', emphasis: ['free'] },
    ],
  },

  /* 10 — Refrain final (2:40–2:57) */
  {
    id: 'final',
    label: 'Refrain final — Apothéose',
    start: 160,
    end: 177,
    lines: [
      { start: 160.0, end: 165.0, main: "I'm not afraid, I'm not afraid", sub: "Je n'ai pas peur, je n'ai pas peur", kind: 'final', emphasis: ['afraid'] },
      { start: 165.0, end: 169.0, main: 'To stand up, to break the chains', sub: 'Me relever, briser les chaînes', kind: 'final', emphasis: ['chains'] },
      { start: 169.0, end: 173.0, main: "I'm not afraid, I'm not afraid", sub: "Je n'ai pas peur, je n'ai pas peur", kind: 'final', emphasis: ['afraid'] },
      { start: 173.0, end: 177.0, main: 'To rise again, through the pain', sub: 'Renaître encore, malgré la douleur', kind: 'final', emphasis: ['rise'] },
    ],
  },

  /* 11 — Tag final ×3 (2:57–3:15) */
  {
    id: 'tag2',
    label: 'Tag final ×3',
    start: 177,
    end: 195,
    lines: [
      { start: 177.4, end: 180.6, main: 'Wolof TechStein beat wê!', kind: 'stamp', note: 'red', fx: 'fracture' },
      { start: 182.8, end: 186.0, main: 'Wolof TechStein beat wê!', kind: 'stamp', note: 'gold' },
      { start: 188.2, end: 191.6, main: 'Wolof TechStein beat wê!', kind: 'stamp', note: 'green' },
    ],
  },

  /* 12 — Outro (3:15–3:35) */
  {
    id: 'outro',
    label: 'Outro',
    start: 195,
    end: 215.2,
    lines: [
      { start: 195.0, end: 202.0, main: "(I'm not afraid...)", sub: "(Je n'ai pas peur...)", kind: 'echo', y: 46 },
      { start: 202.5, end: 207.5, main: "Si ce son t'a touché…", kind: 'cta', icon: 'heart', y: 34 },
      { start: 205.5, end: 210.5, main: 'LIKE   ABONNE-TOI   PARTAGE', kind: 'cta', icon: 'share', y: 50 },
      { start: 208.5, end: 214.0, main: 'Dis-moi en commentaire : quel passage t\u2019a le plus marqué ?', kind: 'cta', icon: 'comment', y: 66 },
      { start: 211.5, end: 215.2, main: 'Daïsky Pro × TechStein', kind: 'logo', note: 'BJ', y: 80 },
      { start: 213.6, end: 215.2, main: "Écoute aussi « I'm Not Dying », déjà disponible", kind: 'echo', note: 'bonus', y: 90 },
    ],
  },
];

export function allLines(): LyricLine[] {
  return SCENES.flatMap((s) => s.lines);
}
