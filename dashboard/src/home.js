// Portada: una fila por hipótesis con lo justo para decidir cuál abrir.
// Fila = nombre y pregunta · fases · efecto · IC frente a 0 · años positivos · PnL · equity.
import { clave, loadRegistro, loadIndice, loadFicha } from './data.js';
import { computeMetrics } from './metrics.js';

const $ = id => document.getElementById(id);
const nf = d => new Intl.NumberFormat('es-ES', { minimumFractionDigits: d, maximumFractionDigits: d });
const pb = v => v * 10000;
const fdate = d => d.split('-').reverse().join('/');
const sign = v => v > 0 ? 'pos' : v < 0 ? 'neg' : '';
const sgn = v => (v > 0 ? '+' : '') + nf(2).format(v);
const STATE = { inconclusive: ['no concluyente', 'caution'], holds: ['se sostiene', 'pos'], falsified: ['falsada', 'neg'] };

document.querySelector('.dash').hidden = true;
$('home').hidden = false;
document.title = 'Hipótesis';

// Registro + experimentos del lab que aún no tienen entrada (se ven igual, con su ID como nombre).
const [registro, indice] = await Promise.all([loadRegistro(), loadIndice()]);
const known = new Set(registro.flatMap(e => [e.id, e.hipotesis]));
const extra = Object.values(Object.fromEntries(indice.filter(r => !known.has(r.hipotesis)).map(r => [r.hipotesis, r])))
  .map(r => ({ id: r.hipotesis, experimentos: { IS: r.id }, reglas: {}, estados: {}, nuevo: true }));
const entries = [...registro, ...extra];
const fichas = await Promise.all(entries.map(loadFicha));

// Entradas con la misma clave (`grupo` o `hipotesis`: varios instrumentos o variantes) se agrupan en una fila.
const groups = [];
entries.forEach((e, k) => {
  const g = clave(e) && groups.find(g => g.id === clave(e));
  if (g) g.ks.push(k); else groups.push({ id: clave(e) ?? e.id, ks: [k] });
});
$('home-sub').textContent = `${groups.length} hipótesis · ${entries.length} pruebas en IS`;

/* ---------- piezas de cada fila ---------- */
const phaseChip = (label, state) => {
  const [txt, cls] = state ? STATE[state] : ['pendiente', ''];
  return `<span class="phase ${cls}" title="${label} · ${txt}" ${state ? '' : 'data-off'}>${label}</span>`;
};

// IC 95 % en una tira: escala propia de la fila, siempre con el 0 dentro.
function ciStrip(r) {
  const [lo, hi] = r.ci95.map(pb), obs = pb(r.difference), W = 150, H = 14;
  const a = Math.min(0, lo), b = Math.max(0, hi), pad = (b - a) * .08;
  const x = v => ((v - a + pad) / (b - a + 2 * pad)) * W;
  return `<svg class="ci" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" aria-hidden="true">
    <line class="ci-axis" x1="0" x2="${W}" y1="${H / 2}" y2="${H / 2}"/>
    <line class="ci-band" x1="${x(lo)}" x2="${x(hi)}" y1="${H / 2}" y2="${H / 2}"/>
    <line class="ci-zero" x1="${x(0)}" x2="${x(0)}" y1="0" y2="${H}"/>
    <circle class="ci-obs" cx="${x(obs)}" cy="${H / 2}" r="3.5"/></svg>`;
}

// Equity en miniatura: curva + superficie de puntos, como en la ficha.
function spark(equity, id) {
  const W = 150, H = 40, v = equity.map(e => e[1]);
  const lo = Math.min(...v), hi = Math.max(...v), step = Math.max(1, Math.floor(v.length / W));
  const pts = v.filter((_, i) => i % step === 0).map((y, i, a) => [(i / (a.length - 1)) * W, H - 2 - ((y - lo) / (hi - lo || 1)) * (H - 4)]);
  const line = pts.map(p => p.map(n => n.toFixed(1)).join(',')).join(' ');
  return `<svg class="spark" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" aria-hidden="true">
    <defs><pattern id="dots${id}" width="3" height="3" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r=".6"/></pattern></defs>
    <polygon class="spark-area" fill="url(#dots${id})" points="0,${H} ${line} ${W},${H}"/>
    <polyline class="spark-line" points="${line}"/></svg>`;
}

