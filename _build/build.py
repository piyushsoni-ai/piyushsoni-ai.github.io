#!/usr/bin/env python3
"""Static site generator for piyushsoni-ai.github.io.

Run from the repo root:  python3 _build/build.py
Writes plain HTML into the repo (GitHub Pages serves it as-is; Jekyll ignores _build/).
"""
import json, os, sys, datetime
from html import escape as esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import *  # noqa

TODAY = datetime.date.today().isoformat()
HAS_PHOTO = os.path.exists(os.path.join(ROOT, PHOTO_FILE))
HAS_RESUME = os.path.exists(os.path.join(ROOT, RESUME_FILE))
PERSON_ID = BASE + "/#person"
SITE_ID = BASE + "/#website"
OG_IMAGE = BASE + "/assets/img/og-default.png"
PAGES = []  # (path, indexable)

NAV = [("home", "Home", "/"), ("about", "About", "/about/"), ("expertise", "Expertise", "/expertise/"),
       ("results", "Results", "/#results"), ("projects", "Projects", "/projects/"),
       ("cases", "Case studies", "/case-studies/"), ("writing", "Writing", "/writing/"),
       ("resume", "Resume", "/resume/"), ("contact", "Contact", "/contact/")]

EXT = 'target="_blank" rel="noopener"'


def ext_a(label, url, track=None, cls=None):
    t = f' data-track="{track}"' if track else ""
    c = f' class="{cls}"' if cls else ""
    return f'<a href="{esc(url)}"{c} {EXT}{t}>{esc(label)}<span class="sr-only"> (opens in a new tab)</span></a>'


def resume_btn(cls="btn"):
    if HAS_RESUME:
        return f'<a class="{cls}" href="/{RESUME_FILE}" download data-track="resume-download">Download resume</a>'
    return f'<a class="{cls}" href="/resume/#download" data-track="resume-view">Download resume</a>'


# ------------------------------------------------------------------ schema
def person(full=True):
    p = {"@type": "Person", "@id": PERSON_ID, "name": NAME, "url": BASE + "/", "jobTitle": ROLE}
    if not full:
        return p
    if HAS_PHOTO:
        p["image"] = BASE + "/" + PHOTO_FILE
    p.update({
        "description": f"{NAME} is an SEO and AI Search leader working across technical SEO, GEO/AEO, organic growth, LLM/RAG workflows and automation since 2011.",
        "worksFor": {"@type": "Organization", "name": "Lucky Digitals", "url": L["lucky"]},
        "address": {"@type": "PostalAddress", "addressLocality": "Kanpur", "addressRegion": "Uttar Pradesh", "addressCountry": "IN"},
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": e[2].split(",")[0]} for e in EDUCATION],
        "knowsAbout": ["Search Engine Optimization", "Technical SEO", "Generative Engine Optimization",
                       "Answer Engine Optimization", "AI Search", "Entity SEO", "Structured Data",
                       "Large Language Models", "Retrieval-Augmented Generation", "AI Agents", "SEO Automation"],
        "sameAs": SAME_AS,
    })
    return p


def crumbs_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(crumbs)]}


def webpage(path, title, desc, kind="WebPage", crumbs=None, extra=None):
    g = [{"@type": kind, "@id": BASE + path + "#webpage", "url": BASE + path, "name": title, "description": desc,
          "isPartOf": {"@id": SITE_ID}, "about": {"@id": PERSON_ID}, "inLanguage": "en"}]
    if crumbs:
        g[0]["breadcrumb"] = {"@id": BASE + path + "#breadcrumb"}
        b = crumbs_schema(crumbs); b["@id"] = BASE + path + "#breadcrumb"; g.append(b)
    if extra:
        g.extend(extra)
    return g


# ------------------------------------------------------------------ layout
def header(active):
    items = []
    for key, label, href in NAV:
        cur = ' aria-current="page"' if key == active else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f'''<header class="site-header">
  <div class="wrap">
    <nav class="nav" aria-label="Main">
      <a class="brand" href="/">{NAME}<span class="dot" aria-hidden="true">.</span></a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav-links"><span class="label">Menu</span></button>
      <ul class="nav-links" id="nav-links">{"".join(items)}</ul>
      <span class="nav-cta">{resume_btn("btn btn-sm")}</span>
    </nav>
  </div>
</header>'''


def footer():
    links = [("LinkedIn", L["linkedin"], "linkedin"), ("GitHub", L["github"], "github"), ("Medium", L["medium"], "medium"),
             ("Substack", L["substack"], "substack"), ("DEV.to", L["devto"], "devto")]
    lis = "".join(f"<li>{ext_a(n, u, 'footer-' + t)}</li>" for n, u, t in links)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <p class="name">{NAME}</p>
        <p class="tag">SEO &amp; AI Search Leader | Technical SEO · GEO/AEO · LLM/RAG · Automation</p>
        <p class="tag">SEO, web and digital growth since 2011.</p>
      </div>
      <nav aria-label="Profiles"><ul class="footer-links">{lis}</ul></nav>
    </div>
    <p class="copy">© <span id="year">2026</span> {NAME}. Kanpur, Uttar Pradesh, India.</p>
  </div>
