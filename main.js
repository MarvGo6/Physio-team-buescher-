(function () {
  // Header: Hintergrund beim Scrollen verstärken
  var header = document.querySelector('.site-header');
  function onScroll() { header.classList.toggle('scrolled', window.scrollY > 20); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

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

  // Sanftes Einblenden beim Scrollen
  var targets = document.querySelectorAll('.section-head, .phase, .offer, .special-card, .special-media, .tagline-card, .audience-cards li, .steps li, .referent-grid > *, .flyer-grid > *, .contact-grid > *');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('in'); io.unobserve(entry.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    targets.forEach(function (el) { el.classList.add('reveal'); io.observe(el); });
  }

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
