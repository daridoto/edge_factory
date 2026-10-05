// Variantes en vivo (toggles) a partir de variantes.csv del lab: una fila por sesión y ventana con precios de
// entrada y salida, la señal y la serie (VIX) de la sesión previa y si es semana de desfase horario.
// Simula la combinación elegida con la misma contabilidad que la referencia al 100 % del lab:
//   unidades = fracción · tamaño · equity previa / entrada · coste = coste_lado por unidad y lado
// así, sin ningún toggle, reproduce equity_100.csv. Exploratorio: sin bootstrap ni batería.

export const BUCKETS = [['≤ 15', -Infinity, 15], ['15–20', 15, 20], ['20–30', 20, 30], ['> 30', 30, Infinity]];
export const DEFAULTS = { ventana: null, btd: false, filtro: false, umbral: 20, desfase: false, tamano: false, k: 2 };

// ¿Algún toggle cambia la operativa respecto a la base del lab?
export const isBase = (o, meta) => o.ventana === meta.base && !o.btd && !o.filtro && !o.desfase && !(o.tamano && o.k !== 1);

/** Fase simulada { equity: [[fecha, equity, exposición]], trades: [{ net, cost, ret, serie }] } en el calendario del lab. */
export function simulate(V, phase, o) {
  const { meta, rows, fraccion } = V, c2 = 2 * meta.coste_lado;
  const win = o.ventana ?? meta.base, hours = h => { const [a, b] = h.map(t => +t.slice(0, 2) + +t.slice(3) / 60); return b - a; };
  const ratio = hours(meta.ventanas[win]) / hours(meta.ventanas[meta.base]);
  const byDate = rows.get(win);
  let E = phase.capital;
  const equity = [], trades = [];
  for (const [fecha, , expo] of phase.labEquity) {
    const r = byDate.get(fecha);
    let x = 0;
    if (r) {
      let on = true;
      if (o.btd && !(r.senal != null && r.senal < 0)) on = false;
      if (o.filtro && !(r.serie != null && r.serie > o.umbral)) on = false;
      if (o.desfase && r.desfase) on = false;
      const w = o.tamano && r.serie != null && r.serie > o.umbral ? o.k : 1;
      if (on && w > 0) {
        const units = fraccion * w * E / r.entrada, cost = units * c2, net = units * (r.salida - r.entrada) - cost;
        trades.push({ net, cost, ret: net / E, serie: r.serie });
        E += net;
        x = Math.min(1, (expo || hours(meta.ventanas[meta.base]) / 23) * ratio);
      }
    }
    equity.push([fecha, E, x]);
  }
  return { equity, trades };
}

/** Retorno neto medio por operación (pb) y nº de operaciones por tramo de la serie (VIX). */
export function byBucket(trades) {
  return BUCKETS.map(([label, lo, hi]) => {
    const xs = trades.filter(t => t.serie != null && t.serie > lo && t.serie <= hi).map(t => t.ret);
    return { label, n: xs.length, pb: xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length * 1e4 : 0 };
  });
}
