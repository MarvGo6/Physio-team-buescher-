# Sportphysiotherapie neu gedacht – Homepage

Landingpage zum 2-Tages-Kurs „Sportphysiotherapie neu gedacht – Von der Verletzung zur Performance“
von Thorsten Büscher, ausgerichtet auf Fortbildungsschulen und Akademien.

- Reines HTML/CSS/JS, kein Build-Schritt – direkt auf Vercel (oder jedem Static Host) deploybar.
- Schriften lokal eingebunden (`assets/fonts`: Archivo variabel, Permanent Marker), keine Google-Verbindung, keine Cookies.
- Kontaktformular öffnet das E-Mail-Programm (mailto) mit vorausgefüllter Anfrage.

## Offene Punkte vor dem Livegang
- Rezensionen: Abschnitt „Stimmen“ in `index.html` enthält Platzhalter. Nur echte, freigegebene Rückmeldungen eintragen
  (Anleitung im HTML-Kommentar dort).
- Impressum/Datenschutz: ladungsfähige Anschrift ergänzen (`impressum.html`, `datenschutz.html`).
- Bilder stammen aus dem Flyer (geringe Auflösung) – hochauflösende Originalfotos in `assets/img/` ersetzen
  (`hero-taping.jpg`, `referent.jpg`, `agility.jpg`, `shoulder-tape.jpg`, `football.jpg`, `boxjump.jpg`).
- Flyer als PDF bereitstellen (`assets/`) und Download-Link in `index.html` anpassen.

## Lokal ansehen
```
python3 -m http.server 8000
```
