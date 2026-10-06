"""Carga de datasets y construcción de periodos de retorno. Filtra IS por fecha antes de leer precios.

Un periodo es el retorno entre dos cierres consecutivos en la frecuencia de la hipótesis:
- "1d": sesión a sesión (SPY diario).
- "1h": hora de reloj h = close(h:45) / close((h-1):45) - 1 (ES 15 min). La hora 18 parte de 16:45,
  el último precio antes de la pausa; el domingo 18 se salta (fin de semana y roll, C6).

Cada dataset declara su `mercado` (qué IS aplica, ver proteccion.MUESTRAS). Las series (SERIES) son
valores diarios auxiliares (volumen de un DEX, precio de referencia) que usan las señales.
"""
from collections import namedtuple
import csv
from datetime import date, datetime, time, timedelta
import math
from pathlib import Path

from .proteccion import MUESTRAS, exigir_muestra

RAIZ = Path(__file__).resolve().parent.parent

# close: precio para retornos (ajustado si existe). precio: precio negociado, para costes y nocional.
# open, high y low solo se cargan si el dataset los declara (operativas con entrada en apertura o stop).
Barra = namedtuple("Barra", "ts close precio open high low", defaults=(None, None, None))
Periodo = namedtuple("Periodo", "inicio fin")  # dos Barra: cierre anterior y cierre del periodo


def _norgate_etf(nombre, instrumento):
    """ETF diario de Norgate: Close ajustado por dividendos para retornos, Unadjusted Close para costes."""
    return dict(ruta=f"data/etf/indices/{nombre} - Temp. 1d - Date 2006-07-17 a 2026-07-15 - Norgate.csv",
                ts="Date", close="Close", precio="Unadjusted Close", instrumento=instrumento, frecuencia="1d",
                mercado="clasica")


DATASETS = {
    "SPY 1d": _norgate_etf("SP500 SPY", "SPY"),
    "QQQ 1d": _norgate_etf("Nasdaq 100 QQQ", "QQQ"),
    "IWM 1d": _norgate_etf("Russell 2000 IWM", "IWM"),
    "DIA 1d": _norgate_etf("Dow Jones DIA", "DIA"),
    "ES 15min": dict(ruta="data/indices/ES_15min_2009-2026.csv",
                     ts="ts", close="close", precio="close", instrumento="ES", frecuencia="15min", mercado="clasica"),
    # Mismas horas que el ES; `close` sin ajustar por roll (las ventanas intradía no cruzan el domingo 18:00).
    "NQ 15min": dict(ruta="data/indices/nq/nq_15m_ohlcv.csv",
                     ts="ts", close="close", precio="close", instrumento="NQ", frecuencia="15min", mercado="clasica"),
    # Binance spot, velas diarias UTC; sin dividendos, así que close = precio negociado.
    "RAY 1d": dict(ruta="data/cripto/RAY_diario.csv", ts="fecha", close="binance_close", precio="binance_close",
                   open="binance_open", high="binance_high", low="binance_low",
                   instrumento="RAY", frecuencia="1d", mercado="cripto", periodos_por_anio=365),
}

# Serie diaria: fecha -> valor. Las celdas vacías son días sin dato (no se interpolan).
SERIES = {
    "Raydium volumen 1d": dict(ruta="data/cripto/defillama_volumen_diario.csv", ts="fecha", valor="RAY_volumen_usd",
                               mercado="cripto"),
    "BTC 1d": dict(ruta="data/cripto/RAY_diario.csv", ts="fecha", valor="btc_close", mercado="cripto"),
    # Cierre diario del VIX (16:15 ET); fichero mixto: se filtra IS por fecha antes de leer el valor.
    "VIX 1d": dict(ruta="data/macro/Indice de volatilidad VIX - Temp. 1d - Date 2006-07-17 a 2026-07-15 - Norgate.csv",
                   ts="Date", valor="Close", mercado="clasica"),
}


def _limites(d, inicio, fin, hipotesis, muestra="IS", base=None):
    """Límites de lectura: por defecto, toda la IS del mercado del dataset; siempre dentro de la muestra autorizada."""
    mercado = d.get("mercado", "clasica")
    inicio, fin = inicio or MUESTRAS[mercado][0], fin or MUESTRAS[mercado][1]
    exigir_muestra(inicio, fin, muestra, mercado, hipotesis, base)
    return str(inicio), str(fin)


def cargar(nombre, inicio=None, fin=None, ruta=None, hipotesis=None, muestra="IS", base=None):
    """Barras de la muestra, ordenadas. Fuera de ella solo se lee la fecha para descartar la fila."""
    d = DATASETS[nombre]
    inicio, fin = _limites(d, inicio, fin, hipotesis, muestra, base)
    barras = []
    with Path(ruta or RAIZ / d["ruta"]).open(newline="", encoding="utf-8-sig") as f:
        lector = csv.DictReader(f)
        if not {d["ts"], d["close"], d["precio"]} <= set(lector.fieldnames or []):
            raise ValueError(f"Faltan columnas en {nombre}")
        for fila in lector:
            texto = fila[d["ts"]]
            if not inicio <= texto[:10] <= fin:
                continue
            ts = datetime.fromisoformat(texto) if len(texto) > 10 else datetime.combine(date.fromisoformat(texto), time(16))
            precios = [float(fila[d[k]]) for k in ("close", "precio", "open", "high", "low") if k in d]
            if not all(math.isfinite(x) and x > 0 for x in precios):
                raise ValueError(f"Precio inválido dentro de IS: {texto}")
            barras.append(Barra(ts, *precios))
    ts = [b.ts for b in barras]
    if not barras or ts != sorted(set(ts)):
        raise ValueError("IS vacío, desordenado o duplicado")
    return barras


def cargar_serie(nombre, inicio=None, fin=None, ruta=None, hipotesis=None, muestra="IS", base=None):
    """{fecha: valor} de una serie auxiliar dentro de la muestra; filtra por fecha antes de leer el valor."""
    d = SERIES[nombre]
    inicio, fin = _limites(d, inicio, fin, hipotesis, muestra, base)
    serie = {}
    with Path(ruta or RAIZ / d["ruta"]).open(newline="", encoding="utf-8-sig") as f:
        lector = csv.DictReader(f)
        if not {d["ts"], d["valor"]} <= set(lector.fieldnames or []):
            raise ValueError(f"Faltan columnas en {nombre}")
        for fila in lector:
            texto = fila[d["ts"]][:10]
            if not inicio <= texto <= fin or fila[d["valor"]] == "":
                continue
            valor = float(fila[d["valor"]])
            if not math.isfinite(valor) or valor < 0 or date.fromisoformat(texto) in serie:
                raise ValueError(f"Valor inválido o duplicado dentro de IS: {nombre} {texto}")
            serie[date.fromisoformat(texto)] = valor
    return dict(sorted(serie.items()))


def periodos(barras, frecuencia, excluir_horas=()):
    if frecuencia == "1d":
        return [Periodo(a, b) for a, b in zip(barras, barras[1:])]
    if frecuencia == "1h":
        cierres = {b.ts: b for b in barras if b.ts.minute == 45}
        out = []
        for ts, fin in cierres.items():
            if ts.hour in excluir_horas:
                continue
            if ts.hour == 18:
                if ts.weekday() == 6:
                    continue
                previo = ts.replace(hour=16)
            else:
                previo = ts - timedelta(hours=1)
            if previo in cierres:
                out.append(Periodo(cierres[previo], fin))
        return out
    raise ValueError(f"Frecuencia de periodo desconocida: {frecuencia}")
