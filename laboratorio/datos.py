"""Carga de datasets y construcción de periodos de retorno. Filtra IS por fecha antes de leer precios.

Un periodo es el retorno entre dos cierres consecutivos en la frecuencia de la hipótesis:
- "1d": sesión a sesión (SPY diario).
- "1h": hora de reloj h = close(h:45) / close((h-1):45) - 1 (ES 15 min). La hora 18 parte de 16:45,
  el último precio antes de la pausa; el domingo 18 se salta (fin de semana y roll, C6).
"""
from collections import namedtuple
import csv
from datetime import date, datetime, time, timedelta
import math
from pathlib import Path

from .proteccion import FIN_IS, INICIO_IS, exigir_is

RAIZ = Path(__file__).resolve().parent.parent

# close: precio para retornos (ajustado si existe). precio: precio negociado, para costes y nocional.
Barra = namedtuple("Barra", "ts close precio")
Periodo = namedtuple("Periodo", "inicio fin")  # dos Barra: cierre anterior y cierre del periodo


def _norgate_etf(nombre, instrumento):
    """ETF diario de Norgate: Close ajustado por dividendos para retornos, Unadjusted Close para costes."""
    return dict(ruta=f"data/etf/indices/{nombre} - Temp. 1d - Date 2006-07-17 a 2026-07-15 - Norgate.csv",
                ts="Date", close="Close", precio="Unadjusted Close", instrumento=instrumento, frecuencia="1d")


DATASETS = {
    "SPY 1d": _norgate_etf("SP500 SPY", "SPY"),
    "QQQ 1d": _norgate_etf("Nasdaq 100 QQQ", "QQQ"),
    "IWM 1d": _norgate_etf("Russell 2000 IWM", "IWM"),
    "DIA 1d": _norgate_etf("Dow Jones DIA", "DIA"),
    "ES 15min": dict(ruta="data/indices/ES_15min_2009-2026.csv",
                     ts="ts", close="close", precio="close", instrumento="ES", frecuencia="15min"),
}


def cargar(nombre, inicio=INICIO_IS, fin=FIN_IS, ruta=None):
    """Barras IS del dataset, ordenadas. Fuera de IS solo se lee la fecha para descartar la fila."""
    exigir_is(inicio, fin)
    d = DATASETS[nombre]
    inicio, fin = str(inicio), str(fin)
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
            close, precio = float(fila[d["close"]]), float(fila[d["precio"]])
            if not all(math.isfinite(x) and x > 0 for x in (close, precio)):
                raise ValueError(f"Precio inválido dentro de IS: {texto}")
            barras.append(Barra(ts, close, precio))
    ts = [b.ts for b in barras]
    if not barras or ts != sorted(set(ts)):
        raise ValueError("IS vacío, desordenado o duplicado")
    return barras


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