</footer>'''


def breadcrumbs_html(crumbs):
    out = []
    for i, (n, u) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            out.append(f'<li aria-current="page">{esc(n)}</li>')
        else:
            out.append(f'<li><a href="{u}">{esc(n)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(out)}</ol></nav>'


def render(path, title, desc, body, active=None, schema=None, og_type="website", noindex=False, og_title=None, og_desc=None):
    canonical = BASE + path
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    ld = ""
    if schema:
        ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": schema}, ensure_ascii=False, indent=1) + "</script>"
    ot, od = og_title or title, og_desc or desc
    html = f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="{NAME}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(ot)}">
<meta property="og:description" content="{esc(od)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME}, {ROLE}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(ot)}">
<meta name="twitter:description" content="{esc(od)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<meta name="theme-color" content="#0a0e1a">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/css/site.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, path.lstrip("/"), "index.html") if path.endswith("/") else os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    PAGES.append((path, not noindex))


def page_head(title, lede, crumbs=None, eyebrow=None, meta_html=""):
    c = breadcrumbs_html(crumbs) if crumbs else ""
    e = f'<span class="eyebrow">{esc(eyebrow)}</span>' if eyebrow else ""
    l = f'<p class="lede">{lede}</p>' if lede else ""
    return f'<div class="page-head"><div class="wrap">{c}{e}<h1>{esc(title)}</h1>{l}{meta_html}</div></div>'


# ------------------------------------------------------------------ components
def stats_html():
    lis = "".join(f'<li class="stat"><b>{v}</b><span>{l}</span></li>' for v, l in STATS)
    return f'<ul class="stats">{lis}</ul><p class="note">{STATS_NOTE}</p>'


def expertise_cards(full=False):
    out = []
    for t, d, items in EXPERTISE:
        show = items if full else items[:5]
        lis = "".join(f"<li>{esc(i)}</li>" for i in show)
        more = "" if full or len(items) <= 5 else f'<li class="muted">and {len(items) - 5} more</li>'
        para = f"<p>{esc(d)}</p>" if full else ""
        out.append(f'<div class="card"><h3>{esc(t)}</h3>{para}<ul>{lis}{more}</ul></div>')
    return f'<div class="grid grid-3">{"".join(out)}</div>'


def tools_html():
    out = []
    for g, items in TOOLS:
        lis = "".join(f"<li>{esc(i)}</li>" for i in items)
        out.append(f'<div class="card"><h3>{esc(g)}</h3><ul>{lis}</ul></div>')
    return f'<div class="tool-groups">{"".join(out)}</div>'


def pill(status):
    label, kind = status
    cls = {"live": "pill live", "dev": "pill dev", "private": "pill dev"}.get(kind, "pill")
    return f'<span class="{cls}">{esc(label)}</span>'


def project_card(p, n=0):
    tags = "".join(f"<li>{esc(t)}</li>" for t in p["tech"][:4])
    return f'''<article class="card proj-card c{n % 6 + 1}">
  <div class="meta"><span class="cat">{esc(p["cat"])}</span>{pill(p["status"])}</div>
  <h3><a href="/projects/{p["slug"]}/" data-track="project-{p["slug"]}">{esc(p["title"])}</a></h3>
  <p>{esc(p["short"])}</p>
  <ul class="tags" aria-label="Technologies">{tags}</ul>
</article>'''


def case_card(c):
    tags = "".join(f"<li>{esc(t)}</li>" for t in c["tags"])
    return f'''<article class="card">
  <span class="cat">Case study</span>
  <h3 style="margin-top:8px"><a href="/case-studies/{c["slug"]}/" data-track="case-{c["slug"]}">{esc(c["title"])}</a></h3>
  <p>{esc(c["card"])}</p>
  <ul class="tags">{tags}</ul>
</article>'''


def article_item(a):
    t, u, src, date = a
    when = f" · {date}" if date else ""
    return f'<li class="article">{ext_a(t, u, "article-click")}<span class="src">{src}{when}</span></li>'


def section(id_, title, inner, lede=None, more=None, eyebrow=None):
    i = f' id="{id_}"' if id_ else ""
    e = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    l = f"<p>{lede}</p>" if lede else ""
    m = f'<a class="more" href="{more[1]}">{more[0]} →</a>' if more else ""
    hid = f"h-{id_}" if id_ else ""
    return f'''<section class="section"{i} aria-labelledby="{hid}">
  <div class="wrap fade-in">
    <div class="section-head"><div>{e}<h2 id="{hid}">{title}</h2>{l}</div>{m}</div>
    {inner}
  </div>
