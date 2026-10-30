# mscosentino.com

Static personal site (ES/EN) for Mariano S. Cosentino. Deployed to Azure Static Web Apps from `main`.

- **Texts live in `content/`** as plain text files (see `content/LEEME.txt` for the format and common tasks). `build.py` has no texts: it reads `content/` and generates the HTML.
- `site/` is what gets published. HTML is generated: edit `content/`, then run `python build.py site`.
- Style and behaviour: `site/assets/style.css` and `site/assets/site.js` (edited directly).
- Photos go in `site/assets/photos/` and are listed per job in `content/jobs/*.txt`.
- `_originales/` holds the full-size source photos and is not committed.
