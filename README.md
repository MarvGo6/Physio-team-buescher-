# Sportphysiotherapie neu gedacht – Homepage

Landingpage zum 2-Tages-Kurs „Sportphysiotherapie neu gedacht – Von der Verletzung zur Performance“
von Thorsten Büscher, ausgerichtet auf Fortbildungsschulen und Akademien.

- Statisches HTML/CSS/JS, mehrere Seiten: Startseite, `/inhalte`, `/referent`, `/akademien`, Impressum, Datenschutz.
- Seiten werden aus `src/` zusammengesetzt: `python3 tools/build.py` (erzeugt die `*.html` im Hauptordner,
  `sitemap.xml` und `robots.txt`). Gemeinsame Bausteine wie „Stimmen“ und „Kontakt“ liegen in `src/partials/`
  und erscheinen dadurch auf allen Seiten. Erzeugte `*.html` nicht direkt bearbeiten.
- Titel, Beschreibungen und strukturierte Daten (SEO) stehen in `tools/build.py` (`SITE_URL` = Hauptadresse).
- Schriften lokal eingebunden (`assets/fonts`: Archivo variabel, Permanent Marker), keine Google-Verbindung, keine Cookies.
- Kontaktformular öffnet das E-Mail-Programm (mailto) mit vorausgefüllter Anfrage.

## Offene Punkte vor dem Livegang
- Rezensionen: Abschnitt „Stimmen“ (`src/partials/stimmen.html`) enthält Platzhalter. Nur echte, freigegebene Rückmeldungen eintragen
  (Anleitung im HTML-Kommentar dort).
- Fotos in `assets/img/` und Video in `assets/video/` stammen von Thorsten Büscher. Vor dem Livegang klären: Einverständnis der abgebildeten
  Patient:innen/Teilnehmenden und Bildrechte (z. B. Screenshots aus Videos von PINO).
- Flyer als PDF bereitstellen (`assets/`) und Download-Link in `index.html` anpassen.

## Kursflyer
- Vorlage: `tools/flyer/flyer.html` (Texte im Objekt `KURSE`, Aufruf `?kurs=taping` bzw. `?kurs=pinofit`).
- Bilder und Druck-PDFs neu erzeugen: lokalen Server im Projektordner auf Port 8766 starten, dann `node tools/flyer/render.js`
  (braucht Playwright). Ergebnis: `assets/flyer-*.jpg` und `assets/flyer-*.pdf`; Vorschaubilder für die Seite liegen in `assets/img/flyer-*-web.jpg`.

## Hosting
- Läuft auf Vercel (`vercel.json`) und genauso auf Cloudflare Pages (`_headers`; Build-Befehl leer lassen,
  Ausgabeordner `/`). Saubere URLs wie `/inhalte` funktionieren auf beiden ohne Zusatzkonfiguration.
- Domain `physio-buescher.de` (INWX, INWX-Nameserver). DNS bei INWX: A `@` und `www` → `76.76.21.21` (Vercel),
  MX `mx1/mx2.forwardemail.net`, TXT `forward-email=kontakt:…` (Weiterleitung an Gmail) und SPF.
- Vercel baut bei jedem Deployment selbst: Build-Befehl `python3 tools/build.py`, Ausgabe `.`.
- Kontakt-E-Mail: in `tools/build.py` `MAIL_LIVE = True` setzen, sobald die Weiterleitung getestet ist.

## Lokal ansehen
```
python3 -m http.server 8000
```