</section>'''


def photo_html():
    if HAS_PHOTO:
        return f'<div class="photo"><img src="/{PHOTO_FILE}" alt="{NAME}, {ROLE}" width="520" height="650" fetchpriority="high"></div>'
    return ('<div class="photo" role="img" aria-label="Photo placeholder"><span class="initials" aria-hidden="true">PKS</span>'
            f'<span class="ph-note">Add photo: /{PHOTO_FILE}</span></div>')


def contact_buttons():
    return (f'<div class="btn-row">{ext_a("LinkedIn", L["linkedin"], "linkedin-contact", "btn btn-primary")}'
            f'{ext_a("GitHub", L["github"], "github-contact", "btn")}'
            f'<a class="btn" href="mailto:{EMAIL}" data-track="email-contact">Email</a></div>')


def opp_html():
    lis = "".join(f"<li>{esc(o)}</li>" for o in OPPORTUNITIES)
    return (f'<div class="narrow"><p class="muted">I am interested in senior and leadership opportunities involving:</p>'
            f'<ul class="tags" style="margin-bottom:18px">{lis}</ul>'
            f'<p class="muted small">Based in Kanpur, India. Open to remote roles and to working with teams across time zones.</p></div>')


# ------------------------------------------------------------------ pages
def build_home():
    feat = [p for p in PROJECTS if p.get("featured")]
    body = f'''<section class="hero" aria-labelledby="h-hero">
  <div class="wrap hero-grid">
    <div>
      <div class="pill-eyebrow"><span class="dot" aria-hidden="true"></span>SEO &amp; AI Search Lead at Lucky Digitals</div>
      <h1 id="h-hero">{NAME}</h1>
      <p class="role"><span class="accent">{ROLE}</span></p>
      <p class="support">{SUPPORT}</p>
      <div class="lede">
        <p>I work at the intersection of SEO, AI Search, LLMs, automation, and digital growth, with hands-on experience in search and web technologies since 2011.</p>
        <p>My work combines strong SEO fundamentals with emerging search technologies, helping businesses improve technical performance, content architecture, entity understanding, organic visibility, AI Search readiness, and operational efficiency.</p>
      </div>
      <div class="btn-row">
        <a class="btn btn-primary" href="/projects/" data-track="hero-projects">View my work</a>
        <a class="btn" href="/case-studies/" data-track="hero-cases">Explore case studies</a>
        {resume_btn()}
        {ext_a("LinkedIn", L["linkedin"], "linkedin-hero", "btn")}
      </div>
    </div>
    <div class="hero-photo">{photo_html()}</div>
  </div>
</section>
{section("results", 'Selected <span class="grad">results</span>', stats_html(), more=("Read the case study", "/case-studies/global-seo-ai-growth/"), eyebrow="Proof of work")}
{section("expertise", 'What I <span class="grad">work on</span>', expertise_cards(), more=("All expertise", "/expertise/"), eyebrow="Expertise")}
{section("tools", 'My <span class="grad">technical toolkit</span>', tools_html())}
{section("projects", 'Featured <span class="grad">SEO, GEO &amp; AI projects</span>', '<div class="grid grid-2">' + "".join(project_card(p, i) for i, p in enumerate(feat)) + "</div>", lede="Open-source tools, live utilities and private products. Each one is explained here first, with code links where the source is public.", more=("All projects", "/projects/"), eyebrow="Portfolio")}
{section("case-studies", 'Case <span class="grad">studies</span>', '<div class="grid grid-2">' + "".join(case_card(c) for c in CASES) + "</div>", more=("All case studies", "/case-studies/"))}
{section("writing", 'Recent <span class="grad">writing</span>', '<ul class="article-list">' + "".join(article_item(a) for a in LATEST) + "</ul>", more=("All articles", "/writing/"), eyebrow="From SEO to AI")}
{section("opportunities", "Open to opportunities", opp_html())}
{section("contact", 'Let\'s <span class="grad">connect</span>', '<div class="narrow"><p class="muted">Interested in discussing SEO, AI Search, organic growth, automation, product ideas, or relevant leadership opportunities? Connect with me through LinkedIn or explore my work on GitHub.</p>' + contact_buttons() + "</div>", eyebrow="Contact")}'''
    schema = [person(), {"@type": "WebSite", "@id": SITE_ID, "url": BASE + "/", "name": NAME,
                         "description": "Portfolio of Piyush Kumar Soni, SEO & AI Search Leader.", "publisher": {"@id": PERSON_ID}, "inLanguage": "en"},
              {"@type": "ProfilePage", "@id": BASE + "/#webpage", "url": BASE + "/", "name": "Piyush Kumar Soni | SEO & AI Search Leader",
               "isPartOf": {"@id": SITE_ID}, "mainEntity": {"@id": PERSON_ID}, "inLanguage": "en"}]
    render("/", "Piyush Kumar Soni | SEO & AI Search Leader",
           "Portfolio of Piyush Kumar Soni, SEO & AI Search leader working across Technical SEO, GEO/AEO, organic growth, LLM/RAG, automation, and digital strategy since 2011.",
           body, "home", schema, og_type="profile",
           og_title="Piyush Kumar Soni | SEO, AI Search & Digital Growth",
           og_desc="Technical SEO, GEO/AEO, AI Search, LLM/RAG, automation, projects, case studies, and search growth experience.")


def timeline_html(compact=False):
    out = []
    for when, title, org, bullets in EXPERIENCE:
        desc = f"<p>{esc(bullets[0])}</p>" if compact else ""
        out.append(f'<li><span class="when">{when}</span><h3>{esc(title)}</h3><p class="small">{esc(org)}</p>{desc}</li>')
    return f'<ol class="timeline">{"".join(out)}</ol>'


def build_about():
    crumbs = [("Home", "/"), ("About", "/about/")]
    title = "About Piyush Kumar Soni | SEO, GEO & AI Search"
    desc = "Learn about Piyush Kumar Soni's experience across Technical SEO, organic growth, GEO/AEO, AI Search, LLM workflows, automation, web technologies, and leadership."
    edu = "".join(f'<li><span class="when">{y}</span><h3>{esc(d)}</h3><p class="small">{esc(s)}</p></li>' for y, d, s in EDUCATION)
    body = page_head("SEO foundations. AI search thinking. Practical execution.", f"{NAME}, {ROLE}. Working in search and web technologies since 2011.", crumbs, "About") + f'''
