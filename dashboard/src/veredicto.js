// Veredicto de la hipótesis: lo decide el usuario en la conversación (frase literal en conocimiento/H-NNN.md) y se copia
// al registro como `veredicto: { marca, motivo, fecha }`. Sin veredicto, no se pinta nada.
const MARCAS = { candidata: ['candidata', 'pos'], observacion: ['en observación', 'caution'], descartada: ['descartada', 'neg'], abierta: ['abierta', ''] };
const fdate = d => d.split('-').reverse().join('/');

// el de la primera entrada que lo tenga (en un grupo, el veredicto es de la hipótesis)
export const veredictoDe = entries => entries.find(e => e.veredicto)?.veredicto;

// color (token) de la marca: en la portada tiñe la línea vertical de la fila; en ficha y comparativa, la superior
export const tono = v => v ? `--${MARCAS[v.marca][1] || 'faint'}` : null;
// la línea superior sigue al veredicto si lo hay (data-verdict en <html>; ver styles.css)
export const marcarPagina = v => { if (v) document.documentElement.dataset.verdict = v.marca; };

export const chip = (v, cls = '') => v ? `<span class="verdict ${MARCAS[v.marca][1]} ${cls}">${MARCAS[v.marca][0]}</span>` : '';

export const linea = v => v ? `<p class="verdict-line">${chip(v)}<span>${fdate(v.fecha)}${v.motivo ? ` — «${v.motivo}»` : ''}</span></p>` : '';
