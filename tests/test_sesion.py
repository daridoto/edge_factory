"""Operativa por sesión: filtro por señal, tamaño por serie, partición de la evidencia, sensibilidad y salida completa."""
from datetime import date, datetime, timedelta
import random
import tempfile
import unittest
from pathlib import Path

from laboratorio import catalogo, ejecutar, motor, sesion
from laboratorio.contratos import Variante
from laboratorio.presentacion import render
from tests.test_variantes import barras_es

PLAN_003, PLAN_004 = "experimentos/H-007-deriva-nocturna-es/H007-IS-REAL-003-odplus-btd.md", "experimentos/H-007-deriva-nocturna-es/H007-IS-REAL-004-odplus-btd-vix.md"


def fila(dia, entrada, salida, senal=None, serie=None):
    d = date.fromisoformat(dia)
    return Variante(fecha=d, previa=d - timedelta(1), ventana="W", entrada=entrada, salida=salida, senal=senal,
                    serie=serie, desfase=False)


FILAS = [fila("2018-01-02", 100, 102, senal=-.01, serie=25),   # opera ×2 (serie > 20)
         fila("2018-01-03", 100, 99, senal=.01, serie=25),     # filtro: no opera
         fila("2018-01-04", 100, 101, senal=-.02, serie=15),   # opera ×1
         fila("2018-01-05", 100, 103, senal=None, serie=30)]   # sin señal: no opera
FECHAS = [date(2018, 1, d) for d in range(1, 7)]


class Simular(unittest.TestCase):
    def test_filtro_tamano_y_costes(self):
        sesiones, ops = sesion.simular(FILAS, FECHAS, ["01:30", "03:30"], 1000, .5, "negativa",
                                       {"umbral": 20, "multiplicador": 2})
        self.assertEqual([(o.entrada.day, o.pnl_bruto, o.coste_entrada, o.pnl_neto) for o in ops],
                         [(2, 4.0, 1.0, 2.0), (4, 1.0, .5, 0.0)])
        self.assertEqual([s.equity for s in sesiones], [1000, 1002, 1002, 1002, 1002, 1002])
        self.assertAlmostEqual(sesiones[1].exposicion, 2 / 23)
        motor.validar_contabilidad(1000, FECHAS[0], FECHAS[-1], sesiones, ops)

    def test_fraccion_reinvierte_y_sin_filtro_opera_todas(self):
        sesiones, ops = sesion.simular(FILAS, FECHAS, ["02:00", "03:00"], 1000, 0, fraccion=1)
        self.assertEqual(len(ops), 4)
        self.assertAlmostEqual(sesiones[-1].equity, 1000 * 1.02 * .99 * 1.01 * 1.03)

    def test_una_fila_por_sesion(self):
        with self.assertRaises(ValueError):
            sesion.simular(FILAS + FILAS[:1], FECHAS, ["02:00", "03:00"], 1000, 0)


class Grupos(unittest.TestCase):
    def test_particion_filtro(self):
        g = sesion.grupos(FILAS, "filtro", "negativa")
        self.assertAlmostEqual(catalogo.media_ventana(list(g.values())), (.02 + .01) / 2 * catalogo.PB)
        self.assertAlmostEqual(catalogo.media_vs_resto(list(g.values())), ((.02 + .01) / 2 - (-.01 + .03) / 2) * catalogo.PB)

    def test_particion_tamano_solo_operadas_con_dato(self):
        g = sesion.grupos(FILAS + [fila("2018-01-08", 100, 90, senal=-.01)], "tamano", "negativa", {"umbral": 20})
        self.assertEqual(list(g), ["2018-01-02", "2018-01-04"])
        self.assertEqual([[round(x, 12) for x in v] for v in g.values()], [[1, .02, 0, 0], [0, 0, 1, .01]])


