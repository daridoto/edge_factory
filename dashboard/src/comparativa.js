// Comparativa: una hipótesis probada en varios instrumentos o variantes (entradas del registro con el mismo `hipotesis`;
// cada una se nombra por su `etiqueta` o, sin ella, por su instrumento).
// Responde, de arriba abajo: ¿en qué instrumentos aparece el efecto? · ¿cómo se habría vivido operándolo?
// · ¿qué años lo sostienen en todos? · cifras por instrumento. Clic en una fila → su ficha.
import * as echarts from 'echarts';
import { clave, loadRegistro, loadFicha } from './data.js';
import { computeMetrics } from './metrics.js';
import { linea, marcarPagina, veredictoDe } from './veredicto.js';

const nf = d => new Intl.NumberFormat('es-ES', { minimumFractionDigits: d, maximumFractionDigits: d });
const pb = v => v * 10000;
const sgn = (v, d = 2) => (v > 0 ? '+' : '') + nf(d).format(v);
const fdate = d => d.split('-').reverse().join('/');
const $ = id => document.getElementById(id);
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const sign = v => v > 0 ? 'pos' : v < 0 ? 'neg' : '';
const STATE = { inconclusive: ['no concluyente', 'caution'], holds: ['se sostiene', 'pos'], falsified: ['falsada', 'neg'] };
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

document.querySelector('.dash').hidden = true;
$('cmp').hidden = false;

const [hid, subHash] = location.hash.slice(1).split('/');
const todo = (await loadRegistro()).filter(e => clave(e) === hid);
// con `subgrupo` (p. ej. HORA 2 en ES y NQ), se ve un subgrupo cada vez (máximo 4 colores) y un selector cambia de uno a otro
const subs = [...new Set(todo.map(e => e.subgrupo).filter(Boolean))];
const sub = subs.find(x => x.toLowerCase() === decodeURIComponent(subHash ?? '').toLowerCase()) ?? subs[0];
const group = sub ? todo.filter(e => e.subgrupo === sub) : todo;
const fichas = await Promise.all(group.map(loadFicha));
// Cifras de una entrada en una fase (IS, OOS o Total); null si esa entrada no la tiene.
function stats(D, key) {
  const ph = D.phases[key];
  if (!ph) return null;
  const r = ph.research, m = computeMetrics(ph), years = Object.values(r.by_year);
  return { ph, r, m, effect: pb(r.difference), ci: r.ci95.map(pb), up: years.filter(v => v > 0).length, nYears: years.length,
    worstLoyo: Math.min(...Object.values(r.leave_one_year_out).map(pb)), ret: m.pnl / D.initialEquity * 100 };
}
// una fila por instrumento o variante, de mayor a menor efecto en IS (el orden no cambia con la fase)
// color por entrada en orden del registro (sigue a la entidad, no al puesto)
const entradas = fichas.map((D, k) => {
  const e = group[k];
  return { e, D, name: e.etiqueta ?? D.identity.instrument, color: `--series-${k + 1}`, st: Object.fromEntries(['IS', 'OOS', 'Total'].map(f => [f, stats(D, f)])) };
}).sort((a, b) => b.st.IS.effect - a.st.IS.effect);
// fase que se ve: todos los bloques muestran solo las entradas que la tienen
let phase = 'IS', items = [];
const setItems = () => { items = entradas.filter(i => i.st[phase]).map(i => ({ ...i, ...i.st[phase] })); };
setItems();
const first = items[0], U = first.r.unit;

/* ---------- cabecera ---------- */
// con efectos distintos (variantes de una hipótesis), la cabecera nombra la hipótesis
const efectos = new Set(items.map(i => i.e.efecto)), efecto = efectos.size === 1 ? first.e.efecto : hid;
// `grupo` del registro (p. ej. «HORA 2 · ES»); si no, efecto e instrumentos o variantes
$('c-name').textContent = group[0].grupo ?? `${efecto} · ${items.map(i => i.name).join(' · ')}`;
document.title = group[0].grupo ? [group[0].grupo, sub].filter(Boolean).join(' · ') : `${hid} · ${efecto}`;
if (subs.length > 1) $('c-name').insertAdjacentHTML('afterend', `<nav class="chips subs" aria-label="Mercado">${subs.map(x =>
  `<a class="chip" href="#${hid}/${x.toLowerCase()}" aria-pressed="${x === sub}">${x}</a>`).join('')}</nav>`);