const kpi = (l, n, d = '', cls = '') =>
  `<div class="kpi"><span class="l">${l}</span><span class="n ${cls}">${n}</span><span class="d">${d || '&nbsp;'}</span></div>`;

// Varias IC en una tira: escala común, una línea por instrumento.
function ciStack(rs) {
  const cis = rs.map(r => r.ci95.map(pb)), W = 150, H = 14, gap = H / (rs.length + 1);
  const a = Math.min(0, ...cis.map(c => c[0])), b = Math.max(0, ...cis.map(c => c[1])), pad = (b - a) * .08;
  const x = v => ((v - a + pad) / (b - a + 2 * pad)) * W;
  return `<svg class="ci" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" aria-hidden="true">
    ${rs.map((r, i) => { const y = gap * (i + 1), [lo, hi] = cis[i];
      return `<line class="ci-band thin" x1="${x(lo)}" x2="${x(hi)}" y1="${y}" y2="${y}"/><circle class="ci-obs" cx="${x(pb(r.difference))}" cy="${y}" r="1.8"/>`; }).join('')}
    <line class="ci-zero" x1="${x(0)}" x2="${x(0)}" y1="0" y2="${H}"/></svg>`;
}

// Equity de varios instrumentos, en % sobre su capital, con la misma escala.
function sparkMany(eqs, id) {
  const W = 150, H = 40, rel = eqs.map(eq => eq.map(e => e[1] / eq[0][1] - 1));
  const lo = Math.min(...rel.flat()), hi = Math.max(...rel.flat());
  return `<svg class="spark" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" aria-hidden="true">${rel.map((v, k) => {
    const step = Math.max(1, Math.floor(v.length / W));
    const pts = v.filter((_, i) => i % step === 0).map((y, i, a) => `${((i / (a.length - 1)) * W).toFixed(1)},${(H - 2 - ((y - lo) / (hi - lo || 1)) * (H - 4)).toFixed(1)}`);
    return `<polyline class="spark-line thin" style="--sc:var(--series-${k + 1})" points="${pts.join(' ')}"/>`; }).join('')}</svg>`;
}

const range = (vs, f) => { const lo = Math.min(...vs), hi = Math.max(...vs); return lo === hi ? f(lo) : `${f(lo)} … ${f(hi)}`; };

