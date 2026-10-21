#!/usr/bin/env python3
"""Baut die statischen Seiten aus src/ zusammen.

    python3 tools/build.py

- Seiteninhalte:   src/pages/<name>.html   (nur der Inhalt von <main>)
- Gemeinsame Teile: src/partials/<name>.html, eingebunden mit  <!-- @include name -->
- Kopf, Navigation, Fuß und SEO-Angaben (Titel, Beschreibung, Canonical, Open Graph,
  strukturierte Daten) kommen aus diesem Skript.
Ausgabe: <name>.html im Projektordner sowie sitemap.xml und robots.txt.
Die erzeugten Dateien nicht von Hand bearbeiten, sondern src/ ändern und neu bauen.
"""
import json
import re
from datetime import date
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

# ---------------------------------------------------------------------------
# Domain und Kontakt-E-Mail
# SITE_URL: Hauptadresse der Website (Canonical, Sitemap, Google-Daten).
# MAIL_LIVE: erst auf True setzen, wenn eine Test-Mail an kontakt@physio-buescher.de
#            im Gmail-Postfach angekommen ist. Dann neu bauen.
# ---------------------------------------------------------------------------
SITE_URL = "https://physio-buescher.de"
MAIL_LIVE = True
EMAIL = "kontakt@physio-buescher.de" if MAIL_LIVE else "physioteambuescher@gmail.com"
# Empfänger des Kontaktformulars (FormSubmit ist für diese Adresse freigeschaltet)
FORM_TARGET = "physioteambuescher@gmail.com"

PERSON = {
    "@type": "Person",
    "@id": f"{SITE_URL}/referent#person",
    "name": "Thorsten Büscher",
    "jobTitle": "Physiotherapeut, Sportphysiotherapeut DOSB, Referent für Fortbildungen",
    "sameAs": ["https://corpus-as.de/thorsten-buescher/"],
    "email": f"mailto:{EMAIL}",
    "telephone": "+49 163 4439593",
    "image": f"{SITE_URL}/assets/img/thorsten-portrait.jpg",
    "url": f"{SITE_URL}/referent",
    "worksFor": {"@type": "Organization", "name": "corpus as", "address": {"@type": "PostalAddress", "addressLocality": "Köln", "addressCountry": "DE"}},
    "workLocation": {"@type": "Place", "name": "Köln"},
    "address": {"@type": "PostalAddress", "streetAddress": "Georgshof 1", "postalCode": "51503", "addressLocality": "Rösrath", "addressCountry": "DE"},
    "hasCredential": [{"@type": "EducationalOccupationalCredential", "name": n} for n in [
        "Physiotherapeut", "Manuelle Therapie", "Sportphysiotherapeut DOSB", "Instructor Kinesiologisches Taping",
        "Ergonomie-Instructor", "Golf-Physio-Trainer", "PINO Headinstructor"]],
    "knowsAbout": ["Sportphysiotherapie", "Manuelle Therapie", "Return to Sport", "Kinesiologisches Taping",
                   "Dry Needling", "Flossing", "Blood Flow Restriction Training", "Funktionelles Training",
                   "Ergonomie", "Golf-Physiotherapie"],
}

COURSE = {
    "@type": "Course",
    "@id": f"{SITE_URL}/kurse/sportphysiotherapie-neu-gedacht#kurs",
    "name": "Sportphysiotherapie neu gedacht. Von der Verletzung zur Performance",
    "description": ("Zweitägige Fortbildung für Physiotherapeut:innen, die Sportphysiotherapie von der akuten "
                    "Verletzungsversorgung bis zur Rückkehr in Training, Wettkampf und Performance denkt: "
                    "Assess, Treat, Train, Return, Perform."),
    "inLanguage": "de",
    "url": f"{SITE_URL}/kurse/sportphysiotherapie-neu-gedacht",
    "provider": {"@id": f"{SITE_URL}/referent#person"},
    "instructor": {"@id": f"{SITE_URL}/referent#person"},
    "audience": {"@type": "Audience", "audienceType": "Physiotherapeut:innen aus Praxis, Klinik und Sport"},
    "teaches": ["Funktionelle Diagnostik", "Manuelle und myofasziale Techniken", "Dry Needling",
                "Kinesiologisches Taping und Sporttaping", "Flossing", "Functional Therapy Training",
                "Blood Flow Restriction Training", "Return to Sport", "Return to Performance"],
    "timeRequired": "P2D",
    "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "onsite", "courseWorkload": "P2D",
                          "location": {"@type": "Place", "name": "Bei der ausrichtenden Akademie, in Deutschland und international"}},
}