<div class="wrap layout">
  <div class="prose">
    <p>I started working across digital, web, and search technologies in 2011. My career has evolved from hands-on SEO and website work into technical SEO, organic growth strategy, team leadership, digital project delivery, AI Search, LLM workflows, RAG, and automation.</p>
    <p>My core strength is connecting traditional search fundamentals with newer AI-driven discovery.</p>
    <p>I work across areas such as crawlability, indexation, site architecture, structured data, internal linking, search intent, topical authority, content optimization, entity understanding, GEO, AEO, AI visibility, and automation.</p>
    <p>Alongside strategy, I enjoy building practical tools and workflows that turn ideas into working systems. Some are public, like <a href="/projects/seo-master-skill/">SEO Master Skill</a> and the <a href="/projects/gbp-audit-ai-visibility/">GBP Audit + AI Visibility</a> extension. Others, like <a href="/projects/snaplife-ai/">SnapLife AI</a>, are products I am building on my own time.</p>
    <h2>My approach</h2>
    <div class="callout"><strong>Strong SEO fundamentals + structured information + authority + entity clarity + useful content + AI-ready systems.</strong></div>
    <p>AI Search has not replaced SEO. It has raised the cost of weak foundations. A page that is hard to crawl, vague about who is behind it, or thin on evidence will struggle in classic results and in AI answers alike. So I fix the foundations first, then build the clarity and authority that both kinds of search reward.</p>
    <h2>Current role</h2>
    <p><strong>{CURRENT_TITLE}</strong> at <a href="{L["lucky"]}" {EXT}>Lucky Digitals</a>, Kanpur, since September 2025. I lead technical SEO, GEO/AEO and AI visibility work for agency clients and build the internal tools and SOPs the SEO team uses.</p>
    <h2>Career path</h2>
    <p>All of my career so far has been at Lucky Digitals, which gave me the chance to move through video, design, web development and SEO before settling into search leadership and AI work.</p>
    {timeline_html(compact=True)}
    <h2>Earlier skills</h2>
    <p>Years of design and video work left me with practical Photoshop, Illustrator and After Effects skills. They are not my focus now, but they help when a project needs a quick visual, a clean landing page or a product demo.</p>
    <h2>Education</h2>
    <ol class="timeline edu">{edu}</ol>
  </div>
  <aside class="aside" aria-label="Quick facts">
    <div class="card"><h2>Quick facts</h2><dl class="facts">
      <div><dt>Role</dt><dd>{ROLE}</dd></div>
      <div><dt>Since</dt><dd>2011</dd></div>
      <div><dt>Company</dt><dd>Lucky Digitals</dd></div>
      <div><dt>Base</dt><dd>Kanpur, India</dd></div>
    </dl></div>
    <div class="card"><h2>Next</h2><p class="small"><a href="/expertise/">Expertise and tools</a><br><a href="/case-studies/">Case studies</a><br><a href="/resume/">Resume</a><br><a href="/contact/">Contact</a></p></div>
  </aside>
