(function () {
  // Alte Sprungmarken der früheren Einzelseite auf die neuen Unterseiten umleiten
  var moved = { '#referent': '/referent', '#inhalte': '/inhalte', '#akademien': '/akademien' };
  if ((location.pathname === '/' || location.pathname === '/index.html') && moved[location.hash]) {
    location.replace(moved[location.hash]);
    return;
  }

  // Mobile Navigation
  var toggle = document.querySelector('.nav-toggle');
  var list = document.getElementById('nav-list');
  if (toggle && list) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      list.classList.toggle('open', !open);
    });
    list.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        toggle.setAttribute('aria-expanded', 'false');
        list.classList.remove('open');
      }
    });
  }

  // Jahr im Footer
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Video: spielt stumm, sobald es sichtbar ist (nicht bei reduzierter Bewegung)
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.ph-video').forEach(function (fig) {
    var video = fig.querySelector('video');
    var btn = fig.querySelector('.video-sound');
    if (reduce) video.setAttribute('controls', '');
    if ('IntersectionObserver' in window && !reduce) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) { var p = video.play(); if (p && p.catch) p.catch(function () {}); }
          else video.pause();
        });
      }, { threshold: 0.35 }).observe(video);
    }
    if (btn) btn.addEventListener('click', function () {
      video.muted = !video.muted;
      if (!video.muted && video.paused) video.play();
      btn.setAttribute('aria-pressed', String(!video.muted));
      btn.textContent = video.muted ? 'Ton an' : 'Ton aus';
    });
  });

  // "Kurs anfragen": Nachricht im Kontaktformular mit dem Kursnamen vorbelegen
  document.querySelectorAll('a[data-kurs]').forEach(function (a) {
    a.addEventListener('click', function () {
      var msg = document.querySelector('#contact-form textarea[name="message"]');
      if (msg && !msg.value.trim()) msg.value = 'Wir interessieren uns für den Kurs „' + a.dataset.kurs + '“.\n\nTermin, Ort und Teilnehmerzahl: ';
    });
  });

  // Kontaktformular: sendet die Anfrage direkt per E-Mail (Dienst FormSubmit).
  // Fällt der Dienst aus, öffnet sich als Ersatz das E-Mail-Programm mit vorausgefüllter Nachricht.
  var form = document.getElementById('contact-form');
  if (form) {
    var note = form.querySelector('.form-note');
    var button = form.querySelector('button[type="submit"]');
    var setNote = function (text, cls) {
      note.textContent = text;
      note.className = 'form-note' + (cls ? ' ' + cls : '');
    };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll('[required]').forEach(function (field) {
        var valid = field.type === 'checkbox' ? field.checked : field.value.trim() !== '' && field.checkValidity();
        field.classList.toggle('invalid', !valid);
        if (!valid) ok = false;
      });
      if (!ok) { setNote('Bitte füllen Sie alle Pflichtfelder (*) korrekt aus.', 'error'); return; }

      var d = new FormData(form);
      if (d.get('_honey')) return; // Spam-Schutz: unsichtbares Feld wurde ausgefüllt
      var subject = 'Kursanfrage „Sportphysiotherapie neu gedacht“' + (d.get('org') ? ' – ' + d.get('org') : '');
      var fields = {
        Name: d.get('name'),
        Einrichtung: d.get('org') || '–',
        'E-Mail': d.get('email'),
        Telefon: d.get('phone') || '–',
        'Zeitraum und Ort': d.get('when') || '–',
        Nachricht: d.get('message')
      };
      var mailtoFallback = function () {
        var body = Object.keys(fields).map(function (k) { return k + ': ' + fields[k]; }).join('\n');
        window.location.href = 'mailto:' + form.dataset.email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
        setNote('Die Anfrage konnte nicht direkt gesendet werden. Ihr E-Mail-Programm wird geöffnet – oder schreiben Sie an ' + form.dataset.email + '.', 'error');
      };

      var payload = Object.assign({ _subject: subject, _replyto: d.get('email'), _template: 'table', _captcha: 'false' }, fields);
      button.disabled = true;
      setNote('Wird gesendet …');
      fetch('https://formsubmit.co/ajax/' + encodeURIComponent(form.dataset.target || form.dataset.email), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (res) {
        return res.json().then(function (data) {
          if (!res.ok || String(data.success) !== 'true') throw new Error(data.message || 'Fehler');
        });
      }).then(function () {
        form.reset();
        setNote('Danke! Ihre Anfrage ist angekommen. Thorsten Büscher meldet sich persönlich bei Ihnen.', 'ok');
      }).catch(mailtoFallback).then(function () {
        button.disabled = false;
      });
    });
  }
})();
