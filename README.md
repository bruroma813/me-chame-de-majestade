# Me chame de majestade

Banco de questões comentadas para o 6º ENAM (29/11/2026).

- `site/index.html`: o site publicado (Netlify publica a pasta `site/`).
- `fonte/`: gerador (`build.py`), template e dados (questões inéditas, comentários das questões reais da FGV, matriz de cobertura do edital, códigos estáveis).

Para regenerar: `cd fonte && python3 build.py` e copiar `dist/index.html` para `site/`.