function groupRow(g, k) {
  const es = g.ks.map(i => entries[i]), Ds = g.ks.map(i => fichas[i]), rs = Ds.map(D => D.phases.IS.research);
  const ph = Ds[0].phases.IS, e = es[0], u = rs[0].unit;
  const states = [...new Set(es.map((x, i) => x.estados?.IS ?? Ds[i].phases.IS.state))];
  const state = states.length === 1 ? states[0] : 'inconclusive';
  const effects = rs.map(r => pb(r.difference)), ups = rs.map(r => Object.values(r.by_year).filter(v => v > 0).length);
  const rets = Ds.map(D => computeMetrics(D.phases.IS).pnl / D.initialEquity * 100);
  const noZero = rs.filter(r => r.ci95[0] > 0 || r.ci95[1] < 0).length;
  const label = i => es[i].etiqueta ?? Ds[i].identity.instrument, variantes = es.some(x => x.etiqueta);
  const best = label(effects.indexOf(Math.max(...effects)));
  return `<a class="row" href="#${g.id}" style="--row-state:var(--${STATE[state]?.[1] ?? 'faint'})">
    <div class="row-id">
      <h2>${e.grupo ?? `${new Set(es.map(x => x.efecto)).size === 1 ? e.efecto : g.id} · ${Ds.map((_, i) => label(i)).join(variantes ? ' · ' : ' ')}`}</h2>
      <p class="question">${rs[0].question.replace(new RegExp(`(el )?${Ds[0].identity.instrument}`), 'el índice')}</p>
      <p class="row-spec">${e.hipotesis ?? g.id} · ${Ds.length} ${variantes ? 'variantes' : 'instrumentos'} · ${Ds[0].identity.frequency} · ${fdate(ph.start)} → ${fdate(ph.end)}</p>
    </div>
    <div class="phases">${phaseChip('IS', state)}${phaseChip('OOS', null)}${phaseChip('Holdout', null)}</div>
    ${kpi(`Efecto ${e.efecto ?? ''}`, range(effects, sgn) + `<span class="u">${u}</span>`, `mayor en ${best}`)}
    <div class="kpi"><span class="l">IC 95 %</span>${ciStack(rs)}<span class="d">${noZero ? `${noZero}/${rs.length} no cruzan 0` : '<span class="warn">todos cruzan 0</span>'}</span></div>
    ${kpi('Años +', range(ups, v => v) + `<span class="u">/ ${Object.keys(rs[0].by_year).length}</span>`)}
    ${kpi('ROI', range(rets, sgn) + '<span class="u">%</span>', Ds[0].sizing ?? e.reglas['Tamaño'] ?? '')}
    ${sparkMany(Ds.map(D => D.phases.IS.equity), k)}
  </a>`;
}

/* ---------- filas ---------- */
$('rows').innerHTML = groups.map((g, gi) => {
  if (g.ks.length > 1) return groupRow(g, gi);
  const k = g.ks[0], D = fichas[k];
  const e = entries[k], ph = D.phases.IS, r = ph.research, m = computeMetrics(ph);
  const years = Object.values(r.by_year), up = years.filter(v => v > 0).length;
  const [lo, hi] = r.ci95.map(pb), crosses = lo < 0 && hi > 0;
  const state = e.estados?.IS ?? ph.state;
  return `<a class="row" href="#${e.id}" style="--row-state:var(--${STATE[state]?.[1] ?? 'faint'})">
    <div class="row-id">
      <h2>${D.name}</h2>
      <p class="question">${r.question}</p>
      <p class="row-spec">${D.identity.instrument} · ${D.identity.frequency} · ${fdate(ph.start)} → ${fdate(ph.end)}${e.nuevo ? ' · <span class="warn">sin registrar</span>' : ''}</p>
    </div>
    <div class="phases">${phaseChip('IS', state)}${phaseChip('OOS', e.experimentos.OOS && e.estados?.OOS)}${phaseChip('Holdout', null)}</div>
    ${kpi(`Efecto ${e.efecto ?? ''}`, sgn(pb(r.difference)) + `<span class="u">${r.unit}</span>`,
          `${e.efecto ?? 'ventana'} ${nf(2).format(pb(r.mean_tom))}` + (r.mean_rest == null ? '' : ` · resto ${nf(2).format(pb(r.mean_rest))}`), sign(r.difference))}
    <div class="kpi"><span class="l">IC 95 %</span>${ciStrip(r)}<span class="d">${nf(2).format(lo)} a ${nf(2).format(hi)} · ${crosses ? '<span class="warn">cruza 0</span>' : 'no cruza 0'}</span></div>
    ${kpi('Años +', `${up}<span class="u">/ ${years.length}</span>`)}
    ${kpi('ROI', sgn(m.roi * 100) + '<span class="u">%</span>', `anual ${nf(2).format(m.cagr * 100)} % · ${nf(0).format(m.pnl)} USD`, sign(m.roi))}
    ${spark(ph.equity, k)}
  </a>`;
}).join('');
