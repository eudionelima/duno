/* view_source.js — T-021 carregamento do código-fonte via /source/<module>/<level> */
'use strict';

function openSourceModal(module, level) {
  const modal   = document.getElementById('source-modal');
  const codeEl  = document.getElementById('source-code');
  const metaEl  = document.getElementById('source-modal-meta');

  if (!modal || !codeEl) return;

  metaEl.textContent = module + ' / ' + level;
  codeEl.textContent = 'Carregando…';
  modal.style.display = 'flex';

  fetch('/source/' + module + '/' + level)
    .then(function(r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(function(data) {
      codeEl.textContent = data.source;
      // Prism highlight se disponível
      if (window.Prism) {
        Prism.highlightElement(codeEl);
      }
    })
    .catch(function(err) {
      codeEl.textContent = 'Erro ao carregar source: ' + err.message;
    });
}
