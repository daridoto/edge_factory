"""Operativa por eventos y muestras por mercado (datos sintéticos)."""
from datetime import date, datetime, timedelta
import unittest

from laboratorio import ejecutar
from laboratorio.datos import Barra, cargar, cargar_serie
from laboratorio.eventos import aplicar_enfriamiento, placebo, ratio_medianas, retorno_neto, salida, simular
from laboratorio.motor import validar_contabilidad
from laboratorio.proteccion import exigir_is

D0 = date(2023, 1, 1)


def velas(ohlc):
    """Una vela diaria por (open, high, low, close) desde D0."""
    return [Barra(datetime.combine(D0 + timedelta(i), datetime.min.time()), c, c, o, h, l)
            for i, (o, h, l, c) in enumerate(ohlc)]


class Proteccion(unittest.TestCase):
    def test_cripto_solo_para_la_hipotesis_autorizada(self):
        exigir_is("2022-01-01", "2026-09-29", "cripto", "H-PROPIA-001")
        for inicio, fin, h in [("2022-01-01", "2026-09-30", "H-PROPIA-001"), ("2021-08-09", "2022-01-01", "H-PROPIA-001"),
                               ("2022-01-01", "2023-01-01", "H-001"), ("2022-01-01", "2023-01-01", None)]:
            with self.subTest(fin=fin, h=h), self.assertRaisesRegex(ValueError, "BLOQUEADO"):
                exigir_is(inicio, fin, "cripto", h)

    def test_datos_cripto_sin_autorizacion_no_se_abren(self):
        with self.assertRaisesRegex(ValueError, "BLOQUEADO"):
            cargar("RAY 1d", ruta="nunca_abierto")
        with self.assertRaisesRegex(ValueError, "BLOQUEADO"):
            cargar_serie("Raydium volumen 1d", ruta="nunca_abierto", hipotesis="H-007")


class Senal(unittest.TestCase):
    def test_ratio_cuenta_dias_con_dato(self):
        serie = {D0 + timedelta(i): 1.0 for i in range(10)}
        del serie[D0 + timedelta(3)]  # hueco: la ventana larga de 5 datos necesita llegar al día 5
        serie.update({D0 + timedelta(i): 5.0 for i in (8, 9)})
        self.assertEqual(ratio_medianas(serie, 3, 5, 2), [D0 + timedelta(9)])
        self.assertEqual(ratio_medianas(serie, 1, 5, 2), [D0 + timedelta(8), D0 + timedelta(9)])

    def test_enfriamiento_acepta_el_dia_t_mas_n(self):
        dias = [D0 + timedelta(i) for i in (0, 5, 10, 11, 25)]
        self.assertEqual(aplicar_enfriamiento(dias, 10), [D0, D0 + timedelta(10), D0 + timedelta(25)])


class Operacion(unittest.TestCase):
    def test_salidas_por_tiempo_stop_y_gap(self):
        planas = [(100, 101, 99, 100)] * 10
        tiempo = salida(velas(planas), D0, 3, .25)
        self.assertEqual((tiempo.i_entrada, tiempo.i_salida, tiempo.motivo), (1, 3, "tiempo"))
        stop = salida(velas(planas[:2] + [(100, 100, 70, 90)] + planas[3:]), D0, 5, .25)
        self.assertEqual((stop.i_salida, stop.salida, stop.motivo), (2, 75, "stop"))
        gap = salida(velas(planas[:2] + [(60, 65, 55, 62)] + planas[3:]), D0, 5, .25)
        self.assertEqual((gap.salida, gap.motivo), (60, "stop en apertura"))
        self.assertIsNone(salida(velas(planas), D0 + timedelta(7), 3, .25))  # t + 3 fuera de la muestra

    def test_contabilidad_concilia_y_reinvierte(self):
        bs = velas([(100, 100, 100, 100), (100, 110, 100, 110), (110, 125, 110, 120), (120, 120, 120, 120),
                    (120, 120, 120, 120), (80, 80, 80, 80), (80, 80, 80, 80)])
        sesiones, ops, detalle = simular(bs, [D0, D0 + timedelta(3)], 2, .25, 1000, .01)
        self.assertEqual([o.entrada.day for o in ops], [2, 5])
        self.assertAlmostEqual(detalle[0][2], 120 * .99 / (100 * 1.01) - 1)
        self.assertAlmostEqual(sesiones[2].equity, 1000 * (1 + detalle[0][2]))
        self.assertEqual(detalle[1][1].motivo, "stop en apertura")  # abre a 120, el día 6 abre a 80 < 90
        self.assertAlmostEqual(sesiones[-1].equity, 1000 * (1 + detalle[0][2]) * (1 + detalle[1][2]))
        validar_contabilidad(1000, "2023-01-01", "2023-01-07", sesiones, ops, "cripto", "H-PROPIA-001")
        self.assertEqual([s.exposicion for s in sesiones], [0, 1, 1, 0, 1, 1, 0])

    def test_placebo_reproducible(self):
        bs = velas([(100 + i, 101 + i, 99 + i, 100 + i) for i in range(60)])
        dias = [b.ts.date() for b in bs]
        a = placebo(bs, dias, 3, 5, .25, .002, 10, sorteos=50)
        self.assertEqual(a, placebo(bs, dias, 3, 5, .25, .002, 10, sorteos=50))
        self.assertTrue(all(x > 0 for x in a))


class PlanRay(unittest.TestCase):
    def test_especificacion_corre_con_datos_sinteticos(self):
        plan = "experimentos/HPROPIA001-IS-REAL-001.md"
        spec = ejecutar.leer_plan(ejecutar.motor.RAIZ / plan)
        n = 400
        precios = [(10 + i * .01,) * 4 for i in range(n)]
        bs = [Barra(datetime(2022, 8, 15) + timedelta(i), p[3], p[3], p[0], p[1] * 1.01, p[2] * .99) for i, p in enumerate(precios)]
        serie = {date(2022, 8, 15) + timedelta(i): (5.0 if i % 60 < 5 and i > 100 else 1.0) for i in range(n)}
        btc = {k: 100.0 for k in serie}
        r, sesiones, ops, _ = ejecutar.ejecutar(spec, plan, barras=bs, serie=serie, referencia=btc, hoy=date(2026, 9, 30))
        self.assertTrue(r.experimento.sintetico)
        self.assertEqual(r.experimento.mercado, "cripto")
        self.assertEqual(r.procedencia.periodos_por_anio, 365)
        self.assertEqual(r.evidencia.componentes[0].valor, len(ops))
        validar_contabilidad(10000, r.experimento.inicio, r.experimento.fin, sesiones, ops, "cripto", "H-PROPIA-001")


if __name__ == "__main__":
    unittest.main()
