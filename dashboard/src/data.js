// Lee la salida del lab (sentinel2/resultados, enlazada en public/lab) y la organiza por fases.
// Cada fase tiene la misma forma, así el dashboard pinta cualquiera igual:
//   { key, state, start, end, equity: [[fecha, equity, exposición]], trades: [{ net, cost }], research }
// Si cambia el formato del lab, este es el único sitio que hay que tocar.
//
// Por experimento, el lab deja: resumen.json, equity.csv y operaciones.csv (esquemas en sentinel2/esquemas/).

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

export async function loadFicha(entry) {
  const dir = `${LAB}/${entry.experimentos.IS}`;
  const r = await getJSON(`${dir}/resumen.json`);
  const [equity, trades] = await Promise.all([getCSV(`${dir}/${r.ficheros.equity}`), getCSV(`${dir}/${r.ficheros.operaciones}`)]);
  return toView(r, equity, trades, entry);
}

// El dashboard trabaja en fracciones (× 10.000 = pb); el lab publica en pb.
const frac = v => v / 1e4;
const fracMap = o => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, frac(v)]));
const PLURAL = { mes: 'meses', 'día': 'días', semana: 'semanas', hora: 'horas' };

function toView(r, equity, trades, entry) {
  const x = r.experimento, ev = r.evidencia, boot = r.robustez.bootstrap;
  // componentes: [n ventana, n resto, media ventana, media resto], en ese orden
  const [nWin, nRest, meanWin, meanRest] = ev.componentes.map(c => c.valor);
  return {
    id: x.hipotesis,
    name: entry.nombre ?? x.hipotesis,
    entry,
    exp: x.id,
    frozen: x.fecha,
    identity: { instrument: x.instrumento, frequency: x.frecuencia },
    repro: { seed: boot.semilla },
    initialEquity: x.capital_inicial,
    phases: {
      IS: {
        key: 'IS',
        state: entry.estados?.IS ?? 'inconclusive',
        start: x.inicio,
        end: x.fin,
        periodsPerYear: r.procedencia.periodos_por_anio,
        equity: equity.map(e => [e.fecha, +e.equity, +e.exposicion]),
        trades: trades.map(t => ({ net: +t.pnl_neto, cost: +t.coste_entrada + +t.coste_salida })),
        research: {
          question: x.pregunta,
          statistic: ev.estadistico,
          unit: ev.unidad,
          bootstrap: { replicas: boot.replicas, bloque: `${boot.bloque} ${boot.bloque > 1 ? PLURAL[boot.unidad] ?? boot.unidad : boot.unidad}` },
          n_tom: nWin, n_rest: nRest,
          mean_tom: frac(meanWin), mean_rest: frac(meanRest),
          difference: frac(ev.valor),
          ci95: [frac(boot.ic_inf), frac(boot.ic_sup)],
          by_year: fracMap(r.robustez.por_anio),
          leave_one_year_out: fracMap(r.robustez.sin_cada_anio),
          cost_stress_net: r.robustez.pnl_costes_x2,
        },
      },
    },
  };
}
