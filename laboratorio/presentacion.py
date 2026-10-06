"""ficha.md: lectura humana generada solo desde resumen.json (sirve para cualquier hipótesis)."""


def n(x, decimales=2):
    return f"{x:,.{decimales}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def _referencia(r):
    if r is None:
        return ["**Referencia al 100 % del capital:** no calculada (experimento anterior al esquema 2.1).", ""]
    return [
        f"**Referencia al 100 % del capital** (la misma operativa con el {n(r.fraccion * 100, 1)} % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):", "",
        "| Riesgo | Valor |", "|---|---:|",
        f"| Máximo drawdown | **{n(r.max_drawdown * 100)} %** |",
        f"| Pico → valle | {r.pico} → {r.valle} |",
        f"| Recuperación | {r.recuperacion or 'no recupera en la muestra'} |",
        f"| Sesiones bajo el agua | {r.sesiones_bajo_agua} |",
        f"| Rentabilidad total | {n(r.rentabilidad_total * 100)} % |",
        f"| Rentabilidad anual | {'no calculable' if r.rentabilidad_anual is None else n(r.rentabilidad_anual * 100) + ' %'} |",
        f"| Sharpe | {'no calculable' if r.sharpe is None else n(r.sharpe)} |", "",
    ]


def _variantes(v):
    if v is None:
        return []
    ventanas = ", ".join(f"{k} {a}–{b}" + (" (base)" if k == v.base else "") for k, (a, b) in v.ventanas.items())
    return [
        "## Variantes (para el dashboard)", "",
        f"[variantes.csv](variantes.csv): {v.filas} filas, una por sesión y ventana ({ventanas}). "
        f"Con cada una: retorno de la sesión previa {'–'.join(v.senal) if v.senal else '(sin señal)'}, "
        f"{v.serie or 'sin serie'} de la sesión previa y si es semana de desfase horario EE. UU.–Europa. "
        "La ventana base reproduce el libro de operaciones. Las combinaciones se calculan en el dashboard "
        "y no pasan por la batería: son exploratorias.", "",
    ]


def _sensibilidad(filas):
    if not filas:
        return []
    return [
        "## Sensibilidad del tamaño por serie (se informa, no se elige)", "",
        "Al 100 % del capital por unidad de tamaño (multiplicador > 1 = apalancamiento). La diferencia es el retorno bruto "
        "medio por operación sobre el umbral menos el resto y no depende del multiplicador.", "",
        "| Umbral | Ops sobre umbral | Diferencia (pb) | × | Rentabilidad total | Máx. drawdown | Sharpe |",
        "|---:|---:|---:|---:|---:|---:|---:|",
        *[f"| {n(f.umbral, 0)} | {f.operaciones_sobre_umbral} | {'—' if f.diferencia is None else n(f.diferencia)} | "
          f"{n(f.multiplicador, 1)} | {n(f.rentabilidad_total * 100)} % | {n(f.max_drawdown * 100)} % | "
          f"{'—' if f.sharpe is None else n(f.sharpe)} |" for f in filas], "",
    ]


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
        (f"**{e.muestra} de {e.base} · EXPLORATORIA**" if e.base else "**SOLO IS · EXPLORATORIA**") + (" · **DATOS SINTÉTICOS: no es evidencia**" if e.sintetico else ""), "",
        f"**Recorrido:** [receta](../../{e.receta}) → [plan](../../{e.plan}) → esta ficha · "
        "datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)", "",
        f"> {c.lectura}", "",
        f"**Muestra:** {e.inicio} → {e.fin} · {e.instrumento} {e.frecuencia} · experimento {e.id}. " + (f"{e.muestra} autorizada; misma especificación que la base." if e.base else "OOS y holdout no utilizados."), "",
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
        f"| Máximo drawdown (tamaño del plan) | {n(m.max_drawdown * 100)} % |",
        f"| Sharpe | {opcional(m.sharpe)} |",
        f"| Costes | {n(m.costes)} {e.moneda} |", "",
        *_referencia(resumen.referencia),
        *_variantes(resumen.variantes),
        *_sensibilidad(resumen.sensibilidad),
        "Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../esquemas/resumen.schema.json).", "",
        "## Supuestos y límites", "",
        *[f"- {x}" for x in c.supuestos + c.limites], "",
        "## Siguiente comprobación (propuesta, sin ejecutar)", "",
        c.siguiente_comprobacion, "",
    ]
    return "\n".join(lineas)
