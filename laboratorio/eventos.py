"""Operativa por eventos: una señal diaria abre una operación de tenencia fija con stop.

- Señal (SENALES): días en que se cumple una condición sobre una serie auxiliar. Tras cada señal usada,
  `enfriamiento` días naturales sin señales nuevas (vuelve a aceptar el día t + enfriamiento).
- Operación: compra a la apertura de la primera barra posterior al día de señal t. Stop si el mínimo de
  una barra toca entrada × (1 - stop): sale al stop, o a la apertura si ya abre por debajo. Si no salta,
  sale al cierre de la última barra con fecha ≤ t + tenencia. Solo se opera si esa fecha cae en la muestra.
- Tamaño: `fraccion` de la equity previa, incluido el coste de entrada. Coste: `coste_pct` del nocional por lado.
- La cuenta se valora al cierre de cada barra (mark-to-market), así el drawdown incluye el de dentro de cada operación.
- Placebo: el mismo número de operaciones en días de señal aleatorios, separados por el enfriamiento.
"""
from collections import namedtuple
from datetime import timedelta
import random
import statistics as st

from .contratos import Operacion, Sesion

Salida = namedtuple("Salida", "i_entrada i_salida entrada salida motivo")


# ---------- señales ----------

def ratio_medianas(serie, corta, larga, umbral):
    """Días en que mediana(últimos `corta` datos) / mediana(últimos `larga` datos) ≥ umbral.
    Las ventanas cuentan días con dato (los huecos se saltan); sin `larga` datos no hay señal."""
    fechas, valores = list(serie), list(serie.values())
    dias = []
    for i in range(larga - 1, len(valores)):
        base = st.median(valores[i - larga + 1:i + 1])
        if base > 0 and st.median(valores[i - corta + 1:i + 1]) / base >= umbral:
            dias.append(fechas[i])
    return dias


SENALES = {"ratio_medianas": ratio_medianas}


def aplicar_enfriamiento(dias, enfriamiento):
    usados = []
    for d in sorted(dias):
        if not usados or d >= usados[-1] + timedelta(days=enfriamiento):
            usados.append(d)
    return usados


# ---------- operación ----------

def salida(barras, t, tenencia, stop):
    """Salida de la operación de la señal del día t, o None si no hay entrada o no cierra dentro de la muestra."""
    fechas = [b.ts.date() for b in barras]
    i = next((k for k, f in enumerate(fechas) if f > t), None)
    limite = t + timedelta(days=tenencia)
    if i is None or limite > fechas[-1]:
        return None
    entrada = barras[i].open
    nivel = entrada * (1 - stop)
    j = i
    while True:
        b = barras[j]
        if b.open <= nivel:
            return Salida(i, j, entrada, b.open, "stop en apertura")
        if b.low <= nivel:
            return Salida(i, j, entrada, nivel, "stop")
        if j + 1 == len(barras) or fechas[j + 1] > limite:
            return Salida(i, j, entrada, b.close, "tiempo")
        j += 1


def retorno_neto(s, coste_pct):
    """Retorno de la operación sobre lo invertido (nocional + coste de entrada)."""
    return s.salida * (1 - coste_pct) / (s.entrada * (1 + coste_pct)) - 1


# ---------- simulación ----------

def simular(barras, dias_senal, tenencia, stop, capital, coste_pct, fraccion=1.0):
    """Devuelve (sesiones, operaciones, detalle); detalle = [(día de señal, Salida, retorno neto)]."""
    if not 0 < fraccion <= 1:
        raise ValueError("fraccion debe estar en (0, 1]; no se permite apalancamiento")
    planes = [(t, s) for t in dias_senal if (s := salida(barras, t, tenencia, stop))]
    for (_, a), (_, b) in zip(planes, planes[1:]):
        if b.i_entrada <= a.i_salida:
            raise ValueError("Operaciones solapadas: el enfriamiento debe cubrir la tenencia")
    por_entrada = {s.i_entrada: (t, s) for t, s in planes}
    sesiones, operaciones, detalle = [], [], []
    equity, abierta, unidades = capital, None, 0.0
    for k, b in enumerate(barras):
        bruto = coste = nocional = 0.0
        if k in por_entrada:
            abierta = por_entrada[k]
            s = abierta[1]
            unidades = fraccion * equity / (s.entrada * (1 + coste_pct))
            c_entrada = coste_pct * unidades * s.entrada
            coste += c_entrada
            nocional += unidades * s.entrada
            previo = s.entrada
        elif abierta:
            previo = barras[k - 1].close
        if abierta:
            t, s = abierta
            final = s.salida if k == s.i_salida else b.close
            bruto = unidades * (final - previo)
            if k == s.i_salida:
                c_salida = coste_pct * unidades * s.salida
                coste += c_salida
                nocional += unidades * s.salida
                pnl = unidades * (s.salida - s.entrada)
                operaciones.append(Operacion(id=f"T{len(operaciones) + 1:04d}", entrada=barras[s.i_entrada].ts.date(),
                                             salida=b.ts.date(), pnl_bruto=pnl, coste_entrada=c_entrada,
                                             coste_salida=c_salida, pnl_neto=pnl - c_entrada - c_salida))
                detalle.append((t, s, retorno_neto(s, coste_pct)))
        equity += bruto - coste
        sesiones.append(Sesion(fecha=b.ts.date(), equity=equity, pnl_bruto=bruto, coste=coste, nocional=nocional,
                               exposicion=1.0 if abierta else 0.0))
        if abierta and k == abierta[1].i_salida:
            abierta = None
    return sesiones, operaciones, detalle


def placebo(barras, candidatos, n, tenencia, stop, coste_pct, separacion, sorteos=2000, semilla=7301):
    """Medias (en fracción) del retorno neto de `n` operaciones en días aleatorios separados ≥ `separacion` días."""
    rng = random.Random(semilla)
    cache, medias = {}, []
    validos = [t for t in candidatos if salida(barras, t, tenencia, stop)]
    for _ in range(sorteos):
        elegidos = []
        for t in rng.sample(validos, len(validos)):
            if all(abs((t - e).days) >= separacion for e in elegidos):
                elegidos.append(t)
                if len(elegidos) == n:
                    break
        if len(elegidos) < n:
            raise ValueError("Placebo imposible: no caben tantas operaciones separadas")
        for t in elegidos:
            if t not in cache:
                cache[t] = retorno_neto(salida(barras, t, tenencia, stop), coste_pct)
        medias.append(st.mean(cache[t] for t in elegidos))
    return medias
