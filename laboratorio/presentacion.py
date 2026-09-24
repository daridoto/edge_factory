"""ficha.md: lectura humana generada solo desde resumen.json (sirve para cualquier hipótesis)."""


def n(x, decimales=2):
    return f"{x:,.{decimales}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def render(resumen):
    e, ev, rb, m, c = (resumen.experimento, resumen.evidencia, resumen.robustez,
                       resumen.metricas, resumen.conclusiones)
    b = rb.bootstrap
    u = ev.unidad
    anios = rb.por_anio
    positivos = sum(v > 0 for v in anios.values())
    sin = rb.sin_cada_anio
    giran = [a for a, v in sin.items() if (v > 0) != (ev.valor > 0)]

    def opcional(valor, sufijo=""):
        return "no calculable" if valor is None else n(valor) + sufijo

    lineas = [
        f"# {e.hipotesis} · {e.pregunta}", "",
        "**SOLO IS · EXPLORATORIA**" + (" · **DATOS SINTÉTICOS: no es evidencia**" if e.sintetico else ""), "",
        f"**Recorrido:** [receta](../../{e.receta}) → [plan](../../{e.plan}) → esta ficha · "
        "datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)", "",
        f"> {c.lectura}", "",
        f"**Muestra:** {e.inicio} → {e.fin} · {e.instrumento} {e.frecuencia} · experimento {e.id}. OOS y holdout no utilizados.", "",
        "## Evidencia", "",
        "| | Valor |", "|---|---:|",
        *[f"| {x.nombre} | {n(x.valor, 0 if x.valor.is_integer() else 2)} {x.unidad} |" for x in ev.componentes],
        f"| **{ev.estadistico}** | **{n(ev.valor)} {u}** |",
        f"| Intervalo bootstrap {n(b.nivel * 100, 0)} % | [{n(b.ic_inf)}; {n(b.ic_sup)}] {u} |", "",
        f"Bootstrap por {b.metodo} (bloque = {b.bloque} × {b.unidad}, {n(b.replicas, 0)} réplicas, semilla {b.semilla}). "
        f"{b.motivo} El intervalo **{'incluye' if b.incluye_cero else 'no incluye'} cero**.", "",
        *(["| Desglose | " + " | ".join(ev.desglose) + " |", "|---|" + "---:|" * len(ev.desglose),
           f"| {u} | " + " | ".join(n(x) for x in ev.desglose.values()) + " |", ""] if ev.desglose else []),
        "## Robustez", "",
        f"- Positivo en **{positivos} de {len(anios)} años**.",
        (f"- Quitando un año cada vez: entre **{n(min(sin.values()))} y {n(max(sin.values()))} {u}**." if sin
         else "- Un solo año: no se puede excluir ninguno."),
        ("- **Cambia de signo al excluir " + ", ".join(giran) + ".**") if giran else "- No cambia de signo al excluir ningún año.",
        f"- PnL de la simulación con costes ×2: {n(rb.pnl_costes_x2)} {e.moneda}.", "",
        "| Año | " + " | ".join(anios) + " |", "|---|" + "---:|" * len(anios),
        f"| {u} | " + " | ".join(n(v) for v in anios.values()) + " |", "",
        "## Simulación de la operativa", "",
        f"- **Entrada:** {e.reglas.entrada}", f"- **Salida:** {e.reglas.salida}",
        f"- **Tamaño:** {e.reglas.tamano}", f"- **Costes:** {e.reglas.costes}", "",
        "| Resultado | Valor |", "|---|---:|",
        f"| Operaciones | {m.operaciones} |",
        f"| PnL neto | {n(m.pnl_neto)} {e.moneda} |",
        f"| Resultado medio por operación | {opcional(m.esperanza, ' ' + e.moneda)} |",
        f"| Tasa de acierto | {opcional(None if m.tasa_acierto is None else m.tasa_acierto * 100, ' %')} |",
        f"| Rentabilidad sobre {n(e.capital_inicial, 0)} {e.moneda} | {n(m.rentabilidad_total * 100)} % |",
        f"| Máximo drawdown | {n(m.max_drawdown * 100)} % |",
        f"| Sharpe | {opcional(m.sharpe)} |",
        f"| Costes | {n(m.costes)} {e.moneda} |", "",
        "Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../esquemas/resumen.schema.json).", "",
        "## Supuestos y límites", "",
        *[f"- {x}" for x in c.supuestos + c.limites], "",
        "## Siguiente comprobación (propuesta, sin ejecutar)", "",
        c.siguiente_comprobacion, "",
    ]
    return "\n".join(lineas)
