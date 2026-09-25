// Comparativa: una hipótesis probada en varios instrumentos (entradas del registro con el mismo `hipotesis`).
// Responde, de arriba abajo: ¿en qué instrumentos aparece el efecto? · ¿cómo se habría vivido operándolo?
// · ¿qué años lo sostienen en todos? · cifras por instrumento. Clic en una fila → su ficha.
import * as echarts from 'echarts';
import { loadRegistro, loadFicha } from './data.js';
import { computeMetrics } from './metrics.js';

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

const hid = location.hash.slice(1);
const group = (await loadRegistro()).filter(e => e.hipotesis === hid);
const fichas = await Promise.all(group.map(loadFicha));
// una fila por instrumento, de mayor a menor efecto
// color por instrumento en orden del registro (sigue a la entidad, no al puesto)
const items = fichas.map((D, k) => {
  const e = group[k], ph = D.phases.IS, r = ph.research, m = computeMetrics(ph);
  const years = Object.values(r.by_year);
  return { e, D, ph, r, m, name: D.identity.instrument, color: `--series-${k + 1}`, effect: pb(r.difference), ci: r.ci95.map(pb),
    up: years.filter(v => v > 0).length, nYears: years.length, worstLoyo: Math.min(...Object.values(r.leave_one_year_out).map(pb)),
    ret: m.pnl / D.initialEquity * 100 };
}).sort((a, b) => b.effect - a.effect);
const first = items[0], U = first.r.unit;

