"""Operativa por sesión: una ventana intradía por sesión lun-vie, con filtro por la señal de la sesión previa y
tamaño según una serie diaria de la sesión previa. Sale de la tabla de variantes.py (mismos precios y covariables).

- Entra al precio de la hora de entrada y sale al de la hora de salida del mismo día (sin posición entre sesiones).
- Filtro (`filtro_senal`): "negativa" opera si señal < 0; "positiva", si > 0; sin filtro, todas. Señal vacía: no opera.
- Tamaño: unidades = fraccion · w · equity previa / entrada (o w unidades sin fraccion), con w = multiplicador si la
  serie de la sesión previa supera el umbral y 1 si no (o si falta el dato). w > 1 es apalancamiento declarado.
- Coste: `coste_lado` por unidad y lado. Exposición: horas de la ventana / 23 (sesión de Globex).
- Calendario de la equity: todas las fechas con barras.

Evidencia sobre el retorno bruto de precio de cada sesión (salida / entrada - 1), en grupos por día
[n ventana, suma ventana, n resto, suma resto] como el resto del catálogo:
- particion "filtro": ventana = sesiones operadas; resto = las que el filtro descarta.
- particion "tamano": ventana = operadas con serie > umbral; resto = operadas con serie <= umbral (sin dato: fuera).
"""
from collections import defaultdict

from .contratos import Operacion, Sesion

HORAS_SESION = 23


def horas(ventana):
    a, b = (int(h[:2]) + int(h[3:]) / 60 for h in ventana)
    if not 0 < b - a <= HORAS_SESION:
        raise ValueError(f"Ventana inválida: {ventana}")
    return b - a


def opera(fila, filtro):
    if filtro is None:
        return True
    if fila.senal is None:
        return False
    return {"negativa": fila.senal < 0, "positiva": fila.senal > 0}[filtro]


def peso(fila, tamano):
    if not tamano or fila.serie is None or fila.serie <= tamano["umbral"]:
        return 1.0
    return float(tamano["multiplicador"])


def simular(filas, fechas, ventana, capital, coste_lado, filtro=None, tamano=None, fraccion=None):
    """(sesiones, operaciones). `filas`: Variante de una sola ventana; `fechas`: calendario de la equity."""
    if fraccion is not None and not 0 < fraccion <= 1:
        raise ValueError("fraccion debe estar en (0, 1]")
    if tamano and not tamano["multiplicador"] > 0:
        raise ValueError("El multiplicador de tamaño debe ser > 0")
    exposicion = horas(ventana) / HORAS_SESION
    por_fecha = {f.fecha: f for f in filas}
    if len(por_fecha) != len(filas):
        raise ValueError("Más de una fila por sesión: filtra una sola ventana")
    sesiones, operaciones, equity = [], [], capital
    for dia in fechas:
        f = por_fecha.get(dia)
        if f is None or not opera(f, filtro):
            sesiones.append(Sesion(fecha=dia, equity=equity, pnl_bruto=0, coste=0, nocional=0, exposicion=0))
            continue
        w = peso(f, tamano)
        unidades = w * (1 if fraccion is None else fraccion * equity / f.entrada)
        bruto = unidades * (f.salida - f.entrada)
        c = coste_lado * unidades
        operaciones.append(Operacion(id=f"T{len(operaciones) + 1:04d}", entrada=dia, salida=dia, pnl_bruto=bruto,
                                     coste_entrada=c, coste_salida=c, pnl_neto=bruto - 2 * c))
        equity += bruto - 2 * c
        sesiones.append(Sesion(fecha=dia, equity=equity, pnl_bruto=bruto, coste=2 * c,
                               nocional=unidades * (f.entrada + f.salida), exposicion=exposicion))
    return sesiones, operaciones


def grupos(filas, particion, filtro=None, tamano=None):
    """{fecha ISO: [n ventana, suma ventana, n resto, suma resto]} en orden cronológico."""
    g = defaultdict(lambda: [0, 0.0, 0, 0.0])
    for f in sorted(filas, key=lambda f: f.fecha):
        r = f.salida / f.entrada - 1
        if particion == "filtro":
            lado = 0 if opera(f, filtro) else 2
        elif particion == "tamano":
            if not opera(f, filtro) or f.serie is None:
                continue
            lado = 0 if f.serie > tamano["umbral"] else 2
        else:
            raise ValueError(f"Partición desconocida: {particion}")
        acc = g[f.fecha.isoformat()]
        acc[lado] += 1
        acc[lado + 1] += r
    return dict(g)
