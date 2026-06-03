/**
 * LearnHub — main.js
 * Lightweight progressive enhancements.
 * No build step required — plain ES2020 with Bootstrap 5 already on page.
 */

/* ── Auto-dismiss flash alerts after 5 s ────────────────────── */
(function () {
  const alerts = document.querySelectorAll('.alert.alert-dismissible');
  alerts.forEach((el) => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      bsAlert.close();
    }, 5000);
  });
})();

/* ── Confirm dialogs on data-confirm elements ───────────────── */
document.addEventListener('click', (e) => {
  const btn = e.target.closest('[data-confirm]');
  if (!btn) return;
  const message = btn.dataset.confirm || 'Are you sure?';
  if (!window.confirm(message)) {
    e.preventDefault();
    e.stopPropagation();
  }
});

/* ── File input: show selected filename ─────────────────────── */
document.querySelectorAll('input[type="file"]').forEach((input) => {
  input.addEventListener('change', () => {
    const label = input.closest('.mb-3')?.querySelector('.form-text');
    if (!label || !input.files.length) return;
    const name = input.files[0].name;
    const sizeMB = (input.files[0].size / 1_048_576).toFixed(2);
    label.textContent = `Selected: ${name} (${sizeMB} MB)`;
  });
});

/* ── Sticky navbar shadow on scroll ─────────────────────────── */
(function () {
  const nav = document.querySelector('.navbar');
  if (!nav) return;
  const onScroll = () => {
    nav.classList.toggle('shadow', window.scrollY > 8);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

/* ── Character counter for textareas with maxlength ─────────── */
document.querySelectorAll('textarea[maxlength]').forEach((ta) => {
  const max = parseInt(ta.getAttribute('maxlength'), 10);
  const counter = document.createElement('div');
  counter.className = 'form-text text-end';
  counter.textContent = `0 / ${max}`;
  ta.parentNode.insertBefore(counter, ta.nextSibling);
  ta.addEventListener('input', () => {
    const len = ta.value.length;
    counter.textContent = `${len} / ${max}`;
    counter.classList.toggle('text-danger', len >= max);
  });
});