// pregunta y reglas: las de la primera entrada del registro (con variantes, la de la hipótesis base)
const q0 = items.find(i => i.e === group[0]);
$('c-q').insertAdjacentHTML('afterend', linea(veredictoDe(todo)));
marcarPagina(veredictoDe(todo));
$('c-q').textContent = group[0].pregunta ?? q0.r.question.replace(new RegExp(`(el )?${q0.D.identity.instrument}`), 'el índice');
// reglas: si las variantes no comparten reglas (salvo el tamaño), una línea por variante con su color
const sinTam = e => JSON.stringify(Object.entries(e.reglas).filter(([k]) => k !== 'Tamaño'));
// solo en grupos que mezclan hipótesis (sus reglas no se resumen en las de la primera); el resto, como siempre
const mixta = new Set(todo.map(e => e.hipotesis)).size > 1;
const porVariante = mixta && entradas.some(i => sinTam(i.e) !== sinTam(q0.e));
const reglas = Object.entries(q0.e.reglas).filter(([k]) => !porVariante || k === 'Tamaño');
$('c-spec').innerHTML = (porVariante ? entradas.map(i => `<div class="spec-var" data-name="${i.name}"><dt><i class="sw" style="--sc:var(${i.color})"></i>${i.name}</dt><dd>${
  Object.entries(i.e.reglas).filter(([k]) => k !== 'Tamaño').map(([k, v]) => `${k.toLowerCase()} ${v}`).join(' · ')}</dd></div>`).join('') : '') + [
  ...reglas.map(([k, v]) => k === 'Tamaño' && first.D.sizing ? [k, `${first.D.sizing} (plan: ${v})`] : [k, v]),
  ['Periodo', `<span id="c-period">${fdate(first.ph.start)} → ${fdate(first.ph.end)}</span>`],
  ['Capital', `${nf(0).format(first.D.initialEquity)} USD`],
  ['Costes', first.e.costes],
].map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`).join('');
const states = [...new Set(items.map(i => i.e.estados?.IS ?? i.ph.state))];
const state = states.length === 1 ? states[0] : 'inconclusive';
document.documentElement.dataset.state = state;
const hasPhase = f => entradas.some(i => i.st[f]);
function renderPhases() {
  const btn = (f, label) => `<button class="phase ${f === 'IS' ? STATE[state][1] : ''}" data-phase="${f}" aria-pressed="${phase === f}" ${hasPhase(f) ? '' : 'disabled'}>${label}</button>`;
  $('c-phases').innerHTML = btn('IS', `IS · ${STATE[state][0]}`) + btn('OOS', hasPhase('OOS') ? 'OOS' : 'OOS · pendiente')
    + (hasPhase('Total') ? btn('Total', 'Total') : '') + '<button class="phase" disabled>Holdout · pendiente</button>';
}
$('c-phases').addEventListener('click', e => {
  const b = e.target.closest('.phase'); if (!b || b.disabled || b.dataset.phase === phase) return;
  phase = b.dataset.phase; setItems();
  for (const n of [...off]) if (!items.some(i => i.name === n)) off.delete(n);
  render();
});
$('c-sub-ci').textContent = `${U} · ${first.r.bootstrap.replicas.toLocaleString('es-ES', { useGrouping: 'always' })} réplicas · bloques de ${first.r.bootstrap.bloque}`;
$('c-sub-eq').textContent = `% sobre ${nf(0).format(first.D.initialEquity)} USD · ${first.D.sizing ?? first.e.reglas['Tamaño'] ?? ''} por entrada`;
$('c-foot').textContent = `${hid} · ${items.map(i => i.D.exp).join(' · ')}`;

/* ---------- gráficos: base común (igual que la ficha) ---------- */
const mono = () => ({ fontFamily: 'IBM Plex Mono', fontSize: 11 });
const axisBase = () => ({ axisLine: { lineStyle: { color: css('--rule') } }, axisTick: { show: false }, axisLabel: { color: css('--muted'), ...mono() }, splitLine: { lineStyle: { color: css('--rule'), type: [1, 3] } } });
const tip = () => ({ backgroundColor: css('--surface'), borderColor: css('--rule'), textStyle: { color: css('--ink'), fontFamily: 'IBM Plex Sans', fontSize: 13 } });
// solo se anima el primer dibujo; el resaltado redibuja sin animación
let booted = false;
const anim = () => ({ animation: !reduced && !booted, animationDuration: 700 });
await document.fonts.ready;   // ECharts mide las etiquetas con la fuente ya cargada (si no, las recorta)
const cCI = echarts.init($('c-ci'), null, { renderer: 'svg' }), cEq = echarts.init($('c-eq'), null, { renderer: 'canvas' });
let hl = null;   // instrumento resaltado (hover en tabla o gráficos)
const off = new Set();   // instrumentos ocultos en la equity (filtro)

/* ---------- efecto e IC 95 %: todos en la misma escala, siempre con el 0 ---------- */
function renderCI() {
  const names = items.map(i => i.name).reverse();   // el eje de categorías va de abajo arriba
  const lo = Math.min(0, ...items.map(i => i.ci[0])), hi = Math.max(0, ...items.map(i => i.ci[1])), pad = (hi - lo) * .06;
  const dim = i => hl && hl !== i.name;
  cCI.setOption({
    ...anim(),
    grid: { left: 8, right: 12, top: 8, bottom: 22, containLabel: true },
    tooltip: { ...tip(), trigger: 'item', formatter: p => { const i = items.find(x => x.name === p.data.name);
      return `<b>${i.name}</b> ${sgn(i.effect)} ${i.r.unit}<br>${i.r.statistic}<br>IC ${nf(2).format(i.ci[0])} a ${nf(2).format(i.ci[1])} · ${i.up}/${i.nYears} años +`; } },
    xAxis: { type: 'value', min: Math.floor(lo - pad), max: Math.ceil(hi + pad), ...axisBase() },
    yAxis: { type: 'category', data: names, ...axisBase(), axisLine: { show: false }, splitLine: { show: false },
      axisLabel: { ...axisBase().axisLabel, color: css('--ink') } },
    series: [
      ...items.map(i => ({ id: 'ci' + i.name, type: 'line', silent: true, symbol: 'none', data: [[i.ci[0], i.name], [i.ci[1], i.name]],
        lineStyle: { color: css('--caution'), width: 6, cap: 'round', opacity: dim(i) ? .15 : .6 } })),
      { id: 'obs', type: 'scatter', symbolSize: 10, data: items.map(i => ({ name: i.name, value: [i.effect, i.name],
          itemStyle: { color: css('--ink'), borderColor: css('--ground'), borderWidth: 2, opacity: dim(i) ? .3 : 1 } })),
        markLine: { silent: true, symbol: 'none', label: { formatter: '0', color: css('--muted'), ...mono() },
          data: [{ xAxis: 0, lineStyle: { color: css('--ink'), width: 1.2, type: 'solid' } }] } },
    ],
  }, { notMerge: true });
}

/* ---------- equity: % sobre el capital inicial, todas superpuestas ---------- */
function renderEq() {
  cEq.setOption({
    ...anim(),
    // a la derecha cabe la etiqueta más larga al final de cada curva
    grid: { left: 44, right: 16 + 7 * Math.max(...items.map(i => i.name.length)), top: 8, bottom: 22 },
    tooltip: { ...tip(), trigger: 'axis', axisPointer: { lineStyle: { color: css('--faint'), type: [1, 3] } },
      // en eje temporal axisValue es un número: la fecha se toma del dato ('AAAA-MM-DD')
      formatter: ps => `${fdate(ps[0].data[0])}<br>` + [...ps].sort((a, b) => b.value[1] - a.value[1])
        .map(p => `${p.marker}${p.seriesName} <span class="mono">${sgn(p.value[1])} %</span>`).join('<br>') },
    xAxis: { type: 'time', ...axisBase(), splitLine: { show: false }, axisLabel: { ...axisBase().axisLabel, formatter: '{yyyy}' } },
    yAxis: { type: 'value', ...axisBase(), axisLabel: { ...axisBase().axisLabel, formatter: v => v + ' %' } },
    // el filtro usa la selección nativa (leyenda oculta): ECharts quita la serie y reajusta el eje
    legend: { show: false, data: items.map(i => i.name), selected: Object.fromEntries(items.map(i => [i.name, !off.has(i.name)])) },
    series: items.map((i, k) => {
      const h = off.has(hl) ? null : hl, on = !h || h === i.name;
      return { id: 'eq' + i.name, name: i.name, type: 'line', showSymbol: false, sampling: 'lttb', z: on ? 3 : 2,
        data: i.ph.equity.map(([d, eq]) => [d, +((eq / i.D.initialEquity - 1) * 100).toFixed(3)]),
        lineStyle: { color: css(i.color), width: h === i.name ? 2.6 : 1.6, opacity: on ? 1 : .12 },
        endLabel: { show: true, formatter: '{a}', color: on ? css('--ink') : css('--faint'), ...mono() },
        markLine: i === items.find(x => !off.has(x.name)) ? { silent: true, symbol: 'none', label: { show: false }, data: [{ yAxis: 0, lineStyle: { color: css('--rule'), type: 'solid' } }] } : undefined };
    }),
  }, { notMerge: true });
}

/* ---------- por año: efecto dentro del año; color por signo, intensidad por magnitud ---------- */
function renderYears() {
  // años de todas las entradas; un año sin dato en una entrada (p. ej. sin noches con VIX > 20) queda vacío
  const years = [...new Set(items.flatMap(i => Object.keys(i.r.by_year)))].sort();
  const vals = items.map(i => years.map(y => y in i.r.by_year ? pb(i.r.by_year[y]) : null));
  const max = Math.max(...vals.flat().filter(v => v != null).map(Math.abs));
  const yl = y => (y === years[0] ? `'${y.slice(2)}*` : `'${y.slice(2)}`);
  const cell = (v, name) => v == null ? `<span class="yc" data-name="${name}" title="sin dato">—</span>` : `<span class="yc" data-name="${name}" style="--c:var(--${v > 0 ? 'pos' : 'neg'});--a:${Math.round(12 + 70 * Math.abs(v) / max)}%" title="${nf(2).format(v)} ${U}">${sgn(v, 1)}</span>`;
  const all = years.map((_, j) => { const col = vals.map(r => r[j]);
    return col.some(v => v == null) ? '<span class="ya">·</span>' : col.every(v => v > 0) ? '<span class="ya pos" title="positivo en todos">▲</span>'
      : col.every(v => v < 0) ? '<span class="ya neg" title="negativo en todos">▼</span>' : '<span class="ya">·</span>'; });
  $('c-years').style.setProperty('--ny', years.length);
  $('c-years').innerHTML = `<span></span>${years.map(y => `<span class="yh">${yl(y)}</span>`).join('')}`
    + items.map((i, k) => `<span class="yn" data-name="${i.name}"><i class="sw" style="--sc:var(${i.color})"></i>${i.name}</span>${vals[k].map(v => cell(v, i.name)).join('')}`).join('')
    + `<span class="yn yt">todos</span>${all.join('')}`;
  const start = items.map(i => i.ph.start).sort()[0], end = items.map(i => i.ph.end).sort().at(-1);
  const sin = entradas.filter(i => !i.st[phase]).map(i => i.name);
  $('c-years-sub').textContent = `${U} · * ${years[0]} desde ${fdate(start).slice(3)}` + (sin.length ? ` · sin ${phase}: ${sin.join(', ')}` : '');
  $('c-period').textContent = `${fdate(start)} → ${fdate(end)}`;
}

/* ---------- tabla por instrumento ---------- */
function renderTable() {
  const th = ['', `Efecto ${efecto}`, 'IC 95 %', 'Años +', 'ROI', 'ROI anual', 'Max DD', 'Sharpe', 'Win rate', 'Peor sin 1 año'];
  const td = i => [
    `<i class="sw" style="--sc:var(${i.color})"></i><b>${i.name}</b>`,
    `<span class="${sign(i.effect)}">${sgn(i.effect)}</span>`,
    `${nf(2).format(i.ci[0])} a ${nf(2).format(i.ci[1])}${i.ci[0] < 0 && i.ci[1] > 0 ? ' <span class="warn">cruza 0</span>' : ''}`,
    `${i.up}/${i.nYears}`,
    `<span class="${sign(i.ret)}">${sgn(i.ret)} %</span>`,
    `<span class="${sign(i.m.cagr)}">${sgn(i.m.cagr * 100)} %</span>`,
    `${nf(2).format(-i.m.maxDD * 100)} %`,
    nf(2).format(i.m.sharpe),
    `${nf(0).format(i.m.winRate * 100)} %`,
    `<span class="${sign(i.worstLoyo)}">${sgn(i.worstLoyo)}</span>`,
  ];
  $('c-table').innerHTML = `<div class="tr th">${th.map(h => `<span>${h}</span>`).join('')}</div>`
    + items.map(i => `<a class="tr" href="#${i.e.id}" data-name="${i.name}">${td(i).map(c => `<span>${c}</span>`).join('')}${detalle(i)}</a>`).join('');
}

// línea de detalle bajo la fila: lo que el lab trae de la evidencia (operaciones, mediana, largos/cortos, predicción,
// sesiones descartadas por el filtro) y el peso de los costes. Solo en grupos que mezclan hipótesis y en pruebas
// largo/corto por señal (con largos y cortos).
function detalle(i) {
  const r = i.r, d = r.detail ?? {}, n = v => v.toLocaleString('es-ES', { useGrouping: 'always' });
  const bruto = i.ph.trades.reduce((a, t) => a + t.net + t.cost, 0) / i.D.initialEquity * 100;
  const coste = i.ph.trades.reduce((a, t) => a + t.cost, 0) / i.D.initialEquity * 100;
  const partes = [
    `${n(r.n_tom)} ops`,
    d.median != null && `mediana ${sgn(d.median)}`,
    d.longs?.[0] != null && `largos ${sgn(d.longs[1])} (${n(d.longs[0])})`,
    d.shorts?.[0] != null && `cortos ${sgn(d.shorts[1])} (${n(d.shorts[0])})`,
    d.hit != null && `acierto ${nf(1).format(d.hit)} %`,
    d.beta != null && `β×100 ${nf(2).format(d.beta)} (t ${nf(2).format(d.tBeta)})`,
    d.r2os != null && `R²<sub>OS</sub> ${sgn(d.r2os)} %`,
    d.beta2 != null && `interacción β2 ${sgn(d.beta2)} (t ${nf(2).format(d.tBeta2)})` + (d.r2osInt != null ? ` · R²<sub>OS</sub> ${sgn(d.r2osInt)} %` : ''),
    r.n_rest ? `descartadas ${sgn(pb(r.mean_rest))} (${n(r.n_rest)})` : null,
    `ROI bruto ${sgn(bruto)} % · costes −${nf(2).format(coste)} %`,
  ].filter(Boolean);
  const txt = partes.join(' · ');
  return mixta && d.longs?.[0] != null ? `<span class="det" title="${txt.replace(/<\/?sub>/g, '')}">${txt}</span>` : '';
}

/* ---------- filtro de la equity: un botón por instrumento, con su color ---------- */
function renderFilter() {
  $('c-filter').innerHTML = items.map(i => `<button class="chip" data-name="${i.name}" aria-pressed="${!off.has(i.name)}"
    title="${off.has(i.name) ? 'Mostrar' : 'Ocultar'} ${i.name} en la equity"><i class="sw" style="--sc:var(${i.color})"></i>${i.name}</button>`).join('');
}
$('c-filter').addEventListener('click', e => {
  const b = e.target.closest('.chip'); if (!b) return;
  const n = b.dataset.name;
  if (off.has(n)) off.delete(n);
  else if (off.size < items.length - 1) off.add(n);   // siempre queda al menos una
  renderFilter(); renderEq();
});

/* ---------- resaltado cruzado: tabla, años, filtro y gráficos ---------- */
function highlight(name) {
  if (name === hl) return; hl = name;
  document.querySelectorAll('#cmp [data-name]').forEach(el => el.classList.toggle('dim', !!hl && el.dataset.name !== hl));
  renderCI(); renderEq();
}
for (const id of ['c-table', 'c-years', 'c-filter']) {
  $(id).addEventListener('mouseover', e => highlight(e.target.closest('[data-name]')?.dataset.name ?? null));
  $(id).addEventListener('mouseleave', () => highlight(null));
}
cEq.on('mouseover', p => highlight(p.seriesName)); cEq.on('mouseout', () => highlight(null));
cCI.on('mouseover', p => highlight(p.data?.name ?? null)); cCI.on('mouseout', () => highlight(null));

/* ---------- arranque + tema ---------- */
const render = () => { renderPhases(); renderCI(); renderEq(); renderYears(); renderTable(); renderFilter(); };
render();
booted = true;
new ResizeObserver(() => { cCI.resize(); cEq.resize(); }).observe($('cmp'));
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', render);
new MutationObserver(render).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
if (document.fonts && document.fonts.ready) document.fonts.ready.then(render);
