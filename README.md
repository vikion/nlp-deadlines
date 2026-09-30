# NLP Deadlines

A static page listing deadlines relevant to NLP researchers: conferences (ACL, EMNLP, NAACL, EACL, COLING, …), ARR cycles, shared tasks, summer schools and PhD/fellowship applications.

## Publish on GitHub Pages
1. Create a repo (e.g. `nlp-deadlines`) and push these files to `main`.
2. Settings → Pages → Source: *Deploy from a branch* → `main` / root.
3. Settings → Actions → General → Workflow permissions: *Read and write* (so the daily bot can commit).
4. Site appears at `https://<you>.github.io/nlp-deadlines/`.

## How it updates
- `data/curated.json` — entries you maintain by hand (schools, shared tasks, fellowships, and verified conference dates). Edit it and commit.
- `scripts/update.py` — merges curated data with [ccfddl/ccf-deadlines](https://github.com/ccfddl/ccf-deadlines) into `data/deadlines.json`. Curated venue+year entries take precedence.
- `.github/workflows/update.yml` — runs the script daily and commits changes.

Entry fields: `venue, year, label, category (conference|shared_task|school|fellowship), date (ISO with offset, AoE = -12:00; null if unknown), precision ("month" for tentative), event_dates, place, note, link`.

Undated entries (schools, fellowships) are marked as unverified in their notes — check the linked site and fill in `date` when announced.
