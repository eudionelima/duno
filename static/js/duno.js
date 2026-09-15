/* duno.js — T-021 JavaScript global DUNO */
'use strict';

// ESC fecha modal de source
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeSourceModal();
});

function closeSourceModal() {
  const modal = document.getElementById('source-modal');
  if (modal) modal.style.display = 'none';
}

// Flash de resultado — remove após 6s
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.alert[data-auto-dismiss]').forEach(function(el) {
    setTimeout(function() {
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '0';
      setTimeout(function() { el.remove(); }, 500);
    }, 6000);
  });
});