/* ---------- cabecera ---------- */
const efecto = first.e.efecto;
$('c-name').textContent = `${efecto} · ${items.map(i => i.name).join(' ')}`;
document.title = `${hid} · ${efecto}`;
$('c-q').textContent = first.r.question.replace(first.name, 'el índice');
$('c-spec').innerHTML = [
  ...Object.entries(first.e.reglas),
  ['Periodo', `${fdate(first.ph.start)} → ${fdate(first.ph.end)}`],
  ['Capital', `${nf(0).format(first.D.initialEquity)} USD`],
  ['Costes', first.e.costes],
].map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`).join('');
const states = [...new Set(items.map(i => i.e.estados?.IS ?? i.ph.state))];
const state = states.length === 1 ? states[0] : 'inconclusive';
document.documentElement.dataset.state = state;
$('c-phases').innerHTML = `<button class="phase ${STATE[state][1]}" aria-pressed="true">IS · ${STATE[state][0]}</button>`
  + '<button class="phase" disabled>OOS · pendiente</button><button class="phase" disabled>Holdout · pendiente</button>';
$('c-sub-ci').textContent = `${U} · ${first.r.bootstrap.replicas.toLocaleString('es-ES', { useGrouping: 'always' })} réplicas · bloques de ${first.r.bootstrap.bloque}`;
$('c-sub-eq').textContent = `% sobre ${nf(0).format(first.D.initialEquity)} USD · ${first.e.reglas['Tamaño'] ?? ''} por entrada`;
$('c-foot').textContent = `${hid} · ${items.map(i => i.D.exp).join(' · ')}`;

/* ---------- gráficos: base común (igual que la ficha) ---------- */
const mono = () => ({ fontFamily: 'IBM Plex Mono', fontSize: 11 });
const axisBase = () => ({ axisLine: { lineStyle: { color: css('--rule') } }, axisTick: { show: false }, axisLabel: { color: css('--muted'), ...mono() }, splitLine: { lineStyle: { color: css('--rule'), type: [1, 3] } } });
const tip = () => ({ backgroundColor: css('--surface'), borderColor: css('--rule'), textStyle: { color: css('--ink'), fontFamily: 'IBM Plex Sans', fontSize: 13 } });
// solo se anima el primer dibujo; el resaltado redibuja sin animación
let booted = false;
const anim = () => ({ animation: !reduced && !booted, animationDuration: 700 });
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
    grid: { left: 44, right: 12, top: 8, bottom: 22 },
    tooltip: { ...tip(), trigger: 'item', formatter: p => { const i = items.find(x => x.name === p.data.name);
      return `<b>${i.name}</b> ${sgn(i.effect)} ${U}<br>IC ${nf(2).format(i.ci[0])} a ${nf(2).format(i.ci[1])} · ${i.up}/${i.nYears} años +`; } },
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
    grid: { left: 44, right: 44, top: 8, bottom: 22 },
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
  const years = Object.keys(first.r.by_year);
  const vals = items.map(i => years.map(y => pb(i.r.by_year[y])));
  const max = Math.max(...vals.flat().map(Math.abs));
  const yl = y => (y === years[0] ? `'${y.slice(2)}*` : `'${y.slice(2)}`);
  const cell = (v, name) => `<span class="yc" data-name="${name}" style="--c:var(--${v > 0 ? 'pos' : 'neg'});--a:${Math.round(12 + 70 * Math.abs(v) / max)}%" title="${nf(2).format(v)} ${U}">${sgn(v, 1)}</span>`;
  const all = years.map((_, j) => { const col = vals.map(r => r[j]);
    return col.every(v => v > 0) ? '<span class="ya pos" title="positivo en todos">▲</span>'
      : col.every(v => v < 0) ? '<span class="ya neg" title="negativo en todos">▼</span>' : '<span class="ya">·</span>'; });
  $('c-years').style.setProperty('--ny', years.length);
  $('c-years').innerHTML = `<span></span>${years.map(y => `<span class="yh">${yl(y)}</span>`).join('')}`
    + items.map((i, k) => `<span class="yn" data-name="${i.name}"><i class="sw" style="--sc:var(${i.color})"></i>${i.name}</span>${vals[k].map(v => cell(v, i.name)).join('')}`).join('')
    + `<span class="yn yt">todos</span>${all.join('')}`;
  $('c-years-sub').textContent = `${U} · * ${years[0]} desde ${fdate(first.ph.start).slice(3)}`;
}

/* ---------- tabla por instrumento ---------- */
function renderTable() {
  const th = ['', `Efecto ${efecto}`, 'IC 95 %', 'Años +', 'Rentab.', 'PnL', 'Max DD', 'Sharpe', 'Win rate', 'Peor sin 1 año'];
  const td = i => [
    `<i class="sw" style="--sc:var(${i.color})"></i><b>${i.name}</b>`,
    `<span class="${sign(i.effect)}">${sgn(i.effect)}</span>`,
    `${nf(2).format(i.ci[0])} a ${nf(2).format(i.ci[1])}${i.ci[0] < 0 && i.ci[1] > 0 ? ' <span class="warn">cruza 0</span>' : ''}`,
    `${i.up}/${i.nYears}`,
    `<span class="${sign(i.ret)}">${sgn(i.ret)} %</span>`,
    `${nf(0).format(i.m.pnl)} USD`,
    `${nf(2).format(-i.m.maxDD * 100)} %`,
    nf(2).format(i.m.sharpe),
    `${nf(0).format(i.m.winRate * 100)} %`,
    `<span class="${sign(i.worstLoyo)}">${sgn(i.worstLoyo)}</span>`,
  ];
  $('c-table').innerHTML = `<div class="tr th">${th.map(h => `<span>${h}</span>`).join('')}</div>`
    + items.map(i => `<a class="tr" href="#${i.e.id}" data-name="${i.name}">${td(i).map(c => `<span>${c}</span>`).join('')}</a>`).join('');
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
const render = () => { renderCI(); renderEq(); renderYears(); renderTable(); renderFilter(); };
render();
booted = true;
new ResizeObserver(() => { cCI.resize(); cEq.resize(); }).observe($('cmp'));
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', render);
new MutationObserver(render).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
if (document.fonts && document.fonts.ready) document.fonts.ready.then(render);
