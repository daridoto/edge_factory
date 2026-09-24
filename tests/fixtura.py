"""Datos sintéticos para tests: contabilidad y formato, nunca evidencia."""
from datetime import date, datetime, timedelta
import random

from laboratorio import ejecutar
from laboratorio.contratos import Operacion, Sesion
from laboratorio.datos import Barra

PLAN_H001 = "experimentos/H001-IS-REAL-001.md"


def precios_2018(semilla=7301):
    rng = random.Random(semilla)
    barras, precio, dia = [], 100.0, date(2018, 1, 1)
    while dia.year == 2018:
        if dia.weekday() < 5:
            precio = round(precio + rng.uniform(-1.5, 1.5), 4)
            barras.append(Barra(datetime(dia.year, dia.month, dia.day, 16), precio, precio))
        dia += timedelta(days=1)
    return barras


def experimento():
    """(Resumen, sesiones, operaciones) sintéticos con la especificación de H-001."""
    spec = ejecutar.leer_plan(ejecutar.motor.RAIZ / PLAN_H001)
    return ejecutar.ejecutar(spec, PLAN_H001, barras=precios_2018(), hoy=date(2026, 9, 24),
                             inicio=date(2018, 1, 1), fin=date(2018, 12, 31))


def muestra_pequena():
    """Dos operaciones: +10 bruto -2 costes = +8; -4 bruto -2 = -6."""
    operaciones = [Operacion(id="a", entrada="2019-01-01", salida="2019-01-02", pnl_bruto=10, coste_entrada=1, coste_salida=1, pnl_neto=8),
                   Operacion(id="b", entrada="2019-01-03", salida="2019-01-04", pnl_bruto=-4, coste_entrada=1, coste_salida=1, pnl_neto=-6)]
    sesiones = [Sesion(fecha=f"2019-01-0{i+1}", equity=e, pnl_bruto=p, coste=1, nocional=20, exposicion=x)
                for i, (e, p, x) in enumerate([(99, 0, 0), (108, 10, 1), (107, 0, 0), (102, -4, 1)])]
    return sesiones, operaciones
