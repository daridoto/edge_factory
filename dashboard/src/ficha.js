import * as echarts from 'echarts';
import { loadRegistro, loadFicha } from './data.js';
import { computeMetrics } from './metrics.js';

// La hipótesis se elige por la URL (#H-001); sin nada, la primera del registro.
const registro = await loadRegistro();
const entry = registro.find(h => h.id === location.hash.slice(1)) ?? registro[0];
const D = await loadFicha(entry);
const P = D.phases;
const U = P.IS.research.unit;   // unidad del estadístico, tal como la da el lab
for (const ph of Object.values(P)) ph.m = computeMetrics(ph);

/* estado de la vista */
let view = 'IS', oosOpen = false;
const hasOOS = () => 'OOS' in P;
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const DUR = reduced ? 0 : 700;

/* formato */
const nf = d => new Intl.NumberFormat('es-ES', { minimumFractionDigits: d, maximumFractionDigits: d });
const pb = v => v * 10000, fpb = (v, d = 2) => nf(d).format(pb(v));
const fdate = d => d.split('-').reverse().join('/');
const $ = id => document.getElementById(id);
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const unit = u => `<span class="u">${u}</span>`;
const sign = v => v > 0 ? 'pos' : v < 0 ? 'neg' : '';
const STATE = { inconclusive: ['no concluyente', 'caution'], holds: ['se sostiene', 'pos'], falsified: ['falsada', 'neg'] };

/* ---------- cabecera ---------- */
$('h-name').textContent = D.name;
$('h-q').textContent = P.IS.research.question;
document.title = D.name;
const B = P.IS.research.bootstrap;
$('sub-boot').textContent = `${B.replicas.toLocaleString('es-ES', { useGrouping: 'always' })} réplicas · bloques de ${B.bloque} · ${U}`;
$('sub-eq').textContent = `USD · ${entry.reglas['Tamaño'] ?? ''} por entrada`;
// si la hipótesis se probó en varios instrumentos, «volver» lleva a su comparativa
if (registro.filter(e => entry.hipotesis && e.hipotesis === entry.hipotesis).length > 1)
  Object.assign(document.querySelector('.dash .back'), { href: `#${entry.hipotesis}`, textContent: `← ${entry.hipotesis} · todos` });
$('foot').textContent = `${D.id} · ${D.exp} · ${fdate(D.frozen)}`;

function renderPhases() {
  const btn = (key, label, { cls = '', disabled = false } = {}) =>
    `<button class="phase ${cls}" data-phase="${key}" aria-pressed="${view === key}" ${disabled ? 'disabled' : ''}>${label}</button>`;
  const st = key => STATE[P[key].state];
  $('phases').innerHTML = [
    btn('IS', `IS · ${st('IS')[0]}`, { cls: st('IS')[1] }),
    oosOpen ? btn('OOS', `OOS · ${st('OOS')[0]}`, { cls: st('OOS')[1] }) : btn('OOS', 'OOS · pendiente', { disabled: !hasOOS() }),
    oosOpen ? btn('Total', 'Total') : '',
    btn('Holdout', 'Holdout · pendiente', { disabled: true }),
  ].join('');
}
$('phases').addEventListener('click', e => {
  const b = e.target.closest('.phase'); if (!b || b.disabled) return;
  if (b.dataset.phase === 'OOS') oosOpen = true;
  setView(b.dataset.phase);
});

