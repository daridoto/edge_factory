// Lee la salida del lab (sentinel2/resultados, enlazada en public/lab) y la organiza por fases.
// Cada fase tiene la misma forma, así el dashboard pinta cualquiera igual:
//   { key, state, start, end, equity: [[fecha, equity, exposición]], trades: [{ net, cost }], research }
// Si cambia el formato del lab, este es el único sitio que hay que tocar.
//
// Por experimento, el lab deja: resumen.json, equity.csv y operaciones.csv (esquemas en ../esquemas/);
// opcionalmente, variantes.csv (una fila por sesión y ventana; ver src/variantes.js).

const LAB = '/lab';

const fetchOk = async url => {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`No se pudo cargar ${url} (${res.status})`);
  return res;
};
const getJSON = async url => (await fetchOk(url)).json();

// CSV del lab: cabecera + filas numéricas, sin comillas; líneas terminadas en CRLF.
async function getCSV(url) {
  const [head, ...rows] = (await (await fetchOk(url)).text()).trim().split(/\r?\n/);
  const keys = head.split(',');
  return rows.map(r => Object.fromEntries(r.split(',').map((v, i) => [keys[i], v])));
}

// Registro de hipótesis: nombre, reglas, costes, estados y experimento de cada fase (public/data/hipotesis.json).
export const loadRegistro = () => getJSON('/data/hipotesis.json');

// Índice del lab: una fila por experimento (id, hipotesis, muestra…), en orden de ejecución.
export const loadIndice = () => getCSV(`${LAB}/indice.csv`);

// Un experimento del lab: resumen y, con simulación al 100 % del capital (lab ≥ 2.1), esa equity y operaciones:
// el riesgo es comparable entre tamaños.
async function loadExp(id, withVariants = false) {
  const dir = `${LAB}/${id}`;
  const r = await getJSON(`${dir}/resumen.json`);
  const f = r.ficheros, al100 = !!f.equity_100;
  const [equity, trades, variantes] = await Promise.all([getCSV(`${dir}/${al100 ? f.equity_100 : f.equity}`),
                                              getCSV(`${dir}/${al100 ? f.operaciones_100 : f.operaciones}`),
                                              withVariants && f.variantes ? getCSV(`${dir}/${f.variantes}`) : null]);
  return { r, equity, trades, variantes, al100 };
}

// Fases: IS siempre; OOS y Total si el registro las nombra (experimentos del lab con muestra OOS / Total).
export async function loadFicha(entry) {
  const is = await loadExp(entry.experimentos.IS, true);
  const view = toView(is.r, is.equity, is.trades, entry);
  for (const key of ['OOS', 'Total']) {
    const id = entry.experimentos[key];
    if (!id) continue;
    const e = await loadExp(id);
    if (e.r.experimento.muestra !== key) throw new Error(`${id} no es un experimento ${key}`);
    view.phases[key] = toPhase(key, e.r, e.equity, e.trades, entry);
  }
  if (is.variantes) view.variants = toVariants(is.r, is.variantes, is.al100);
  return view;
}

// variantes.csv → { meta, fraccion, rows: Map(ventana → Map(fecha → fila)) }. Celda vacía = sin dato.
function toVariants(r, filas, al100) {
  const num = v => v === '' ? null : +v;
  const rows = new Map(Object.keys(r.variantes.ventanas).map(k => [k, new Map()]));
  for (const x of filas)
    rows.get(x.ventana).set(x.fecha, { entrada: +x.entrada, salida: +x.salida, senal: num(x.senal), serie: num(x.serie), desfase: x.desfase === 'True' });
  // misma fracción que la equity que se pinta: así, sin toggles, la simulación reproduce la del lab
  return { meta: r.variantes, fraccion: al100 ? r.referencia.fraccion : 1, rows };
}

// El dashboard trabaja en fracciones (× 10.000 = pb); el lab publica en pb.
const frac = v => v / 1e4;
const fracMap = o => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, frac(v)]));
const PLURAL = { mes: 'meses', 'día': 'días', semana: 'semanas', hora: 'horas' };

// Retorno neto de cada operación sobre la equity de la sesión anterior a la entrada (el capital disponible al entrar).
function tradesWithReturn(trades, equity, capital) {
  const before = new Map(equity.map((e, i) => [e.fecha, i ? +equity[i - 1].equity : capital]));
  return trades.map(t => ({ net: +t.pnl_neto, cost: +t.coste_entrada + +t.coste_salida, ret: +t.pnl_neto / before.get(t.entrada) }));
}

function toView(r, equity, trades, entry) {
  const x = r.experimento, boot = r.robustez.bootstrap;
  return {
    id: x.hipotesis,
    name: entry.nombre ?? x.hipotesis,
    entry,
    exp: x.id,
    frozen: x.fecha,
    identity: { instrument: x.instrumento, frequency: x.frecuencia },
    repro: { seed: boot.semilla },
    initialEquity: x.capital_inicial,
    // tamaño con el que está simulada la equity que se pinta
    sizing: r.referencia ? '100 % del capital' : null,
    phases: { IS: toPhase('IS', r, equity, trades, entry) },
  };
}

function toPhase(key, r, equity, trades, entry) {
  const x = r.experimento, ev = r.evidencia, boot = r.robustez.bootstrap;
  // componentes: [n ventana, n resto, media ventana, media resto], en ese orden; sin resto (n resto = 0), sin su media
  const [nWin, nRest, meanWin, meanRest] = ev.componentes.map(c => c.valor);
  return {
    key,
    state: entry.estados?.[key] ?? 'inconclusive',
    start: x.inicio,
    end: x.fin,
    periodsPerYear: r.procedencia.periodos_por_anio,
    capital: x.capital_inicial,
    equity: equity.map(e => [e.fecha, +e.equity, +e.exposicion]),
    trades: tradesWithReturn(trades, equity, x.capital_inicial),
    research: {
      question: x.pregunta,
      statistic: ev.estadistico,
      unit: ev.unidad,
      bootstrap: { replicas: boot.replicas, bloque: `${boot.bloque} ${boot.bloque > 1 ? PLURAL[boot.unidad] ?? boot.unidad : boot.unidad}` },
      n_tom: nWin, n_rest: nRest,
      mean_tom: frac(meanWin), mean_rest: nRest ? frac(meanRest) : null,
      difference: frac(ev.valor),
      ci95: [frac(boot.ic_inf), frac(boot.ic_sup)],
      by_year: fracMap(r.robustez.por_anio),
      leave_one_year_out: fracMap(r.robustez.sin_cada_anio),
      cost_stress_net: r.robustez.pnl_costes_x2,
    },
  };
}
