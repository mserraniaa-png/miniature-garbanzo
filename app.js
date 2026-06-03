document.addEventListener('DOMContentLoaded', () => {
  initSmoothScroll();
  initFadeInObserver();
  initActiveNav();
  initParallax();
  initLightbox();
  initFilters();
});

function initSmoothScroll() {
  const navLinks = document.querySelectorAll('.nav-menu a, .btn-primary');
  const header = document.querySelector('.main-header');
  if (!header) return;
  const headerHeight = header.offsetHeight;

  navLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (!href || !href.startsWith('#')) return;
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        window.scrollTo({
          top: target.offsetTop - headerHeight,
          behavior: 'smooth'
        });
      }
    });
  });
}

function initFadeInObserver() {
  const elements = document.querySelectorAll('.fade-in');
  if (!elements.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });

  elements.forEach(el => observer.observe(el));
}

function initActiveNav() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-menu a');
  if (!sections.length || !navLinks.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + id) {
            link.classList.add('active');
          }
        });
      }
    });
  }, {
    threshold: 0.3,
    rootMargin: '0px 0px -100px 0px'
  });

  sections.forEach(section => observer.observe(section));
}

function initParallax() {
  const wraps = document.querySelectorAll('.portfolio-item .image-wrap');
  if (!wraps.length) return;

  const portfolio = document.getElementById('portfolio');
  if (!portfolio) return;

  let ticking = false;

  function update() {
    const viewportCenter = window.innerHeight / 2;

    wraps.forEach(wrap => {
      const rect = wrap.getBoundingClientRect();
      const itemCenter = rect.top + rect.height / 2;
      const speed = parseFloat(wrap.dataset.speed) || 0.5;
      const offset = (itemCenter - viewportCenter) * speed * 0.06;
      wrap.style.transform = `translateY(${-offset}px)`;
    });
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(update);
      ticking = true;
    }
  }, { passive: true });
}

function initLightbox() {
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxMeta = document.getElementById('lightbox-meta');
  const lightboxTitle = document.getElementById('lightbox-title');
  const lightboxDesc = document.getElementById('lightbox-desc');
  const closeBtn = lightbox?.querySelector('.lightbox-close');
  const backdrop = lightbox?.querySelector('.lightbox-backdrop');
  const items = document.querySelectorAll('.portfolio-item');

  if (!lightbox) return;

  function open(item) {
    const img = item.querySelector('img');
    const meta = item.querySelector('.meta');
    const title = item.querySelector('h3');
    const desc = item.dataset.description || '';

    if (img) lightboxImg.src = img.src;
    if (img) lightboxImg.alt = img.alt;
    if (meta) lightboxMeta.textContent = meta.textContent;
    if (title) lightboxTitle.textContent = title.textContent;
    lightboxDesc.textContent = desc;

    document.body.style.overflow = 'hidden';
    lightbox.classList.add('active');
  }

  function close() {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
  }

  items.forEach(item => {
    item.addEventListener('click', () => open(item));
  });

  if (closeBtn) closeBtn.addEventListener('click', close);
  if (backdrop) backdrop.addEventListener('click', close);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && lightbox.classList.contains('active')) {
      close();
    }
  });
}

function initFilters() {
  const buttons = document.querySelectorAll('.portfolio-filters button');
  const items = document.querySelectorAll('.portfolio-item');
  if (!buttons.length || !items.length) return;

  const filterMap = {
    'todas': 'all',
    'editorial': 'editorial',
    'paisaje': 'paisaje',
    'retrato': 'retrato'
  };

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filterKey = btn.textContent.trim().toLowerCase();
      const filter = filterMap[filterKey] || 'all';

      items.forEach(item => {
        if (filter === 'all') {
          item.classList.remove('hidden');
        } else {
          const cat = item.dataset.category;
          if (cat === filter) {
            item.classList.remove('hidden');
          } else {
            item.classList.add('hidden');
          }
        }
      });
    });
  });
}
