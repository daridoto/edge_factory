// Entrada: sin nada en la URL, la portada; con #<hipótesis> de varios instrumentos, la comparativa;
// con #<grupo>/<subgrupo>, la comparativa de ese subgrupo (p. ej. #hora-2/nq); con #<entrada del registro>, su ficha.
import './styles.css';
import { clave, loadRegistro } from './data.js';

// Transición entre vistas: la actual se desvanece, se recarga y la nueva entra cuando ya tiene datos.
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
addEventListener('hashchange', () => {
  document.documentElement.classList.add('leaving');
  setTimeout(() => location.reload(), reduced ? 0 : 160);
});
const hash = location.hash.slice(1);
try {
  if (!hash) await import('./home.js');
  else if ((await loadRegistro()).filter(e => clave(e) === hash.split('/')[0]).length > 1) await import('./comparativa.js');
  else await import('./ficha.js');
} finally {
  document.documentElement.classList.add('ready');
}
