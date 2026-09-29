# Polices de production

- Barlow Condensed Bold : `@fontsource/barlow-condensed` 5.3.0, sous-ensemble latin, poids 700. Conversion WOFF2 → TTF via fontTools, sans modification des dessins. Licence OFL jointe. Vérification des caractères des paroles : aucun glyphe manquant.
- DejaVu Sans Bold : police système Debian, UI et badge. Licence jointe.

Acquisition : `npm pack --ignore-scripts @fontsource/barlow-condensed@5.3.0` puis `TTFont(source_woff2)`, `font.flavor=None`, `font.save(destination_ttf)`.

- Great Vibes Regular : `@fontsource/great-vibes` 5.3.0, poids 400, latin, convertie de WOFF2 vers TTF avec fontTools. Licence OFL jointe ; titres et artiste couverts.