</div>
{section("opportunities", "Open to opportunities", opp_html())}'''
    render("/about/", title, desc, body, "about", webpage("/about/", title, desc, "AboutPage", crumbs))


def build_expertise():
    crumbs = [("Home", "/"), ("Expertise", "/expertise/")]
    title = "SEO, GEO & AI Search expertise | Piyush Kumar Soni"
    desc = "Piyush Kumar Soni's expertise across technical SEO, organic growth, GEO/AEO, AI Search, LLM and RAG workflows, automation and SEO team leadership, plus the tools he uses."
    body = page_head("Expertise", "Six areas I work in every day, and the tools I use for them. Search fundamentals come first; AI work is built on top of them.", crumbs, "What I do") + \
        section(None, "Areas of expertise", expertise_cards(full=True)) + \
        section("tools", "Tools", tools_html(), lede="A short list of tools I use regularly, grouped by job.") + \
        section(None, "See it in practice", '<p class="muted">The best evidence is the work itself.</p><div class="btn-row"><a class="btn btn-primary" href="/case-studies/">Case studies</a><a class="btn" href="/projects/">Projects</a></div>')
    render("/expertise/", title, desc, body, "expertise", webpage("/expertise/", title, desc, "WebPage", crumbs))


def build_projects():
    crumbs = [("Home", "/"), ("Projects", "/projects/")]
    title = "SEO, AI & Automation Projects | Piyush Kumar Soni"
    desc = "Explore SEO, AI Search, browser extension, RAG, automation, and product projects built by Piyush Kumar Soni."
    minor = "".join(f'''<article class="card"><div class="meta"><span class="cat">{esc(m["cat"])}</span>{pill(m["status"])}</div>
<h3>{esc(m["title"])}</h3><p>{esc(m["short"])}</p><div class="card-foot">{ext_a("Open on Hugging Face", m["url"], m["track"])}</div></article>''' for m in MINOR_PROJECTS)
    body = page_head("Projects", "Tools and products I have built or am building. Public projects link to their source or live demo; private ones are documented here without exposing code.", crumbs, "Proof of work") + \
        section(None, "All projects", '<div class="grid">' + "".join(project_card(p, i) for i, p in enumerate(PROJECTS)) + "</div>") + \
        section(None, "Smaller experiments", f'<div class="grid">{minor}</div>') + \
        section(None, "More on GitHub and Hugging Face", f'<div class="btn-row">{ext_a("GitHub repositories", L["github_repos"], "github-repos", "btn")}{ext_a("Hugging Face profile", L["huggingface"], "huggingface", "btn")}</div>')
    items = [{"@type": "ListItem", "position": i + 1, "url": f"{BASE}/projects/{p['slug']}/", "name": p["title"]} for i, p in enumerate(PROJECTS)]
    render("/projects/", title, desc, body, "projects",
           webpage("/projects/", title, desc, "CollectionPage", crumbs, [{"@type": "ItemList", "itemListElement": items}]))


def stack_html():
    groups = [("Frontend", "Next.js 14 · App Router · Tailwind CSS · PWA"),
              ("Backend", "Supabase · PostgreSQL · Auth · Storage · Edge Functions · pgvector"),
              ("AI", "Gemini 2.0 Flash (primary) · Groq Llama 4 Scout (fallback)"),
              ("Payments", "Razorpay"),
              ("Architecture", "pnpm · Turborepo · Monorepo")]
    return '<div class="stack">' + "".join(f"<div><h3>{g}</h3><p>{v}</p></div>" for g, v in groups) + "</div>"


def project_schema(p, path):
    kind = p.get("schema")
    if kind == "code":
        return [{"@type": "SoftwareSourceCode", "name": p["title"], "description": p["short"], "url": BASE + path,
                 "codeRepository": L["seo_master"], "license": "https://opensource.org/licenses/MIT",
                 "programmingLanguage": "Markdown", "author": {"@id": PERSON_ID}, "version": "1.0.3"}]
    if kind == "browser":
        return [{"@type": "SoftwareApplication", "name": "GBP Audit + AI Visibility", "description": p["short"],
                 "applicationCategory": "BrowserApplication", "operatingSystem": "Firefox", "url": L["firefox"],
                 "softwareVersion": "1.0.0", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                 "author": {"@id": PERSON_ID}, "publisher": {"@type": "Organization", "name": "Lucky Digitals", "url": L["lucky"]}}]
    if kind == "web":
        return [{"@type": "SoftwareApplication", "name": p["title"], "description": p["short"],
                 "applicationCategory": "WebApplication", "operatingSystem": "Any (web browser)",
                 "url": p["links"][0][1], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                 "author": {"@id": PERSON_ID}}]
    return []


def build_project_pages():
    cases = {c["slug"]: c for c in CASES}
    for p in PROJECTS:
        path = f"/projects/{p['slug']}/"
        crumbs = [("Home", "/"), ("Projects", "/projects/"), (p["title"], path)]
        links = "".join(ext_a(l, u, t, "btn btn-primary" if i == 0 else "btn") for i, (l, u, t, _) in enumerate(p["links"]))
        if p.get("case"):
            links += f'<a class="btn" href="/case-studies/{p["case"]}/" data-track="case-from-project">Read the case study</a>'
        btns = f'<div class="btn-row">{links}</div>' if links else ""
        secs = ""
        for h, html in p["sections"]:
            secs += f"<h2>{esc(h)}</h2>" + (stack_html() if html == "STACK" else html)
        extra = "".join(f"<p>{ext_a(l, u, 'article-click')}</p>" for l, u in p.get("extra_links", []))
        related = [q for q in PROJECTS if q["slug"] != p["slug"]][:3]
        rel = "".join(f'<li><a href="/projects/{q["slug"]}/">{esc(q["title"])}</a></li>' for q in related)
        facts = f'''<dl class="facts">
  <div><dt>Status</dt><dd>{esc(p["status"][0])}</dd></div>
  <div><dt>Type</dt><dd>{esc(p["cat"])}</dd></div>
  <div><dt>Role</dt><dd>{esc(p["role"].split(".")[0])}</dd></div>
