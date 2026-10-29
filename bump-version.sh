#!/bin/sh
# Met à jour le numéro de version des fichiers CSS/JS dans toutes les pages,
# pour forcer les navigateurs à recharger la dernière version du site.
V=$(date +%Y%m%d%H%M)
for f in *.html; do
  sed -i -E "s#(href=\"css/style\.css)(\?v=[0-9]+)?\"#\1?v=$V\"#; s#(src=\"js/[a-z-]+\.js)(\?v=[0-9]+)?\"#\1?v=$V\"#g" "$f"
done
echo "Version $V"
