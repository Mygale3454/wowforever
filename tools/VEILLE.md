# Veille hebdomadaire des builds (guides.html)

Source : https://github.com/snibi/forever-meta (fichiers `src/content/specs/<classe>-<spe>.json`, champ `builds`).
Dernier commit intégré au site : `tools/forever-meta-commit.txt`.

## Fichiers
- `tools/builds.json` : un build PvE par spé (clé `warrior-arms`, etc.) :
  `code` (hash du calculateur, sans `talents.html#`), `total` (51), `split` ("16/35/0"), `stats` (libellés anglais),
  `races` {alliance, horde} (ids : human, dwarf, night-elf, gnome, orc, undead, tauren, troll), `key` (talents clés),
  `adapted` (true si le build source a été complété pour atteindre 51 points), `main` (arbre principal).
- `tools/guides.py` : génère `guides.html` à partir de `builds.json` (textes FR écrits à la main dans le script, ne pas copier la prose de la source).
  Lancer : `python3 tools/guides.py` depuis la racine du dépôt.

## Format du hash du calculateur
`classe-arbre1-arbre2-arbre3` : un caractère base36 par talent, dans l'ordre des talents de chaque arbre
(voir `js/talents-data.js`), zéros finaux supprimés. Règles : 51 points max, 5 points par rang, prérequis respectés.
Vérifier un build : ouvrir `talents.html#<code>` avec Playwright et lire le compteur « 51 / 51 ».

## Procédure (mode prudent : ne jamais pousser sur main)
1. `git clone --depth 50 https://github.com/snibi/forever-meta` dans un dossier temporaire.
2. `git diff <commit intégré>..HEAD --stat -- src/content/specs src/data` : s'il n'y a rien, s'arrêter et le signaler brièvement.
3. Sinon, pour chaque spé modifiée, comparer le build PvE (talents, stats, races) avec `tools/builds.json`.
4. Préparer la mise à jour sur une branche `veille-builds-AAAA-MM-JJ` : `builds.json`, `forever-meta-commit.txt`,
   `python3 tools/guides.py`, `sh bump-version.sh`, une news en haut de `js/news.js`. Pousser uniquement cette branche.
5. Envoyer à Mygale un résumé en français : quelles spés changent et comment, et lien de la branche.
   La fusion sur main se fait seulement après son accord.

## Leveling pas à pas (pas-a-pas*.html)
Générées depuis Polestar (https://github.com/fitzforge/polestar, GPL-3.0) :
`git clone --depth 1 https://github.com/fitzforge/polestar /tmp/polestar && python3 tools/pas_a_pas.py /tmp/polestar`.
Les noms de lieux sans traduction dans les données sont dans `tools/lieux_fr.json` ; ceux restés en anglais sont listés dans `tools/lieux_manquants.json`.

## Après toute génération de pages
`python3 tools/seo.py` : remet l'adresse officielle et les balises de partage de chaque page, et refait le sitemap.
