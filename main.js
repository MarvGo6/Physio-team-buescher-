(function () {
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

  // Kontaktformular: öffnet das E-Mail-Programm mit vorausgefüllter Anfrage
  var form = document.getElementById('contact-form');
  if (form) {
    var note = form.querySelector('.form-note');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var required = form.querySelectorAll('[required]');
      var ok = true;
      required.forEach(function (field) {
        var valid = field.type === 'checkbox' ? field.checked : field.value.trim() !== '' && field.checkValidity();
        field.classList.toggle('invalid', !valid);
        if (!valid) ok = false;
      });
      if (!ok) {
        note.textContent = 'Bitte füllen Sie alle Pflichtfelder (*) korrekt aus.';
        note.classList.add('error');
        return;
      }
      var d = new FormData(form);
      var subject = 'Kursanfrage „Sportphysiotherapie neu gedacht“' + (d.get('org') ? ' – ' + d.get('org') : '');
      var body = [
        'Name: ' + d.get('name'),
        'Einrichtung: ' + (d.get('org') || '–'),
        'E-Mail: ' + d.get('email'),
        'Telefon: ' + (d.get('phone') || '–'),
        'Wunschzeitraum / Ort: ' + (d.get('when') || '–'),
        '',
        d.get('message')
      ].join('\n');
      window.location.href = 'mailto:physioteambuescher@gmail.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      note.classList.remove('error');
      note.textContent = 'Ihr E-Mail-Programm wird geöffnet. Falls nicht, schreiben Sie bitte direkt an physioteambuescher@gmail.com.';
    });
  }
})();
