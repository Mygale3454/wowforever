# wowforever

Site de fan non officiel consacré à World of Warcraft: Forever.

## Organisation
- `index.html`, `actualites.html`, `debuter.html`, `classes.html`, `donjons.html`, `legacy.html`, `calendrier.html` : les pages
- `css/style.css` : couleurs et mise en page (les couleurs sont en haut du fichier)
- `js/site.js` : menu, pied de page et barre latérale communs à toutes les pages
- `images/` : les illustrations

## Remplacer une image
Dépose ta propre image (par ex. une capture d'écran du jeu) dans `images/`,
puis remplace `images/xxx.svg` par `images/ton-image.jpg` dans la page voulue.

## Ajouter une page
1. Copie une page existante (par ex. `legacy.html`) sous un nouveau nom.
2. Change son contenu.
3. Ajoute-la dans la liste `MENU` en haut de `js/site.js`.
