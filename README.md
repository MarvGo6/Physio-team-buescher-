# Sportphysiotherapie neu gedacht – Homepage

Landingpage zum 2-Tages-Kurs „Sportphysiotherapie neu gedacht – Von der Verletzung zur Performance“
von Thorsten Büscher, ausgerichtet auf Fortbildungsschulen und Akademien.

- Statisches HTML/CSS/JS, mehrere Seiten: Startseite, `/inhalte`, `/referent`, `/akademien`, Impressum, Datenschutz.
- Seiten werden aus `src/` zusammengesetzt: `python3 tools/build.py` (erzeugt die `*.html` im Hauptordner,
  `sitemap.xml` und `robots.txt`). Gemeinsame Bausteine wie „Stimmen“ und „Kontakt“ liegen in `src/partials/`
  und erscheinen dadurch auf allen Seiten. Erzeugte `*.html` nicht direkt bearbeiten.
- Titel, Beschreibungen und strukturierte Daten (SEO) stehen in `tools/build.py`. Bei eigener Domain dort `SITE_URL` ändern.
- Schriften lokal eingebunden (`assets/fonts`: Archivo variabel, Permanent Marker), keine Google-Verbindung, keine Cookies.
- Kontaktformular öffnet das E-Mail-Programm (mailto) mit vorausgefüllter Anfrage.

## Offene Punkte vor dem Livegang
- Rezensionen: Abschnitt „Stimmen“ (`src/partials/stimmen.html`) enthält Platzhalter. Nur echte, freigegebene Rückmeldungen eintragen
  (Anleitung im HTML-Kommentar dort).
- Impressum/Datenschutz: ladungsfähige Anschrift ergänzen (`impressum.html`, `datenschutz.html`).
- Fotos in `assets/img/` und Video in `assets/video/` stammen von Thorsten Büscher. Vor dem Livegang klären: Einverständnis der abgebildeten
  Patient:innen/Teilnehmenden und Bildrechte (z. B. Screenshots aus Videos von PINO).
- Flyer als PDF bereitstellen (`assets/`) und Download-Link in `index.html` anpassen.

## Lokal ansehen
```
python3 -m http.server 8000
```
