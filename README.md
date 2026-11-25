# piyushsoni-ai.github.io

Portfolio of **Piyush Kumar Soni**, SEO & AI Search Leader.
Live: https://piyushsoni-ai.github.io/

Plain static HTML, one CSS file, one small JS file. No framework, no build step needed on GitHub Pages.

## Editing

All text lives in `_build/content.py`. After editing:

```bash
python3 _build/build.py
```

This regenerates every page, `sitemap.xml`, `robots.txt`, the favicon and the OG image. Jekyll ignores `_build/`, so it is never published.

## Two files to add before going live

| File | What happens when you add it |
|---|---|
| `assets/img/piyush-kumar-soni.jpg` (portrait, about 520×650) | Hero shows the photo instead of the "PKS" placeholder, and the Person schema gets an `image`. |
| `assets/resume/Piyush_Kumar_Soni_SEO_AI_Search_Master_Resume_2026.docx` | Every "Download resume" button links to the file. Until then they open `/resume/`, which has a print / save-as-PDF option. |

Rebuild after adding either file.

## Analytics

None is installed. Links carry `data-track` attributes (resume, LinkedIn, GitHub, projects, case studies, extension, contact). `assets/js/site.js` forwards those clicks automatically if you later add Plausible, GoatCounter (free) or GA4. Nothing is sent otherwise.

## Content to review

- `/case-studies/global-seo-ai-growth/`: the narrative is written in general terms around the supplied metrics. Check it matches the real project.
- Google Maps Scraper: the GitHub repo is empty, so the page says the code is not published yet. Update `content.py` once code is pushed.
- Medium: links use `@piyushkrsoni` (from the brief). The old site used `@piyushkumarsoni`. Keep whichever is live.

See `_build/AUDIT.md` for the audit and plan.
