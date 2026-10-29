# Overlays Twitch wowforever

Cinq scènes au format 1920 x 1080, sur le thème parchemin de WoW Forever.

| Fichier | Scène | Contenu |
|---|---|---|
| `attente.html` | Le stream commence bientôt | Compte à rebours, astuces WoW Forever qui défilent, braises animées |
| `pause.html` | Pause | Le nain et sa chope, avec l'enseigne « C'est l'heure du rafraîchissement ! » |
| `fin.html` | Fin du live | Petit message de remerciement |
| `jeu.html` | En jeu (fond transparent) | Médaillon de ton éolide mage et derniers soutiens (abonné, abos offerts, bits) en bas à gauche |
| `discussion.html` | Discussion | Grand cadre webcam, cadre de chat « La taverne », astuces |

Le dossier `png/` contient les mêmes scènes en images fixes, si tu préfères des images simples.

## Ajouter un overlay dans OBS (version animée, conseillée)

1. Dans OBS, crée une scène (par exemple « Attente »).
2. Dans **Sources**, clique sur **+** puis **Navigateur**.
3. Coche **Fichier local** et choisis `attente.html`,
   ou décoche-le et colle l'adresse en ligne :
   `https://mygale3454.github.io/wowforever/overlays/attente.html?nom=TonPseudo&min=10`
4. Largeur **1920**, hauteur **1080**, puis **OK**.

Fais pareil pour les autres scènes.

## Personnaliser avec l'adresse

Ajoute ces réglages à la fin de l'adresse en ligne. Avec un fichier local, ouvre plutôt `overlay.js` et remplace `"wowforever"` par ton pseudo à la ligne `const NOM`.

Réglages possibles :

- `?nom=TonPseudo` : ton pseudo Twitch, sur toutes les scènes
- `&min=5` : durée du compte à rebours de l'écran d'attente, en minutes

Exemple : `attente.html?nom=Mygale&min=5`

Le compte à rebours repart de zéro à chaque fois que la scène est rechargée. Dans OBS, coche
**« Actualiser le navigateur quand la scène devient active »** pour qu'il redémarre à chaque passage sur la scène.

## Scène « En jeu »

1. Ajoute d'abord la **Capture de jeu** de WoW.
2. Ajoute `jeu.html` en source Navigateur **tout en haut de la liste** : son fond est transparent.

En bas à gauche s'affichent le médaillon de ton éolide et trois plaques : dernier abonné,
derniers abonnements offerts et derniers bits. Tu les remplis avec l'adresse :

`jeu.html?sub=Pseudo1&gift=Pseudo2&bits=Pseudo3`

Autres réglages possibles :
- `&cam=1` : affiche aussi un cadre webcam au-dessus du médaillon (320 x 180, à 28 px du bord gauche et 300 px du bas)
- `&perso=Prénom Nom` : change le nom affiché sous le portrait (par défaut « Mygale Araneae »)

Pour changer de portrait, remplace l'image `img/mygale.jpg` (format carré).

### Mise à jour automatique avec Streamlabs

1. Sur streamlabs.com : **Paramètres** (ton avatar en haut à droite) → **Paramètres API** → onglet **Jetons API**.
2. Copie **Ton jeton Socket API** (« Your Socket API Token »).
3. Dans OBS, mets cette adresse dans la source navigateur de la scène « En jeu » :
   `https://mygale3454.github.io/wowforever/overlays/jeu.html?slt=TON_JETON`
4. Teste avec les boutons **Test** de la fenêtre d'alerte Streamlabs (abonnement, bits…) : les plaques doivent changer et s'illuminer.

Les derniers noms sont gardés en mémoire par OBS, même après un redémarrage.
Ne montre jamais cette adresse à l'écran : le jeton est personnel.

## Scène « Discussion »

- Webcam ou fenêtre : cadre de 1200 x 675, à 64 px de la gauche et 140 px du haut. La plaque « Discussion avec… » est placée sous le cadre, elle reste visible.
- Chat : place une source de chat (par exemple l'adresse « Chat en fenêtre » de Twitch) dans le cadre de droite (520 x 675).

## Animations d'alertes (dossier `alertes/`)

Quatre animations originales de 3 secondes, au fond transparent, pour les alertes Streamlabs :

| Fichier | Idée d'utilisation |
|---|---|
| `rune.webm` | Follow |
| `parchemin.webm` | Abonnement |
| `tresor.webm` | Bits et dons |
| `portail.webm` | Raid |

Les versions `.gif` sont fournies pour les logiciels qui ne lisent pas le WebM (moins nettes).
Dans Streamlabs, champ **Image** de l'alerte → icône d'envoi → **Upload**, ou icône 🔗 avec l'adresse en ligne, par exemple :
`https://mygale3454.github.io/wowforever/overlays/alertes/rune.webm`
