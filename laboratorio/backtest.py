"""Backtest común: opera las ventanas completas de las observaciones y valora la cuenta por día.

Una operación es una racha de periodos consecutivos en la ventana (cada uno empieza donde acaba el
anterior) con tantos periodos como valores tiene la ventana (con `longitud` None, de cualquier longitud: p. ej. un
semestre, cerrado al final de la muestra si la ventana sigue abierta). Entra al cierre anterior al primero y sale
al cierre del último. Tamaño: 1 unidad del precio negociado o, con `fraccion`, esa fracción de la equity
al cierre de entrada (unidades fraccionarias); crece con `close` (retorno total si `close` está ajustado).
Coste: `coste_lado` por unidad y lado.
"""
from collections import defaultdict

from .contratos import Operacion, Sesion


def rachas(obs, longitud):
    actual, out = [], []
    for o in obs:
        if o.en_ventana and (not actual or actual[-1].periodo.fin == o.periodo.inicio):
            actual.append(o)
            continue
        if actual and (longitud is None or len(actual) == longitud):
            out.append(actual)
        actual = [o] if o.en_ventana else []
    if actual and (longitud is None or len(actual) == longitud):
        out.append(actual)
    return out


def backtest(obs, longitud, capital, coste_lado, fraccion=None):
    """Sin `fraccion`, 1 unidad por operación. Con `fraccion` (0-1], unidades = fraccion · equity / precio de entrada."""
    if fraccion is not None and not 0 < fraccion <= 1:
        raise ValueError("fraccion debe estar en (0, 1]; no se permite apalancamiento")
    bruto, coste, nocional, compra = (defaultdict(float) for _ in range(4))
    en_posicion, total = defaultdict(int), defaultdict(int)
    for o in obs:
        total[o.periodo.fin.ts.date()] += 1
    operaciones = []
    for racha in rachas(obs, longitud):
        entrada, salida = racha[0].periodo.inicio, racha[-1].periodo.fin
        dia_entrada = entrada.ts.date()
        if fraccion is None:
            acciones = 1
        else:  # equity al cierre de entrada con lo ya operado (las rachas llegan en orden de entrada)
            equity = capital + sum(bruto[d] - coste[d] for d in total if d <= dia_entrada)
            acciones = fraccion * equity / entrada.precio
        unidades = acciones * entrada.precio / entrada.close
        for o in racha:
            dia = o.periodo.fin.ts.date()
            bruto[dia] += unidades * (o.periodo.fin.close - o.periodo.inicio.close)
            en_posicion[dia] += 1
        valor = unidades * salida.close
        c_entrada = coste_lado * acciones
        c_salida = coste_lado * valor / salida.precio
        pnl = valor - acciones * entrada.precio
        operaciones.append(Operacion(id=f"T{len(operaciones) + 1:04d}", entrada=dia_entrada, salida=salida.ts.date(),
                                     pnl_bruto=pnl, coste_entrada=c_entrada, coste_salida=c_salida,
                                     pnl_neto=pnl - c_entrada - c_salida))
        coste[dia_entrada] += c_entrada
        coste[salida.ts.date()] += c_salida
        nocional[dia_entrada] += acciones * entrada.precio
        compra[dia_entrada] = max(compra[dia_entrada], acciones * entrada.precio + c_entrada)
        nocional[salida.ts.date()] += valor
    sesiones, equity = [], capital
    for dia in sorted(total):
        if compra[dia] > equity:
            raise ValueError("Capital insuficiente; no se permite apalancamiento")
        equity += bruto[dia] - coste[dia]
        sesiones.append(Sesion(fecha=dia, equity=equity, pnl_bruto=bruto[dia], coste=coste[dia],
                               nocional=nocional[dia], exposicion=en_posicion[dia] / total[dia]))
    return sesiones, operaciones