COURSE_TAPING = {
    "@type": "Course",
    "@id": f"{SITE_URL}/kurse/kinesio-taping#kurs",
    "name": "Kinesio-Taping kompakt: Grundtechniken und Anwendungsmöglichkeiten",
    "description": ("Eintägiger PINO-Kompaktkurs mit 10 Unterrichtseinheiten: kinesiologisches Taping aus funktionell-anatomischer, "
                    "biomechanischer und orthopädischer Sicht, mit hohem Praxisanteil."),
    "inLanguage": "de",
    "url": f"{SITE_URL}/kurse/kinesio-taping",
    "provider": {"@id": f"{SITE_URL}/referent#person"},
    "instructor": {"@id": f"{SITE_URL}/referent#person"},
    "timeRequired": "P1D",
    "audience": {"@type": "Audience", "audienceType": "Physiotherapeut:innen, Masseur:innen, Ergotherapeut:innen, Heilpraktiker:innen, Ärzt:innen"},
    "teaches": ["Kinesiologisches Taping", "Muskelanlagen", "Ligamentanlagen", "Korrekturtechniken", "Lymphtaping", "Funktionelle Befunderhebung"],
    "coursePrerequisites": "Keine Vorkenntnisse erforderlich",
    "educationalCredentialAwarded": "Teilnahmebescheinigung mit 10 Unterrichtseinheiten",
    "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "onsite", "courseWorkload": "PT10H"},
}

COURSE_PINOFIT = {
    "@type": "Course",
    "@id": f"{SITE_URL}/kurse/bandagen-flossing-bfr#kurs",
    "name": "Bandagen, Flossing und BFR: PINOFIT Kombikurs",
    "description": ("Tageskurs, der PINOFIT Bandagen, Blood Flow Restriction Training und Flossing zu einem Konzept für "
                    "Therapie, Rehabilitation, Training und Prävention verbindet."),
    "inLanguage": "de",
    "url": f"{SITE_URL}/kurse/bandagen-flossing-bfr",
    "provider": {"@id": f"{SITE_URL}/referent#person"},
    "instructor": {"@id": f"{SITE_URL}/referent#person"},
    "timeRequired": "P1D",
    "audience": {"@type": "Audience", "audienceType": "Physiotherapeut:innen, Sportwissenschaftler:innen, Personal- und Fitnesstrainer:innen, Ärzt:innen"},
    "teaches": ["Blood Flow Restriction Training", "Okklusionstraining", "Flossing", "Funktionelle Bandagen"],
    "educationalCredentialAwarded": "Teilnahmebescheinigung",
    "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "onsite", "courseWorkload": "P1D"},
}

NAV = [("/kurse", "Kurse", ("kurse",)), ("/referent", "Referent", ("referent",)), ("/akademien", "Für Akademien", ("akademien",))]


def crumbs(*items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE_URL}{p}"} for i, (n, p) in enumerate(items)]}