class Tendencia(unittest.TestCase):
    def test_precio_frente_a_su_media(self):
        from laboratorio.datos import Barra
        bs = [Barra(datetime(2018, 1, d, 16), c, c) for d, c in [(2, 10), (3, 20), (4, 30), (5, 60)]]   # barras de 16:00 = precio 16:15
        t = sesion.tendencia(bs, "15min", "16:15", 3)
        self.assertEqual(list(t), [date(2018, 1, 4), date(2018, 1, 5)])
        self.assertAlmostEqual(t[date(2018, 1, 4)], 30 / 20 - 1)
        self.assertAlmostEqual(t[date(2018, 1, 5)], 60 / (110 / 3) - 1)

    def test_filtro_por_rango_de_serie(self):
        f = {"senal": None, "serie_max": 20}
        self.assertEqual([sesion.opera(x, f) for x in FILAS], [False, False, True, False])     # serie 25, 25, 15, 30
        self.assertFalse(sesion.opera(fila("2018-01-08", 100, 101, senal=-.01), f))         # sin dato: no opera
        g = sesion.grupos(FILAS + [fila("2018-01-08", 100, 101)], "filtro", f)
        self.assertNotIn("2018-01-08", g)                                                  # sin dato: fuera de la evidencia

    def test_particion_serie_y_control(self):
        g = sesion.grupos(FILAS, "serie", "negativa", {"umbral": 20})
        self.assertEqual(sorted(g), ["2018-01-02", "2018-01-04"])           # operadas con dato
        c = sesion.grupos(FILAS, "serie", "negativa", {"umbral": 20}, lado_filtro="descartadas")
        self.assertEqual(list(c), ["2018-01-03"])                           # descartada con señal; la de señal vacía, fuera


def vix(barras, semilla=3):
    rng = random.Random(semilla)
    return {d: rng.uniform(10, 30) for d in sorted({b.ts.date() for b in barras})}


class Ejecutor(unittest.TestCase):
    def correr(self, plan, **extra):
        spec = ejecutar.leer_plan(motor.RAIZ / plan)
        bs = barras_es()
        return ejecutar.ejecutar(spec, plan, barras=bs, serie=vix(bs), hoy=date(2026, 10, 6), **extra)

    def test_nucleo_guarda_y_carga(self):
        resumen, sesiones, ops, al_100, filas = self.correr(PLAN_003)
        self.assertIsNone(filas)
        self.assertIsNone(resumen.sensibilidad)
        self.assertTrue(resumen.experimento.sintetico)
        self.assertEqual(resumen.metricas.operaciones, len(ops))
        with tempfile.TemporaryDirectory() as tmp:
            motor.guardar(Path(tmp) / "x", resumen, sesiones, ops, al_100)
            self.assertEqual(motor.cargar(Path(tmp) / "x")[0], resumen)

    def test_tamano_y_sensibilidad(self):
        resumen, _, ops, al_100, _ = self.correr(PLAN_004)
        filas = resumen.sensibilidad
        self.assertEqual([(f.umbral, f.multiplicador) for f in filas],
                         [(u, k) for u in (15, 20, 25, 30) for k in (1.5, 2, 3)])
        # la diferencia no depende del multiplicador y la de 20 es la evidencia
        self.assertEqual(len({(f.umbral, f.diferencia) for f in filas}), 4)
        self.assertAlmostEqual(next(f.diferencia for f in filas if f.umbral == 20), resumen.evidencia.valor)
        # la fila de 20 y ×2 es la referencia al 100 %
        f = next(f for f in filas if (f.umbral, f.multiplicador) == (20, 2))
        self.assertAlmostEqual(f.rentabilidad_total, resumen.referencia.rentabilidad_total)
        self.assertTrue(any(o.coste_entrada == 2 * .125 for o in ops))   # alguna noche ×2 (1 unidad × 2)
        self.assertIn("Sensibilidad", render(resumen))

    def test_sin_filtro_no_hay_resto(self):
        resumen, _, ops, _, _ = self.correr("experimentos/H-007-deriva-nocturna-es/H007-IS-REAL-005-odplus.md")
        c = [x.valor for x in resumen.evidencia.componentes]
        self.assertEqual(c[:2], [len(ops), 0])
        self.assertAlmostEqual(c[2], resumen.evidencia.valor)
        self.assertNotIn("Diferencia", " ".join(x.nombre for x in resumen.evidencia.componentes))

    def test_control_por_tendencia(self):
        plan = "experimentos/H-007-deriva-nocturna-nq/H007-IS-REAL-007-nq-btd-tendencia.md"
        spec = ejecutar.leer_plan(motor.RAIZ / plan)
        bs = barras_es(inicio=datetime(2017, 1, 1, 18), fin=datetime(2018, 12, 29), semilla=4)
        resumen, sesiones, ops, al_100, _ = ejecutar.ejecutar(spec, plan, barras=bs, hoy=date(2026, 10, 6))
        c = resumen.control
        self.assertEqual(c.lados, ["alcista", "bajista"])
        self.assertAlmostEqual(c.medias.operadas[0] - c.medias.operadas[1], resumen.evidencia.valor)
        self.assertAlmostEqual(c.medias.descartadas[0] - c.medias.descartadas[1], c.diferencia_descartadas)
        self.assertLessEqual(c.ic_inf, c.ic_sup)
        self.assertTrue(set(c.sin_cada_anio) <= {"2017", "2018"})
        self.assertIn("Control", render(resumen))
        with tempfile.TemporaryDirectory() as tmp:
            motor.guardar(Path(tmp) / "H-007-x" / "H007-IS-REAL-007-y", resumen, sesiones, ops, al_100)

    def test_tamano_sin_serie_falla(self):
        spec = ejecutar.leer_plan(motor.RAIZ / PLAN_004)
        del spec["datos"]["serie"]
        with self.assertRaises(ValueError):
            ejecutar.ejecutar(spec, PLAN_004, barras=barras_es(), hoy=date(2026, 10, 6))