function renderSpec() {
  const ph = P[view];
  $('spec').innerHTML = [
    ...Object.entries(entry.reglas),
    ['Activo', `${D.identity.instrument} · ${D.identity.frequency}`],
    ['Periodo', `${fdate(ph.start)} → ${fdate(ph.end)}`],
    ['Capital', `${nf(0).format(D.initialEquity)} USD`],
    ['Costes', entry.costes],
  ].map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`).join('');
}

/* ---------- bootstrap: réplicas por fase (ilustrativas, reproducibles con la semilla) ---------- */
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const BOOT_N = 5000;
Object.values(P).forEach((ph, k) => {
  const [lo, hi] = ph.research.ci95.map(pb), r = rng(D.repro.seed + k), mid = (lo + hi) / 2, sd = (hi - lo) / 3.92;
  ph.boot = Array.from({ length: BOOT_N }, () => mid + sd * Math.sqrt(-2 * Math.log(1 - r())) * Math.cos(2 * Math.PI * r()));
  ph.bootNeg = ph.boot.filter(v => v < 0).length / BOOT_N;
});
// mismas cajas para todas las fases: así el histograma se transforma en vez de redibujarse
// ancho de caja según el rango (≤ 40 cajas), siempre con el 0 dentro: es la referencia de lectura
const allBoot = Object.values(P).flatMap(ph => ph.boot);
const bLo = Math.min(0, ...allBoot), bHi = Math.max(0, ...allBoot);
const BIN = [0.05, 0.1, 0.2, 0.25, 0.5, 1, 2, 5, 10].find(s => (bHi - bLo) / s <= 40) ?? 20;
const binLo = Math.floor(bLo / BIN) * BIN, nBins = Math.ceil((bHi - binLo) / BIN);
const binX = i => +(binLo + i * BIN).toFixed(4);
const fx = v => new Intl.NumberFormat('es-ES', { maximumFractionDigits: 2 }).format(v);
const binsOf = ph => { const n = Array(nBins).fill(0); ph.boot.forEach(v => n[Math.min(Math.floor((v - binLo) / BIN), nBins - 1)]++); return n; };

/* ---------- KPIs con cifras animadas ---------- */
const KPIS = {
  'kpi-ev': [
    { l: `Efecto ${entry.efecto}`, v: ph => [pb(ph.research.difference)], f: ([v]) => (v >= 0 ? '+' : '') + nf(2).format(v) + unit(U),
      d: ph => `${entry.efecto} ${fpb(ph.research.mean_tom)} · resto ${fpb(ph.research.mean_rest)}`, cls: ph => sign(ph.research.difference), t: P.IS.research.statistic },
    { l: 'IC 95 %', v: ph => ph.research.ci95.map(pb), f: ([a, b]) => `(${a.toFixed(2)}, ${b.toFixed(2)})`,
      d: ph => ph.research.ci95[0] < 0 && ph.research.ci95[1] > 0 ? '<span class="warn">cruza 0</span>' : 'no cruza 0', t: 'Tramo central del 95 % de las réplicas' },
    { l: 'Réplicas < 0', v: ph => [ph.bootNeg * 100], f: ([v]) => nf(0).format(v) + unit('%'), d: () => 'por debajo de 0', t: 'Porcentaje de réplicas con el estadístico negativo' },
  ],
  'kpi-res': [
    { l: 'PnL neto', v: ph => [ph.m.pnl], f: ([v]) => nf(2).format(v) + unit('USD'), d: ph => 'costes 2×: ' + nf(2).format(ph.m.pnlCosts2x), cls: ph => sign(ph.m.pnl), t: 'Equity final − inicial, neto de costes' },
    { l: 'Operaciones', v: ph => [ph.m.trades], f: ([v]) => nf(0).format(v), d: ph => 'exposición ' + nf(0).format(ph.m.exposure * 100) + ' %', t: 'Número de operaciones cerradas' },
    { l: 'Win rate', v: ph => [ph.m.winRate * 100], f: ([v]) => nf(0).format(v) + ' %', d: ph => 'payoff ' + nf(2).format(ph.m.payoff), t: 'Operaciones con PnL neto > 0 / todas' },
    { l: 'Profit factor', v: ph => [ph.m.profitFactor], f: ([v]) => nf(2).format(v), d: () => '', t: 'Ganancias netas / pérdidas netas' },
    { l: 'Sharpe', v: ph => [ph.m.sharpe], f: ([v]) => nf(2).format(v), d: ph => 'Sortino ' + nf(2).format(ph.m.sortino), t: `Anualizado, ${P.IS.periodsPerYear ?? 252} sesiones, rf = 0` },
    { l: 'Max DD', v: ph => [ph.m.maxDD * 100], f: ([v]) => nf(2).format(v) + ' %', d: ph => ph.m.openDDAge ? 'abierto ' + ph.m.openDDAge + ' ses.' : 'cerrado', t: 'Máxima caída desde un máximo de equity' },
  ],
};
for (const [id, defs] of Object.entries(KPIS))
  $(id).innerHTML = defs.map(k => `<div class="kpi" title="${k.t}"><span class="l">${k.l}</span><span class="n"></span><span class="d"></span></div>`).join('');

function updateKPIs() {
  const ph = P[view];
  for (const [id, defs] of Object.entries(KPIS)) {
    [...$(id).children].forEach((el, i) => {
      const k = defs[i], n = el.querySelector('.n'), to = k.v(ph), from = n._v || to, t0 = performance.now();
      n.className = 'n ' + (k.cls ? k.cls(ph) : '');
      el.querySelector('.d').innerHTML = k.d(ph) || '&nbsp;';
      n._v = to;
      const step = now => {
        const p = DUR ? Math.min((now - t0) / DUR, 1) : 1, e = 1 - (1 - p) ** 3;
        n.innerHTML = k.f(to.map((v, j) => from[j] + (v - from[j]) * e));
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    });
  }
}

/* ---------- gráficos: base común ---------- */
const charts = [];
const mk = (id, renderer = 'svg') => { const c = echarts.init($(id), null, { renderer }); charts.push(c); return c; };
const mono = () => ({ fontFamily: 'IBM Plex Mono', fontSize: 11 });
const axisBase = () => ({ axisLine: { lineStyle: { color: css('--rule') } }, axisTick: { show: false }, axisLabel: { color: css('--muted'), ...mono() }, splitLine: { lineStyle: { color: css('--rule'), type: [1, 3] } } });
// Barra de puntos: cada fila es un trío de puntos que se repite a lo alto de la barra.
const DOTS = 'path://M0,1a1,1 0 1,0 2,0a1,1 0 1,0 -2,0M3,1a1,1 0 1,0 2,0a1,1 0 1,0 -2,0M6,1a1,1 0 1,0 2,0a1,1 0 1,0 -2,0';
const dotBar = { type: 'pictorialBar', symbol: DOTS, symbolSize: ['70%', 2.4], symbolRepeat: true, symbolMargin: 1.2, symbolClip: true };
const tip = () => ({ backgroundColor: css('--surface'), borderColor: css('--rule'), textStyle: { color: css('--ink'), fontFamily: 'IBM Plex Sans', fontSize: 13 } });
const anim = { animation: !reduced, animationDuration: DUR, animationDurationUpdate: DUR, animationEasingUpdate: 'cubicOut' };

// la equity usa canvas: dibuja miles de puntos
const cEq = mk('ch-eq', 'canvas'), cBoot = mk('ch-boot'), cYear = mk('ch-year');

/* ---------- equity y drawdown ---------- */
// Nube de puntos (estética depth map): cada día se rellena con puntos entre la curva y la base.
// Más densos y brillantes junto a la curva ("cerca"), más escasos y tenues al alejarse ("lejos").
const DEPTH = [ // tramos de profundidad: [desde, hasta, opacidad, tamaño]
  [0, .08, .6, 1.3], [.08, .25, .34, 1.2], [.25, .5, .19, 1.1], [.5, 1, .09, 1],
];
function cloudOf(top, base, perUnit, seed) {
  const r = rng(seed), layers = DEPTH.map(() => []);
  top.forEach((t, i) => {
    const h = t - base, n = Math.round(Math.abs(h) * perUnit);
    for (let k = 0; k < n; k++) {
      const d = r() ** 2.2;                         // sesgo: la mayoría cerca de la curva
      layers[DEPTH.findIndex(([a, b]) => d >= a && d < b)].push([i, t - d * h]);
    }
  });
  return layers;
}
const cloudSeries = (id, layers, color, xi) => layers.map((pts, li) => ({
  id: `${id}${li}`, type: 'scatter', data: pts, xAxisIndex: xi, yAxisIndex: xi, large: true, silent: true, tooltip: { show: false },
  symbolSize: DEPTH[li][3], itemStyle: { color, opacity: DEPTH[li][2] },
}));

// Fases: caídas relevantes (rojo) y tramos de crecimiento entre ellas (verde).
// Solo cuentan las caídas de al menos DD_MIN × drawdown máximo; las demás son ruido.
const DD_MIN = 0.2;
function ddPhases(dd, dates) {
  const maxDD = Math.min(...dd), drops = []; let cur = null;
  dd.forEach((v, i) => {
    if (v < 0) { if (!cur) cur = { start: Math.max(i - 1, 0), min: 0 }; cur.min = Math.min(cur.min, v); }
    else if (cur) { cur.end = i; drops.push(cur); cur = null; }
  });
  if (cur) { cur.end = dd.length - 1; drops.push(cur); }
  const big = drops.filter(d => d.min <= maxDD * DD_MIN), rises = []; let from = 0;
  big.forEach(d => { if (d.start > from) rises.push({ start: from, end: d.start }); from = d.end; });
  if (from < dates.length - 1) rises.push({ start: from, end: dates.length - 1 });
  const band = (r, color) => [{ xAxis: dates[r.start], itemStyle: { color, opacity: .08 } }, { xAxis: dates[r.end] }];
  return [...big.map(r => band(r, css('--neg'))), ...rises.map(r => band(r, css('--pos')))];
}

// qué se dibuja en cada vista: IS solo; OOS y Total, la serie completa
const shownPhase = () => view === 'IS' ? P.IS : P.Total;
let dates = [], drawId = 0, lastSpan = null;
const DRAW_MS = reduced ? 0 : 800;

function renderEq() {
  const ph = shownPhase(), oosAt = P.IS.equity.length, n = ph.equity.length;
  dates = ph.equity.map(e => e[0]);
  const eqv = ph.equity.map(e => e[1]);
  let peak = -Infinity;
  const dd = eqv.map(v => { peak = Math.max(peak, v); return +((v / peak - 1) * 100).toFixed(4); });
  const lo = Math.min(...eqv), hi = Math.max(...eqv), pad = (hi - lo) * .06;
  const eqLo = Math.floor(lo - pad), eqHi = Math.ceil(hi + pad);
  const yearStart = new Set(dates.map((d, i) => i > 0 && d.slice(0, 4) !== dates[i - 1].slice(0, 4) ? i : -1).filter(i => i >= 0));
  const eqCloud = cloudOf(eqv, eqLo, 8 / (eqHi - eqLo), 11);
  const ddCloud = cloudOf(dd, 0, 5 / Math.abs(Math.min(...dd) || 1), 12);
  const split = view !== 'IS';

  // Opción del gráfico mostrando solo hasta el índice `upto` (el resto aún "sin dibujar").
  const frame = upto => {
    const cut = arr => arr.slice(0, upto + 1);
    const cutCloud = layers => layers.map(l => l.filter(p => p[0] <= upto));
    const done = upto >= n - 1, axisDates = dates.slice(0, upto + 1);
    const bands = ddPhases(cut(dd), axisDates);
    const veil = view === 'OOS' && done ? [[{ xAxis: dates[0] }, { xAxis: dates[oosAt - 1] }]] : [];
    const oosLine = split && upto >= oosAt ? [{ xAxis: dates[oosAt], label: { formatter: 'OOS', position: 'insideEndTop', color: css('--muted'), ...mono() } }] : [];
    return {
      animation: false,
      tooltip: { ...tip(), trigger: 'axis', axisPointer: { type: 'line', lineStyle: { color: css('--faint') } } },
      axisPointer: { link: [{ xAxisIndex: 'all' }] },
      grid: [{ left: 52, right: 4, top: 8, height: '68%' }, { left: 52, right: 4, top: '72%', bottom: 24 }],
      dataZoom: [{ type: 'inside', xAxisIndex: [0, 1] }],
      xAxis: [
        { type: 'category', data: axisDates, gridIndex: 0, ...axisBase(), axisLabel: { show: false }, boundaryGap: false },
        { type: 'category', data: axisDates, gridIndex: 1, ...axisBase(), boundaryGap: false,
          axisTick: { show: true, interval: i => yearStart.has(i), lineStyle: { color: css('--rule') } },
          axisLabel: { ...axisBase().axisLabel, interval: i => yearStart.has(i), formatter: v => v.slice(0, 4) } }],
      yAxis: [
        { type: 'value', gridIndex: 0, min: eqLo, max: eqHi, ...axisBase(), axisLabel: { ...axisBase().axisLabel, formatter: v => nf(0).format(v) } },
        { type: 'value', gridIndex: 1, max: 0, splitNumber: 2, ...axisBase(), axisLabel: { ...axisBase().axisLabel, formatter: v => nf(2).format(v) + '%' } }],
      series: [
        { id: 'hl0', type: 'line', data: [], xAxisIndex: 0, yAxisIndex: 0, silent: true },
        { id: 'hl1', type: 'line', data: [], xAxisIndex: 1, yAxisIndex: 1, silent: true },
        ...cloudSeries('ec', cutCloud(eqCloud), css('--ink'), 0),
        ...cloudSeries('dc', cutCloud(ddCloud), css('--neg'), 1),
        { id: 'eq', name: 'Equity', type: 'line', data: cut(eqv), showSymbol: false, connectNulls: false, lineStyle: { color: css('--ink'), width: 1.6 },
          xAxisIndex: 0, yAxisIndex: 0, markArea: { silent: true, data: bands },
          markLine: { silent: true, symbol: 'none', lineStyle: { color: css('--muted'), type: 'dashed', width: 1 }, data: oosLine },
          tooltip: { valueFormatter: v => v == null ? '—' : nf(2).format(v) + ' USD' } },
        { id: 'dd', name: 'Drawdown', type: 'line', data: cut(dd), showSymbol: false, lineStyle: { color: css('--neg'), width: 1.3 },
          xAxisIndex: 1, yAxisIndex: 1, markArea: { silent: true, data: bands },
          markLine: { silent: true, symbol: 'none', lineStyle: { color: css('--muted'), type: 'dashed', width: 1 }, label: { show: false }, data: oosLine },
          tooltip: { valueFormatter: v => v == null ? '—' : nf(3).format(v) + ' %' } },
        { id: 'veil0', type: 'line', data: [], xAxisIndex: 0, yAxisIndex: 0, silent: true, z: 10, markArea: { silent: true, itemStyle: { color: css('--ground'), opacity: .6 }, data: veil } },
        { id: 'veil1', type: 'line', data: [], xAxisIndex: 1, yAxisIndex: 1, silent: true, z: 10, markArea: { silent: true, itemStyle: { color: css('--ground'), opacity: .6 }, data: veil } },
      ],
    };
  };

  // Si el eje se amplía (IS → OOS/Total), el tramo nuevo se traza de izquierda a derecha.
  const id = ++drawId, grows = lastSpan === 'IS' && split && DRAW_MS > 0;
  lastSpan = split ? 'full' : 'IS';
  if (!grows) { cEq.setOption(frame(n - 1), { replaceMerge: ['series'] }); return; }
  const t0 = performance.now();
  const step = now => {
    if (id !== drawId) return;                               // otra vista interrumpió el dibujo
    const p = Math.min((now - t0) / DRAW_MS, 1), e = p < .5 ? 2 * p * p : 1 - (-2 * p + 2) ** 2 / 2;
    cEq.setOption(frame(Math.round(oosAt - 1 + (n - oosAt) * e)), { replaceMerge: ['series'] });
    if (p < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

/* ---------- bootstrap: histograma + una fila de intervalo por fase ---------- */
function renderBoot() {
  const ph = P[view], counts = binsOf(ph), [ciLo, ciHi] = ph.research.ci95.map(pb), obs = pb(ph.research.difference);
  const rows = oosOpen ? ['Total', 'OOS', 'IS'] : ['IS'];
  const label = i => String(binX(i));
  const obsBin = Math.min(Math.floor((obs - binLo) / BIN), nBins - 1);
  const ciRow = key => {
    const on = rows.includes(key), sel = key === view, [a, b] = on ? P[key].research.ci95.map(pb) : [];
    return { id: 'ci' + key, type: 'line', xAxisIndex: 1, yAxisIndex: 1, silent: true, symbol: 'none',
      data: on ? [[a, key], [b, key]] : [], lineStyle: { color: css('--caution'), width: 6, opacity: sel ? .6 : .18, cap: 'round' } };
  };
  const top = oosOpen ? '48%' : '58%', stripTop = oosOpen ? '64%' : '80%';
  cBoot.setOption({
    ...anim,
    grid: [{ left: 44, right: 0, top: 18, height: top }, { left: 44, right: 0, top: stripTop, bottom: 22 }],
    tooltip: { ...tip(), trigger: 'axis', formatter: p => { const bar = p.find(x => x.seriesType === 'pictorialBar'); if (!bar) return ''; const i = bar.dataIndex; return `${fx(binX(i))} a ${fx(binX(i + 1))} ${U}: <b>${bar.value}</b> réplicas`; } },
    xAxis: [
      { type: 'category', gridIndex: 0, data: counts.map((_, i) => label(i)), ...axisBase(), axisLabel: { show: false } },
      // mismo rango que las barras: cada barra ocupa [x, x+1] en este eje
      { type: 'value', gridIndex: 1, min: binLo, max: binX(nBins), interval: BIN, ...axisBase(), splitLine: { show: false },
        axisPointer: { show: false, triggerTooltip: false }, axisLabel: { ...axisBase().axisLabel, formatter: v => Math.round(v / BIN) % 5 === 0 ? fx(v) : '' } }],
    yAxis: [
      { type: 'value', gridIndex: 0, ...axisBase(), axisLabel: { show: false }, splitLine: { show: false } },
      { type: 'category', gridIndex: 1, data: rows, ...axisBase(), axisLine: { show: false }, splitLine: { show: false },
        axisLabel: { ...axisBase().axisLabel, formatter: v => v, color: css('--muted') } }],
    series: [
      { ...dotBar, id: 'hist', xAxisIndex: 0, yAxisIndex: 0, barCategoryGap: '8%',
        data: counts.map((n, i) => { const x = binX(i), inCI = x + BIN > ciLo && x < ciHi;
          return { value: n, itemStyle: { color: x < 0 ? css('--neg') : css('--muted'), opacity: inCI ? .85 : .25 } }; }),
        markLine: { silent: true, symbol: 'none', data: [
          { xAxis: label(Math.round(-binLo / BIN)), lineStyle: { color: css('--ink'), width: 1.2, type: 'solid' }, label: { formatter: '0', color: css('--muted'), ...mono() } },
          { xAxis: label(obsBin), lineStyle: { color: css('--ink'), width: 1.2, type: 'dashed' }, label: { formatter: 'observado ' + nf(2).format(obs), color: css('--ink'), ...mono() } }] } },
      ciRow('IS'), ciRow('OOS'), ciRow('Total'),
      { id: 'ciZero', type: 'line', xAxisIndex: 1, yAxisIndex: 1, silent: true, data: [],
        markLine: { silent: true, symbol: 'none', label: { show: false }, data: [{ xAxis: 0, lineStyle: { color: css('--ink'), width: 1.2, type: 'solid' } }] } },
      { id: 'ciObs', type: 'scatter', xAxisIndex: 1, yAxisIndex: 1, silent: true, symbolSize: 10,
        data: rows.map(k => ({ value: [pb(P[k].research.difference), k], itemStyle: { color: css('--ink'), opacity: k === view ? 1 : .35, borderColor: css('--ground'), borderWidth: 2 } })) },
    ],
  });
}

/* ---------- por año: efecto dentro del año (barras) y total sin ese año (puntos) ---------- */
let years = [];
const yLabel = y => y === '2009' ? "'09*" : "'" + y.slice(2);
function renderYear() {
  const ph = P[view];
  years = Object.keys(oosOpen ? P.Total.research.by_year : P.IS.research.by_year);
  const byYear = (P.Total ?? P.IS).research.by_year;
  const isYear = y => y in P.IS.research.by_year;
  const inView = y => view === 'Total' || (view === 'IS' ? isYear(y) : !isYear(y));
  const loyo = years.map(y => ph.research.leave_one_year_out[y] != null ? pb(ph.research.leave_one_year_out[y]) : null);
  const full = pb(ph.research.difference);
  // escala de las barras según la magnitud del efecto (10 pb para H-001, 1 pb para H-007…)
  const barVals = years.map(y => Math.abs(pb(byYear[y])));
  const yStep = 10 ** Math.floor(Math.log10(Math.max(...barVals) || 1));
  const vals = loyo.filter(v => v != null).concat(0, full);
  // paso "redondo" (1, 2, 5 × 10ⁿ) para ~4 tramos: sirve igual para ±5 pb que para +50 %
  const raw = (Math.max(...vals) - Math.min(...vals)) / 4 || 1, mag = 10 ** Math.floor(Math.log10(raw));
  const loyoStep = mag * ([1, 2, 5].find(k => k * mag >= raw) ?? 10);
  const lo = Math.floor(Math.min(...vals) / loyoStep) * loyoStep, hi = Math.ceil(Math.max(...vals) / loyoStep) * loyoStep;
  cYear.setOption({
    ...anim,
    axisPointer: { link: [{ xAxisIndex: 'all' }] },
    tooltip: { ...tip(), trigger: 'axis', valueFormatter: v => v == null ? '—' : nf(2).format(v) + ' ' + U },
    grid: [{ left: 36, right: 0, top: 8, height: '40%' }, { left: 36, right: 0, top: '46%', bottom: 22 }],
    xAxis: [
      { type: 'category', gridIndex: 0, data: years.map(yLabel), ...axisBase(), axisLabel: { show: false } },
      { type: 'category', gridIndex: 1, data: years.map(yLabel), ...axisBase() }],
    yAxis: [
      { type: 'value', gridIndex: 0, splitNumber: 3, min: v => Math.min(0, Math.floor(v.min / yStep) * yStep), max: v => Math.max(0, Math.ceil(v.max / yStep) * yStep), ...axisBase() },
      { type: 'value', gridIndex: 1, min: lo, max: hi, interval: loyoStep, ...axisBase() }],
    series: [
      { ...dotBar, id: 'years', name: 'Dentro del año', xAxisIndex: 0, yAxisIndex: 0, barWidth: '58%',
        data: years.map(y => ({ value: pb(byYear[y]), itemStyle: { color: byYear[y] >= 0 ? css('--pos') : css('--neg'), opacity: !inView(y) ? .2 : y === '2009' ? .35 : .85 } })) },
      { id: 'loyo', name: 'Total sin ese año', type: 'scatter', xAxisIndex: 1, yAxisIndex: 1, symbolSize: 9,
        data: loyo.map(v => ({ value: v, itemStyle: { color: v < 0 ? css('--neg') : css('--faint') } })),
        markLine: { silent: true, symbol: 'none', data: [
          { yAxis: 0, lineStyle: { color: css('--ink'), width: 1.2, type: 'solid' }, label: { show: false } },
          { yAxis: full, lineStyle: { color: css('--ink'), type: 'dashed' }, label: { formatter: 'total ' + nf(2).format(full), color: css('--ink'), ...mono(), position: 'insideEndTop' } }] } },
    ],
  });
}

/* ---------- microinteracción: año en "Por año" → mismo año en la equity ---------- */
let hlYear = null;
function highlightYear(y) {
  if (y === hlYear) return; hlYear = y;
  const i0 = y ? dates.findIndex(d => d.startsWith(y)) : -1;
  const i1 = y ? dates.findLastIndex(d => d.startsWith(y)) : -1;
  const area = i0 < 0 ? [] : [[{ xAxis: dates[i0] }, { xAxis: dates[i1] }]];
  const style = { color: css('--ink'), opacity: .07 };
  cEq.setOption({ series: [
    { id: 'hl0', markArea: { silent: true, itemStyle: style, data: area, label: { show: true, position: 'insideTop', formatter: y || '', color: css('--ink'), ...mono() } } },
    { id: 'hl1', markArea: { silent: true, itemStyle: style, data: area } },
  ] });
}
cYear.on('updateAxisPointer', e => { const info = e.axesInfo && e.axesInfo[0]; highlightYear(info ? years[info.value] : null); });
cYear.getZr().on('globalout', () => highlightYear(null));

/* ---------- cambio de fase ---------- */
function setView(v) {
  view = v; hlYear = null;
  document.documentElement.dataset.state = P[v].state;   // color de la línea superior
  renderPhases(); renderSpec(); updateKPIs();
  renderEq(); renderBoot(); renderYear();
}

/* ---------- arranque + tema ---------- */
setView('IS');
new ResizeObserver(() => charts.forEach(c => c.resize())).observe(document.querySelector('.dash-main'));
const retheme = () => { hlYear = null; renderEq(); renderBoot(); renderYear(); };
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', retheme);
new MutationObserver(retheme).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
if (document.fonts && document.fonts.ready) document.fonts.ready.then(retheme);
