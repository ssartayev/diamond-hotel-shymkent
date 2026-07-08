/* Diamond Hotel Shymkent — interactions.
   Progressive enhancement: the site is fully usable without JS. */
(() => {
  'use strict';

  const header = document.querySelector('[data-header]');
  const hasHero = document.body.classList.contains('has-hero');

  /* Header: solid after scroll (always solid on pages without hero).
     Mobile booking bar: appears after the hero CTA scrolls out of view. */
  const mobileCta = document.querySelector('[data-mobile-cta]');
  const syncHeader = () => {
    const solid = !hasHero || window.scrollY > 24;
    header.classList.toggle('is-solid', solid);
    if (mobileCta) {
      const show = !hasHero || window.scrollY > window.innerHeight * 0.55;
      mobileCta.classList.toggle('is-visible', show);
    }
  };
  syncHeader();
  window.addEventListener('scroll', syncHeader, { passive: true });

  /* Mobile menu */
  const toggle = document.querySelector('.nav-toggle');
  const menu = document.getElementById('mobile-menu');
  if (toggle && menu) {
    const setMenu = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
      document.body.classList.toggle('menu-open', open);
      if (open) {
        menu.hidden = false;
        void menu.offsetHeight; // flush styles so the fade-in transition runs
        menu.classList.add('is-open');
        header.classList.add('is-solid');
      } else {
        menu.classList.remove('is-open');
        setTimeout(() => { menu.hidden = true; syncHeader(); }, 300);
      }
    };
    toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') setMenu(false);
    });
  }

  /* Booking dialog */
  const booking = document.getElementById('booking-dialog');
  if (booking) {
    document.querySelectorAll('[data-open-booking]').forEach((btn) =>
      btn.addEventListener('click', () => booking.showModal()));
    booking.querySelector('[data-close-booking]').addEventListener('click', () => booking.close());
    booking.addEventListener('click', (e) => {
      if (e.target === booking) booking.close(); // backdrop click
    });
  }

  /* Reveal on scroll (once), with stagger inside [data-reveal-group] */
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    document.querySelectorAll('[data-reveal-group]').forEach((group) => {
      group.querySelectorAll(':scope .reveal').forEach((el, i) => {
        el.style.setProperty('--reveal-delay', `${Math.min(i * 70, 350)}ms`);
      });
    });
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('is-visible'));
  }

  /* Gallery: filters + lightbox */
  const grid = document.querySelector('[data-gallery]');
  if (grid) {
    const items = [...grid.querySelectorAll('.gallery-item')];

    document.querySelectorAll('.filter-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach((b) =>
          b.setAttribute('aria-pressed', String(b === btn)));
        const f = btn.dataset.filter;
        items.forEach((it) =>
          it.classList.toggle('is-hidden', f !== 'all' && it.dataset.cat !== f));
      });
    });

    const lightbox = document.getElementById('lightbox');
    if (lightbox) {
      const img = lightbox.querySelector('.lightbox-stage img');
      const caption = lightbox.querySelector('.lightbox-caption');
      const counter = lightbox.querySelector('.lightbox-counter');
      let current = 0;

      const visible = () => items.filter((it) => !it.classList.contains('is-hidden'));
      const show = (i) => {
        const list = visible();
        current = (i + list.length) % list.length;
        const item = list[current];
        const src = item.dataset.full || item.querySelector('img').src;
        img.src = src;
        img.alt = item.querySelector('img').alt;
        caption.textContent = item.dataset.caption || '';
        counter.textContent = `${current + 1} / ${list.length}`;
      };

      items.forEach((item) => item.addEventListener('click', () => {
        show(visible().indexOf(item));
        lightbox.showModal();
      }));
      lightbox.querySelector('[data-lb-close]').addEventListener('click', () => lightbox.close());
      lightbox.querySelector('[data-lb-prev]').addEventListener('click', () => show(current - 1));
      lightbox.querySelector('[data-lb-next]').addEventListener('click', () => show(current + 1));
      lightbox.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') show(current - 1);
        if (e.key === 'ArrowRight') show(current + 1);
      });
      lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox || e.target.classList.contains('lightbox-stage')) lightbox.close();
      });
      /* swipe */
      let x0 = null;
      lightbox.addEventListener('touchstart', (e) => { x0 = e.touches[0].clientX; }, { passive: true });
      lightbox.addEventListener('touchend', (e) => {
        if (x0 === null) return;
        const dx = e.changedTouches[0].clientX - x0;
        if (Math.abs(dx) > 48) show(current + (dx < 0 ? 1 : -1));
        x0 = null;
      }, { passive: true });
    }
  }

  /* Footer year */
  const year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();
})();
