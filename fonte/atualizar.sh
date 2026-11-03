#!/bin/sh
# Regenera o site a partir dos dados e copia para site/ (publicado pelo Netlify)
set -e
cd "$(dirname "$0")"
python3 build.py
cp dist/index.html ../site/index.html
echo "site/index.html atualizado"
