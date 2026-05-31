// ─── API Health Check ─────────────────────────────────────────────
async function checkApiStatus() {
  const dot  = document.querySelector('.status-dot');
  const text = document.querySelector('.status-text');
  if (!dot || !text) return;

  try {
    // We try to hit the API docs endpoint — FastAPI always serves it
    const r = await fetch('/api-health-proxy', { signal: AbortSignal.timeout(4000) });
    if (r.ok || r.status < 500) {
      dot.classList.add('online');
      text.textContent = 'API connected';
    } else {
      throw new Error('bad status');
    }
  } catch {
    dot.classList.remove('online');
    dot.classList.add('offline');
    text.textContent = 'API offline';
  }
}

// ─── Auto-dismiss flash messages ─────────────────────────────────
function autoDismissFlash() {
  document.querySelectorAll('.flash').forEach((el, i) => {
    setTimeout(() => {
      el.style.transition = 'opacity 0.4s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 400);
    }, 5000 + i * 300);
  });
}

// ─── Animate probability bars on load ────────────────────────────
function animateProbBars() {
  document.querySelectorAll('.prob-bar-fill').forEach(bar => {
    const target = bar.style.width;
    bar.style.width = '0%';
    requestAnimationFrame(() => {
      setTimeout(() => { bar.style.width = target; }, 100);
    });
  });
}

// ─── Form validation helpers ──────────────────────────────────────
function enhanceForm() {
  const form = document.getElementById('patientForm');
  if (!form) return;

  form.addEventListener('submit', function(e) {
    const emptyRequired = [...form.querySelectorAll('[required]')]
      .filter(el => el.value === '' || el.value === null);

    if (emptyRequired.length > 0) {
      e.preventDefault();
      emptyRequired[0].focus();
      emptyRequired[0].style.borderColor = 'var(--red)';
      emptyRequired[0].style.boxShadow = '0 0 0 3px rgba(247,126,126,0.15)';
      setTimeout(() => {
        emptyRequired[0].style.borderColor = '';
        emptyRequired[0].style.boxShadow = '';
      }, 2000);

      // Show a brief notice
      const notice = document.createElement('div');
      notice.className = 'flash flash--error';
      notice.innerHTML = '<span>Please fill in all required fields.</span>';
      notice.style.marginBottom = '1rem';
      form.prepend(notice);
      setTimeout(() => notice.remove(), 3000);
    }
  });

  // Clear red border on input
  form.querySelectorAll('.input').forEach(el => {
    el.addEventListener('change', () => {
      el.style.borderColor = '';
      el.style.boxShadow = '';
    });
  });
}

// ─── Sidebar active link indicator ───────────────────────────────
function highlightNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && path === href) {
      link.classList.add('active');
    }
  });
}

// ─── Confirm delete ───────────────────────────────────────────────
document.querySelectorAll('[data-confirm]')?.forEach(btn => {
  btn.addEventListener('click', e => {
    if (!confirm(btn.dataset.confirm)) e.preventDefault();
  });
});

// ─── Init ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  checkApiStatus();
  autoDismissFlash();
  animateProbBars();
  enhanceForm();
  highlightNav();
});
