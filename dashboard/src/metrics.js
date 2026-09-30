// Métricas económicas de una fase, calculadas igual para IS, OOS y Total.
// Convenciones: sesiones/año del lab (phase.periodsPerYear; 252 por defecto, 365 en cripto), rf = 0, desviación muestral (ddof = 1).

export function computeMetrics(phase) {
  const A = phase.periodsPerYear ?? 252;
  const eq = phase.equity.map(e => e[1]);
  // el primer día cuenta con retorno 0 frente al capital inicial (igual que el motor del lab)
  const r = eq.map((v, i) => i ? v / eq[i - 1] - 1 : 0);
  const mean = r.reduce((a, b) => a + b, 0) / r.length;
  const sd = Math.sqrt(r.reduce((a, b) => a + (b - mean) ** 2, 0) / (r.length - 1));
  const down = Math.sqrt(r.reduce((a, b) => a + Math.min(b, 0) ** 2, 0) / r.length);

  let peak = -Infinity, peakAt = 0, maxDD = 0;
  eq.forEach((v, i) => { if (v >= peak) { peak = v; peakAt = i; } maxDD = Math.max(maxDD, 1 - v / peak); });
  const openDDAge = eq[eq.length - 1] < peak ? eq.length - 1 - peakAt : 0;

  const nets = phase.trades.map(t => t.net);
  const wins = nets.filter(v => v > 0), losses = nets.filter(v => v < 0);   // PnL 0: ni gana ni pierde
  const sum = a => a.reduce((x, y) => x + y, 0);
  const avgWin = wins.length ? sum(wins) / wins.length : 0;
  const avgLoss = losses.length ? Math.abs(sum(losses) / losses.length) : 0;
  const costs = sum(phase.trades.map(t => t.cost));
  const pnl = eq[eq.length - 1] - eq[0];

  return {
    pnl,
    pnlCosts2x: pnl - costs,
    trades: nets.length,
    exposure: phase.equity.reduce((a, e) => a + e[2], 0) / phase.equity.length,   // fracción media de cada sesión con posición
    winRate: nets.length ? wins.length / nets.length : 0,
    payoff: avgLoss ? avgWin / avgLoss : 0,
    profitFactor: losses.length ? sum(wins) / Math.abs(sum(losses)) : 0,
    sharpe: Math.sqrt(A) * mean / sd,
    sortino: Math.sqrt(A) * mean / down,
    maxDD,
    openDDAge,
  };
}