</dl>'''
        tech = "".join(f"<li>{esc(t)}</li>" for t in p["tech"])
        body = page_head(p["title"], esc(p["short"]), crumbs, p["cat"], btns) + f'''
<div class="wrap layout">
  <div class="prose">
    <h2>Problem</h2><p>{esc(p["problem"])}</p>
    <h2>Solution</h2><p>{esc(p["solution"])}</p>
    <h2>My role</h2><p>{esc(p["role"])}</p>
    {secs}
    {"<h2>Further reading</h2>" + extra if extra else ""}
  </div>
  <aside class="aside" aria-label="Project details">
    <div class="card"><h2>At a glance</h2>{facts}</div>
    <div class="card"><h2>Key technologies</h2><ul class="tags">{tech}</ul></div>
    <div class="card"><h2>Other projects</h2><ul class="small">{rel}</ul><p class="small" style="margin:0"><a href="/projects/">All projects →</a></p></div>
  </aside>
</div>'''
        render(path, p["meta_title"], p["meta_desc"], body, "projects",
               webpage(path, p["meta_title"], p["meta_desc"], "WebPage", crumbs, project_schema(p, path)))


def build_cases():
    crumbs = [("Home", "/"), ("Case studies", "/case-studies/")]
    title = "SEO & AI Search Case Studies | Piyush Kumar Soni"
    desc = "Technical SEO, organic growth, AI Search, GEO/AEO, automation, and product-development case studies by Piyush Kumar Soni."
    body = page_head("Case studies", "How the work was done: the problem, the thinking, what shipped and what it taught me. Client names are left out where work is confidential.", crumbs, "Case studies") + \
        section(None, "All case studies", '<div class="grid grid-2">' + "".join(case_card(c) for c in CASES) + "</div>")
    items = [{"@type": "ListItem", "position": i + 1, "url": f"{BASE}/case-studies/{c['slug']}/", "name": c["title"]} for i, c in enumerate(CASES)]
    render("/case-studies/", title, desc, body, "cases",
           webpage("/case-studies/", title, desc, "CollectionPage", crumbs, [{"@type": "ItemList", "itemListElement": items}]))

    projects = {p["slug"]: p for p in PROJECTS}
    for c in CASES:
        path = f"/case-studies/{c['slug']}/"
        crumbs = [("Home", "/"), ("Case studies", "/case-studies/"), (c["title"], path)]
        res = ""
        if c["results"]:
            lis = "".join(f'<li class="stat"><b>{v}</b><span>{l}</span></li>' for v, l in c["results"])
            res = f'<h2>Results</h2><ul class="stats" style="grid-template-columns:repeat(auto-fill,minmax(150px,1fr))">{lis}</ul>'
        secs = ""
        for h, html in c["body"]:
            if h == "Lessons" and res:
                secs += res
                res = ""
            secs += f"<h2>{esc(h)}</h2>{html}"
        secs += res
        side = ""
        if c["project"]:
            p = projects[c["project"]]
            side = f'<div class="card"><h2>Related project</h2><p class="small"><a href="/projects/{p["slug"]}/">{esc(p["title"])}</a></p><p class="small muted" style="margin:0">{esc(p["status"][0])}</p></div>'
        others = "".join(f'<li><a href="/case-studies/{o["slug"]}/">{esc(o["title"])}</a></li>' for o in CASES if o["slug"] != c["slug"])
        body = page_head(c["title"], esc(c["intro"]), crumbs, "Case study") + f'''
<div class="wrap layout">
  <article class="prose">{secs}</article>
  <aside class="aside" aria-label="Related">
    {side}
    <div class="card"><h2>More case studies</h2><ul class="small">{others}</ul></div>
    <div class="card"><h2>Work with me</h2><p class="small">Open to SEO leadership and AI Search roles.</p>{ext_a("Connect on LinkedIn", L["linkedin"], "linkedin-case", "btn btn-sm")}</div>
  </aside>