class MuestraOOS(unittest.TestCase):
    def test_solo_el_experimento_autorizado_y_dentro_de_la_oos(self):
        from laboratorio.proteccion import exigir_muestra
        exigir_muestra("2021-01-01", "2026-05-28", "OOS", "clasica", "H-007", "H007-IS-REAL-003")
        exigir_muestra("2009-09-27", "2026-05-28", "Total", "clasica", "H-007", "H007-IS-REAL-003")
        for args in [("2021-01-01", "2026-05-28", "OOS", "clasica", "H-007", "H007-IS-REAL-002"),   # no autorizado
                     ("2020-12-30", "2021-06-01", "OOS", "clasica", "H-007", "H007-IS-REAL-003"),   # empieza en IS
                     ("2021-01-01", "2026-06-30", "OOS", "clasica", "H-007", "H007-IS-REAL-003"),   # pasa del último dato
                     ("2009-09-27", "2026-05-28", "Total", "clasica", "H-007", "H007-IS-REAL-002"),  # Total sin autorizar
                     ("2021-01-01", "2021-06-01", "IS", "clasica", "H-007", None)]:                 # IS con fechas OOS
            with self.subTest(args), self.assertRaises(ValueError):
                exigir_muestra(*args)

    def test_plan_oos_identico_a_su_base(self):
        spec = ejecutar.leer_plan(motor.RAIZ / "experimentos/H-007-deriva-nocturna-es/H007-OOS-REAL-001-odplus-btd.md")
        ejecutar.exigir_mismo_plan(spec)
        spec["sesion"] = {**spec["sesion"], "ventana": ["02:00", "03:00"]}
        with self.assertRaises(ValueError):
            ejecutar.exigir_mismo_plan(spec)

    def test_oos_sintetico_lleva_base_y_valida(self):
        spec = ejecutar.leer_plan(motor.RAIZ / "experimentos/H-007-deriva-nocturna-es/H007-OOS-REAL-001-odplus-btd.md")
        bs = barras_es(inicio=datetime(2022, 1, 9, 18), fin=datetime(2022, 3, 5))
        resumen, sesiones, ops, al_100, _ = ejecutar.ejecutar(spec, "experimentos/H-007-deriva-nocturna-es/H007-OOS-REAL-001-odplus-btd.md", barras=bs,
                                                               hoy=date(2026, 10, 6))
        self.assertEqual((resumen.experimento.muestra, resumen.experimento.base), ("OOS", "H007-IS-REAL-003"))
        with tempfile.TemporaryDirectory() as tmp:
            motor.guardar(Path(tmp) / "x", resumen, sesiones, ops, al_100)
            self.assertEqual(motor.cargar(Path(tmp) / "x")[0], resumen)


if __name__ == "__main__":
    unittest.main()