PAGES = {
    "index": dict(
        path="/",
        title="Thorsten Büscher: Referent Kinesio-Taping, BFR & Sportphysio",
        description=("Fortbildungen mit Thorsten Büscher, Sportphysiotherapeut DOSB: Return to Sport (2 Tage), Kinesio-Taping Kurs, BFR & Flossing (je 1 Tag). DE, AT, CH."),
        og_image="/assets/og-image.jpg",
        jsonld=[{"@type": "WebSite", "name": "Sportphysiotherapie neu gedacht", "url": f"{SITE_URL}/", "inLanguage": "de"},
                COURSE, COURSE_TAPING, COURSE_PINOFIT, PERSON],
        priority="1.0",
    ),
    "referent": dict(
        path="/referent",
        title="Thorsten Büscher: Physiotherapeut & PINO Head Instructor",
        description=("Thorsten Büscher, Sportphysiotherapeut DOSB und PINO Head Instructor: Referent für Kinesio-Taping, BFR und Return to Sport. 5 Jahre Olympiastützpunkt Köln."),
        og_image="/assets/img/thorsten-portrait.jpg",
        jsonld=[{"@type": "ProfilePage", "mainEntity": PERSON},
                crumbs(("Startseite", "/"), ("Referent", "/referent"))],
        priority="0.8",
    ),
    "kurse": dict(
        path="/kurse",
        title="Fortbildungen: Kinesio-Taping, BFR, Flossing & Sportphysio",
        description=("Drei Fortbildungen für Physiotherapeut:innen: Return to Sport (2 Tage), Kinesio-Taping Kurs (10 UE) und BFR, Flossing & Bandagen. Auch als Inhouse-Schulung."),
        og_image="/assets/img/flyer-kinesio-taping-kompakt-web.jpg",
        jsonld=[{"@type": "ItemList", "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "item": c} for i, c in enumerate([COURSE, COURSE_TAPING, COURSE_PINOFIT])]},
                crumbs(("Startseite", "/"), ("Kurse", "/kurse"))],
        priority="0.9",
    ),
    "kurse/sportphysiotherapie-neu-gedacht": dict(
        path="/kurse/sportphysiotherapie-neu-gedacht",
        title="Sportphysiotherapie Fortbildung: Return to Sport (2 Tage)",
        description=("Return to Sport Fortbildung in 2 Tagen: Diagnostik, Dry Needling, Taping, Flossing, BFR und Return to Performance. Referent: 5 Jahre Olympiastützpunkt Köln."),
        og_image="/assets/img/flyer-sportphysiotherapie-web.jpg",
        jsonld=[COURSE, crumbs(("Startseite", "/"), ("Kurse", "/kurse"), ("Sportphysiotherapie neu gedacht", "/kurse/sportphysiotherapie-neu-gedacht"))],
        priority="0.9",
    ),
    "kurse/kinesio-taping": dict(
        path="/kurse/kinesio-taping",
        title="Kinesio-Taping Kurs kompakt: 1 Tag, 10 UE | Thorsten Büscher",
        description=("Kinesio-Taping Kurs für Physio- und Ergotherapeut:innen: 1 Tag, 10 UE, Tape inklusive, Zertifikat. Muskel-, Ligament- und Lymphanlagen. Auch inhouse."),
        og_image="/assets/img/flyer-kinesio-taping-kompakt-web.jpg",
        jsonld=[COURSE_TAPING, crumbs(("Startseite", "/"), ("Kurse", "/kurse"), ("Kinesio-Taping kompakt", "/kurse/kinesio-taping"))],
        priority="0.9",
    ),
    "kurse/bandagen-flossing-bfr": dict(
        path="/kurse/bandagen-flossing-bfr",
        title="BFR, Flossing & Bandagen Fortbildung | PINOFIT 1-Tages-Kurs",
        description=("BFR Fortbildung für Physios und Trainer: Blood Flow Restriction, Flossing und PINOFIT Bandagen an einem Tag. Dosierung, Sicherheit, Material von PINO."),
        og_image="/assets/img/flyer-pinofit-kombikurs-web.jpg",
        jsonld=[COURSE_PINOFIT, crumbs(("Startseite", "/"), ("Kurse", "/kurse"), ("Bandagen, Flossing & BFR", "/kurse/bandagen-flossing-bfr"))],
        priority="0.9",
    ),
    "akademien": dict(
        path="/akademien",
        title="Referent buchen: Inhouse-Fortbildung Taping, BFR, Sportphysio",
        description=("Referent für Ihr Fortbildungsprogramm oder als Inhouse-Schulung: Sportphysiotherapie, Kinesio-Taping, BFR und Flossing. Deutschland, Österreich, Schweiz."),
        og_image="/assets/og-image.jpg",
        jsonld=[COURSE, COURSE_TAPING, COURSE_PINOFIT, crumbs(("Startseite", "/"), ("Für Akademien", "/akademien"))],
        priority="0.9",
    ),
    "impressum": dict(path="/impressum", title="Impressum | Thorsten Büscher Sportphysiotherapie",
                      description="Impressum", noindex=True),
    "datenschutz": dict(path="/datenschutz", title="Datenschutz | Thorsten Büscher Sportphysiotherapie",
                        description="Datenschutzerklärung", noindex=True),
}

LAYOUT = """<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
{robots}  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#0b1426">
  <meta name="author" content="Thorsten Büscher">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="de_DE">
  <meta property="og:site_name" content="Sportphysiotherapie neu gedacht">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="/assets/fonts/archivo-latin-standard-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css">
{jsonld}</head>
<body class="page-{cls}">
  <a class="skip" href="#main">Zum Inhalt springen</a>

  <header class="site-header" id="top">
    <div class="wrap header-inner">
      <a class="brand" href="/" aria-label="Startseite">
        <span class="brand-name">Thorsten Büscher</span>
        <span class="brand-sub">Sportphysiotherapie</span>
      </a>
      <nav class="nav" aria-label="Hauptnavigation">
        <button class="nav-toggle" aria-expanded="false" aria-controls="nav-list">
          <span class="sr-only">Menü</span><span class="bar"></span><span class="bar"></span>
        </button>
        <ul id="nav-list" class="nav-list">
{nav}
          <li><a href="{cta}" class="btn btn-tape">Termin abstimmen</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main id="main">
{body}  </main>

  <footer class="site-footer">
    <div class="wrap footer-inner">
      <p class="marker">Therapie trifft Training.</p>
      <p>© <span id="year">{year}</span> Thorsten Büscher</p>
      <nav aria-label="Weitere Seiten"><a href="/kurse">Kurse</a><a href="/kurse/sportphysiotherapie-neu-gedacht">Sportphysiotherapie</a><a href="/kurse/kinesio-taping">Kinesio-Taping</a><a href="/kurse/bandagen-flossing-bfr">Bandagen, Flossing &amp; BFR</a><a href="/referent">Referent</a><a href="/akademien">Für Akademien</a><a href="/impressum">Impressum</a><a href="/datenschutz">Datenschutz</a></nav>
    </div>
  </footer>

  <script src="/main.js" defer></script>
</body>
</html>
"""


def include(text):
    def repl(m):
        return (SRC / "partials" / f"{m.group(1)}.html").read_text()
    return re.sub(r"[ \t]*<!-- @include ([\w-]+) -->\n?", repl, text)


def build():
    urls = []
    for name, p in PAGES.items():
        body = include((SRC / "pages" / f"{name}.html").read_text())
        has_contact = 'id="kontakt"' in body
        nav = "\n".join(
            f'          <li><a href="{href}"{" aria-current=\"page\"" if name.split("/")[0] in keys else ""}>{label}</a></li>'
            for href, label, keys in NAV)
        canonical = SITE_URL + p["path"]
        blocks = ""
        graph = list(p.get("jsonld", []))
        faqs = re.findall(r'<details class="faq-item"><summary>(.*?)</summary><div>(.*?)</div></details>', body, re.S)
        if faqs:
            graph.append({"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": unescape(q), "acceptedAnswer": {"@type": "Answer", "text": unescape(re.sub(r"<[^>]+>", "", a)).strip()}}
                for q, a in faqs]})
        if graph:
            data = {"@context": "https://schema.org", "@graph": graph}
            blocks = ('  <script type="application/ld+json">\n'
                      + json.dumps(data, ensure_ascii=False, indent=2) + "\n  </script>\n")
        html = LAYOUT.format(
            name=name, cls=name.replace("/", "-"), title=escape(p["title"]), description=escape(p["description"]),
            robots='  <meta name="robots" content="noindex, follow">\n' if p.get("noindex") else "",
            canonical=canonical, og_image=SITE_URL + p.get("og_image", "/assets/og-image.jpg"),
            jsonld=blocks, nav=nav, cta="#kontakt" if has_contact else "/#kontakt",
            body=body, year=date.today().year)
        html = html.replace("@@FORM_TARGET@@", FORM_TARGET).replace("@@EMAIL@@", EMAIL)
        out = ROOT / f"{name}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        if not p.get("noindex"):
            urls.append((canonical, p.get("priority", "0.5")))
        print(f"  {name}.html")

    today = date.today().isoformat()
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>" for u, pr in urls]
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("  sitemap.xml, robots.txt")


if __name__ == "__main__":
    build()