</div>'''
        render(path, c["meta_title"], c["meta_desc"], body, "cases",
               webpage(path, c["meta_title"], c["meta_desc"], "WebPage", crumbs), og_type="article")


def build_writing():
    crumbs = [("Home", "/"), ("Writing", "/writing/")]
    title = "Articles on SEO, GEO, AI Search & RAG | Piyush Kumar Soni"
    desc = "Articles by Piyush Kumar Soni on technical SEO, GEO and AI Search, LLM and RAG development, and SEO automation, published on Substack, DEV.to, Hashnode and Medium."
    groups = "".join(section(None, esc(g), '<ul class="article-list">' + "".join(article_item(a) for a in arts) + "</ul>") for g, arts in ARTICLES.items())
    pubs = f'''<div class="btn-row">{ext_a("Substack: From SEO to AI", L["substack"], "substack", "btn")}{ext_a("Medium", L["medium"], "medium", "btn")}{ext_a("DEV.to", L["devto"], "devto", "btn")}{ext_a("Hashnode", L["hashnode"], "hashnode", "btn")}</div>'''
    body = page_head("Writing", "What I have learned doing the work, published across my newsletter and developer blogs. Links open on the original platform.", crumbs, "Articles") + \
        groups + section(None, "Follow the writing", '<p class="muted">New posts go to the <strong>From SEO to AI</strong> newsletter first.</p>' + pubs)
    render("/writing/", title, desc, body, "writing", webpage("/writing/", title, desc, "CollectionPage", crumbs))


def build_resume():
    crumbs = [("Home", "/"), ("Resume", "/resume/")]
    title = "Resume: SEO & AI Search Leader | Piyush Kumar Soni"
    desc = "Resume of Piyush Kumar Soni, SEO & AI Search leader since 2011: technical SEO, organic growth, GEO/AEO, LLM/RAG workflows, automation and team leadership."
    if HAS_RESUME:
        dl = f'<div class="btn-row" id="download"><a class="btn btn-primary" href="/{RESUME_FILE}" download data-track="resume-download">Download resume (DOCX)</a><button class="btn" type="button" onclick="window.print()">Print or save as PDF</button></div>'
    else:
        dl = (f'<div class="btn-row" id="download"><span class="btn btn-primary" aria-disabled="true">Download resume (DOCX): file coming soon</span>'
              f'<button class="btn" type="button" onclick="window.print()">Print or save as PDF</button></div>'
              f'<!-- PLACEHOLDER: add /{RESUME_FILE} and rebuild to enable the download button -->')
    jobs = "".join(f'<div class="job"><h3>{esc(t)}</h3><p class="small muted" style="margin:0">{esc(o)} · <span class="when">{w}</span></p><ul>' +
                   "".join(f"<li>{esc(b)}</li>" for b in bs) + "</ul></div>" for w, t, o, bs in EXPERIENCE)
    core = "".join(f"<li><strong>{esc(t)}:</strong> {esc(', '.join(i[:6]))}</li>" for t, _, i in EXPERTISE)
    projs = "".join(f'<li><a href="/projects/{p["slug"]}/">{esc(p["title"])}</a>: {esc(p["short"])}</li>' for p in PROJECTS)
    edu = "".join(f"<li><strong>{esc(d)}</strong>, {esc(s)} ({y})</li>" for y, d, s in EDUCATION)
    tools = "".join(f"<li><strong>{esc(g)}:</strong> {esc(', '.join(i))}</li>" for g, i in TOOLS)
    profs = "".join(f"<li>{n}: {ext_a(u.replace('https://', '').replace('www.', '').rstrip('/'), u)}</li>" for n, u in
                    [("LinkedIn", L["linkedin"]), ("GitHub", L["github"]), ("Hugging Face", L["huggingface"]), ("Substack", L["substack"]), ("Portfolio", BASE)])
    body = page_head(NAME, f"<strong>{ROLE}</strong> · Kanpur, Uttar Pradesh, India", crumbs, "Resume", dl) + f'''
<div class="wrap" style="padding-top:36px;padding-bottom:72px">
  <div class="prose resume">
    <h2 style="margin-top:0">Professional summary</h2>
    <p>SEO and AI Search leader with experience since 2011 across Technical SEO, organic growth, content strategy, site architecture, structured data, internal linking, analytics, CMS-based web delivery, GEO/AEO, LLM/RAG workflows, automation, and team leadership.</p>
    <h2>Core expertise</h2><ul>{core}</ul>
    <h2>Experience</h2>{jobs}
    <h2>Projects</h2><ul>{projs}</ul>
    <h2>Education</h2><ul>{edu}</ul>
    <h2>Tools</h2><ul>{tools}</ul>
    <h2>Profiles</h2><ul>{profs}</ul>
  </div>
