# Portfolio audit and rebuild plan

Site: https://piyushsoni-ai.github.io/
Repo: piyushsoni-ai/piyushsoni-ai.github.io
Audited: 25 Nov 2026

## 1. Audit of the current site

The repo holds one file, `index.html` (42 KB), with two commits. No images, no CSS or JS files, no sitemap, no robots.txt, no resume file, no analytics.

What the page does well
- Exact name "Piyush Kumar Soni" used throughout, Person JSON-LD with sameAs, canonical, OG and Twitter tags.
- Verified career timeline (Sep 2011 start at Lucky Digitals) and education (BCA 2011, MCA 2018).
- Honours `prefers-reduced-motion`.

Problems found
- Positioning is "SEO Expert & AI/LLM Specialist", not the target "SEO & AI Search Leader". Hero and timeline lead with web design, graphics and video roles.
- Single page. No project pages, no case studies, no writing hub, no resume page. Recruiters must leave the site to understand any project.
- Every project card links to the GitHub profile root, not the project.
- "Schema Markup Generator" and "AI Content Humanizer" are listed, but no public repo exists for either (`ai-content-humanizer` returns auth-required; no schema generator repo).
- `google-maps-scraper` repo exists but is empty. The site presents it as "Completed".
- No results or proof section. The 211K clicks / 10.5M impressions work is not shown anywhere.
- The Firefox extension (live on AMO, v1.0.0) and the Hugging Face Spaces are missing or linked to the HF profile root.
- Medium link in sameAs uses `@piyushkumarsoni`; the brief supplies `@piyushkrsoni`.
- Schema `image` points to a Carrd-hosted file, not an asset in this repo. Schema also exposes the email address and an `alternateName` ("Piyush Soni") that works against exact-name consistency.
- `meta keywords` (ignored by Google) and `geo.*` tags add noise.
- Three Google Fonts families (render-blocking request, ~100 KB).
- Typing "console" animation and pulsing dot add JS and motion with no information value.
- Nav hidden on mobile with no menu replacement. No skip link, no visible focus styles.
- Footer has 8 icon-only social buttons with no text labels.
- No 404 page.

## 2. What stays
- Person entity data: name, Kanpur/UP/IN address, worksFor Lucky Digitals, alumniOf.
- Career timeline dates and education (moved to About and Resume).
- Dark navy theme direction (toned down, single blue accent).
- Reduced-motion handling.
- Canonical domain and URL.
- Public email already on the site (kept on Contact only, removed from schema).

## 3. What goes
- Console typing animation, pulse dot, gradient headline text, multi-colour icon tiles.
- "Schema Markup Generator" and "AI Content Humanizer" cards (no public source).
- `meta keywords`, `geo.*` meta, `alternateName`.
- Google Fonts (replaced with system font stack).
- Icon-only footer row (replaced with five text links).
- Web Designer / Graphic Designer / Video Editor roles as headline positioning (kept as history in About and Resume).

## 4. Sitemap
```
/                                   Home
/about/                             About
/expertise/                         Expertise and tools
/projects/                          Projects hub
  /projects/seo-master-skill/
  /projects/gbp-audit-ai-visibility/
  /projects/google-maps-scraper/
  /projects/snaplife-ai/
  /projects/teachmonk/
  /projects/seo-meta-generator/
  /projects/seo-ai-citation-audit/
/case-studies/                      Case studies hub
  /case-studies/global-seo-ai-growth/
  /case-studies/gbp-ai-visibility/
  /case-studies/seo-master-skill/
  /case-studies/snaplife-ai/
/writing/                           Articles grouped by topic (external links)
/resume/                            HTML resume + download
/contact/                           Contact + profile hub (replaces /connect/)
/404.html                           noindex
```
"Results" in the nav points to `/#results`. AI Business Name Generator gets a card on /projects/ only (low priority, avoids a thin page).

## 5. Homepage wireframe
```
[ sticky nav: name | Home About Expertise Results Projects Case studies Writing Resume Contact | Download resume ]
[ HERO  photo slot | H1 Piyush Kumar Soni / SEO & AI Search Leader / supporting line / intro / 4 CTAs ]
[ RESULTS  6 stat tiles + disclaimer ]
[ EXPERTISE  6 cards, 4 items each, link to /expertise/ ]
[ TOOLS  3 grouped lists ]
[ FEATURED PROJECTS  4 cards, link to /projects/ ]
[ CASE STUDIES  4 cards ]
[ WRITING  4 latest article cards, link to /writing/ ]
[ OPEN TO OPPORTUNITIES  short list ]
[ CONTACT  LinkedIn / GitHub / Email ]
[ footer ]
```

## 6. Content hierarchy
Identity, positioning, results, expertise, projects, case studies, writing, career interests, contact. Historical design/video skills sit in About and Resume only.

## 7. SEO metadata plan
Every page gets a unique title (under ~60 chars where possible), unique description, self-canonical, OG + Twitter tags, shared OG image `/assets/img/og-default.png`. Home, About, Projects and Case Studies use the exact titles and descriptions from the brief. Deep pages follow `<Page> | Piyush Kumar Soni`.

## 8. Schema plan
- Home: `Person` (@id `/#person`) + `WebSite` (@id `/#website`).
- All other pages: `WebPage` / `CollectionPage` / `ProfilePage` referencing `/#person`, plus `BreadcrumbList` on deeper pages.
- `SoftwareApplication` only for things people can use today: Firefox extension (BrowserApplication), SEO Meta Generator and AI Citation Audit (WebApplication).
- `SoftwareSourceCode` for SEO Master Skill (public MIT repo).
- No schema for SnapLife AI, TeachMonk, Google Maps Scraper (not released / no code yet).
- No `Article` schema: no articles are hosted on the portfolio.
- `sameAs`: LinkedIn, GitHub, Medium, Substack, DEV.to, Hugging Face, Wellfound.

## 9. Internal linking plan
- Each project page links to its case study and back; each case study links to its project.
- Every deep page has breadcrumbs and a "related" block.
- Home links to every hub. Hubs link to every child.
- Resume links to project pages; About links to Resume, Expertise, Case Studies.
- Footer links to five external profiles; Contact holds the full profile hub.

## 10. Design direction
Dark navy (#0b1220) with one restrained blue accent (#5b9dff), system font stack, 8px spacing scale, simple bordered cards, no glow, no gradient text, motion limited to hover colour changes. Body text 17px, line length capped near 70ch. Visible focus rings. Single small JS file (mobile menu, click tracking hooks, photo fallback).