</div>'''
    render("/resume/", title, desc, body, "resume", webpage("/resume/", title, desc, "ProfilePage", crumbs))


def build_contact():
    crumbs = [("Home", "/"), ("Contact", "/contact/")]
    title = "Contact Piyush Kumar Soni | SEO & AI Search"
    desc = "Contact Piyush Kumar Soni about SEO, AI Search, organic growth, automation or leadership roles, and find his LinkedIn, GitHub, Hugging Face and writing profiles."
    hub = [("Professional", [("LinkedIn", L["linkedin"]), ("Wellfound", L["wellfound"]), ("About.me", L["aboutme"])]),
           ("Development", [("GitHub", L["github"]), ("Hugging Face", L["huggingface"])]),
           ("Writing", [("Substack", L["substack"]), ("Medium", L["medium"]), ("DEV.to", L["devto"]), ("Hashnode", L["hashnode"])]),
           ("Community", [("Quora", L["quora"]), ("Reddit", L["reddit"]), ("Bluesky", L["bluesky"]), ("Instagram", L["instagram"])])]
    cards = ""
    for g, items in hub:
        lis = "".join(f'<li><a href="{u}" {EXT} data-track="profile-{n.lower().replace(".", "").replace(" ", "")}">{n}<span aria-hidden="true">↗</span><span class="sr-only"> (opens in a new tab)</span></a></li>' for n, u in items)
        cards += f'<div class="card"><h3>{g}</h3><ul>{lis}</ul></div>'
    body = page_head("Let's connect", "Interested in discussing SEO, AI Search, organic growth, automation, product ideas, or relevant leadership opportunities? Connect with me through LinkedIn or explore my work on GitHub.", crumbs, "Contact", contact_buttons()) + \
        section("profiles", "Where to find me", f'<div class="hub">{cards}</div>', lede="LinkedIn is the fastest way to reach me. The other profiles hold my code, tools and writing.") + \
        section(None, "Open to opportunities", opp_html())
    render("/contact/", title, desc, body, "contact", webpage("/contact/", title, desc, "ContactPage", crumbs))


def build_404():
    body = page_head("Page not found", "The page you were looking for has moved or does not exist.") + \
        '<div class="wrap" style="padding:36px 20px 72px"><div class="btn-row" style="margin-top:0"><a class="btn btn-primary" href="/">Home</a><a class="btn" href="/projects/">Projects</a><a class="btn" href="/case-studies/">Case studies</a><a class="btn" href="/contact/">Contact</a></div></div>'
    render("/404.html", "Page not found | Piyush Kumar Soni", "This page does not exist on the portfolio of Piyush Kumar Soni.", body, None, None, noindex=True)


def build_seo_files():
    urls = "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod></url>\n" for p, idx in PAGES if idx)
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write(f"# Search engines and AI crawlers are welcome.\nUser-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {BASE}/sitemap.xml\n")


def build_assets():
    fav = os.path.join(ROOT, "assets/img/favicon.svg")
    with open(fav, "w") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0b1220"/>'
                '<rect x="2" y="2" width="60" height="60" rx="12" fill="none" stroke="#5b9dff" stroke-width="3"/>'
                '<text x="32" y="42" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="24" fill="#e9eef7">PKS</text></svg>')
    og = os.path.join(ROOT, "assets/img/og-default.png")
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (1200, 630), "#0b1220")
        d = ImageDraw.Draw(img)
        def font(size, bold=True):
            for p in ["/usr/share/fonts/opentype/inter/Inter-Bold.otf" if bold else "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
                      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
                if os.path.exists(p):
                    return ImageFont.truetype(p, size)
            return ImageFont.load_default()
        d.rectangle([0, 0, 1200, 8], fill="#5b9dff")
        d.text((80, 190), NAME, font=font(84), fill="#e9eef7")
        d.text((80, 300), ROLE, font=font(48), fill="#5b9dff")
        d.text((80, 380), "Technical SEO · GEO/AEO · LLM/RAG · Automation", font=font(34, False), fill="#a3afc4")
        d.text((80, 520), "piyushsoni-ai.github.io", font=font(28, False), fill="#7f8ba3")
        img.save(og, optimize=True)
    except Exception as e:  # keep building even without Pillow
        print("OG image skipped:", e)


if __name__ == "__main__":
    build_assets()
    build_home(); build_about(); build_expertise(); build_projects(); build_project_pages()
    build_cases(); build_writing(); build_resume(); build_contact(); build_404()
    build_seo_files()
    print(f"Built {len(PAGES)} pages. Photo: {'yes' if HAS_PHOTO else 'placeholder'}. Resume file: {'yes' if HAS_RESUME else 'placeholder'}.")
