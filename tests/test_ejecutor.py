"""Piezas del ejecutor único: datos, catálogo, backtest y robustez."""
import csv
from datetime import date, datetime
from pathlib import Path
import tempfile
import unittest

from laboratorio.backtest import backtest
from laboratorio.catalogo import dias_de_mes, grupos, hora, media_vs_resto
from laboratorio.datos import DATASETS, Barra, Periodo, cargar, periodos
from laboratorio.robustez import bootstrap, por_anio, sin_cada_anio


ETF_DIARIOS = ["SPY 1d", "QQQ 1d", "IWM 1d", "DIA 1d"]


def barra(ts, close, precio=None):
    return Barra(datetime.fromisoformat(ts), close, precio or close)


class Datos(unittest.TestCase):
    def test_filtra_is_antes_de_leer_precios(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "mixto.csv"
            def escribir(fuera):
                with p.open("w", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(["Date", "Close", "Unadjusted Close"])
                    w.writerows([["2008-01-01", fuera, fuera], ["2010-01-04", 100, 110],
                                 ["2010-01-05", 101, 111], ["2021-01-01", fuera, fuera]])
            for nombre in ETF_DIARIOS:
                with self.subTest(nombre):
                    escribir("NO SE DEBE LEER")
                    a = cargar(nombre, ruta=p)
                    escribir("OTRO VALOR INVÁLIDO")
                    self.assertEqual(a, cargar(nombre, ruta=p))
                    self.assertEqual([(b.close, b.precio) for b in a], [(100, 110), (101, 111)])

    def test_ningun_intervalo_fuera_de_is(self):
        for nombre in DATASETS:
            with self.subTest(nombre), self.assertRaisesRegex(ValueError, "BLOQUEADO"):
                cargar(nombre, fin=date(2021, 1, 1), ruta="nunca_abierto")

    def test_horas(self):
        bs = [barra(ts, c) for ts, c in [
            ("2015-03-01 23:45", 100), ("2015-03-02 00:45", 101), ("2015-03-02 01:45", 102),
            ("2015-03-02 16:45", 110), ("2015-03-02 17:45", 111), ("2015-03-02 18:45", 112),
            ("2015-03-01 16:45", 90), ("2015-03-01 18:45", 91)]]
        bs.sort(key=lambda b: b.ts)
        horas = {(p.fin.ts.day, p.fin.ts.hour): p.inicio.ts.strftime("%d %H:%M") for p in periodos(bs, "1h", excluir_horas=[17])}
        self.assertEqual(horas, {(2, 0): "01 23:45", (2, 1): "02 00:45", (2, 18): "02 16:45"})  # domingo 18 y hora 17 fuera


class Catalogo(unittest.TestCase):
    def test_dias_de_mes_solo_meses_completos(self):
        bs = [barra(f"2015-{m:02}-{d:02} 16:00", 100 + i) for i, (m, d) in enumerate(
            [(m, d) for m in (1, 2, 3) for d in range(1, 9)])]
        obs = dias_de_mes(periodos(bs, "1d"), [-1, 1], date(2015, 1, 5), date(2015, 3, 5), "mes")
        self.assertEqual({o.unidad for o in obs}, {"2015-02"})
        self.assertEqual([o.etiqueta for o in obs], [1, 2, 3, 4, -4, -3, -2, -1])
        self.assertEqual([o.en_ventana for o in obs], [True] + [False] * 6 + [True])

    def test_bateria_con_efecto_constante(self):
        g = {f"{2010 + i // 12}-{i % 12 + 1:02}": [4, .04, 16, 0] for i in range(24)}
        obs = list(g.values())
        self.assertAlmostEqual(media_vs_resto(obs), 100)
        for x in bootstrap(obs, media_vs_resto, bloque=3, replicas=100):
            self.assertAlmostEqual(x, 100)
        self.assertEqual(bootstrap(obs, media_vs_resto, 3, 100), bootstrap(obs, media_vs_resto, 3, 100))
        self.assertEqual(list(por_anio(g, media_vs_resto)), ["2010", "2011"])
        self.assertAlmostEqual(sin_cada_anio(g, media_vs_resto)["2010"], 100)


class Backtest(unittest.TestCase):
    def test_una_unidad_retorno_total_y_costes_de_ambos_lados(self):
        # Enero y febrero de 4 sesiones; ventana -1..+1: entra al cierre de la sesión 3 de enero y sale en la 1 de febrero.
        bs = [barra(f"2010-{m:02}-0{d} 16:00", 100 + i, 200) for i, (m, d) in enumerate([(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (2, 4)])]
        obs = [o for o in dias_de_mes(periodos(bs, "1d"), [-1, 1], date(2009, 12, 1), date(2010, 2, 28), "mes")]
        sesiones, operaciones = backtest(obs, 2, 10000, .01)
        t, = operaciones
        bruto = 200 * (104 / 102 - 1)
        self.assertAlmostEqual(t.pnl_bruto, bruto)
        self.assertAlmostEqual(t.coste_salida, .01 * 104 / 102)
        self.assertAlmostEqual(sesiones[-1].equity, 10000 + bruto - .01 - .01 * 104 / 102)
        self.assertEqual([s.exposicion for s in sesiones], [0, 0, 1, 1, 0, 0, 0])

    def test_fraccion_de_equity_se_reinvierte(self):
        # Dos meses con ventana -1..+1: cada operación compra el 30 % de la equity al cierre de entrada.
        dias = [(m, d) for m in (1, 2, 3) for d in (1, 2, 3, 4)]
        bs = [barra(f"2010-{m:02}-0{d} 16:00", 100 + i, 100 + i) for i, (m, d) in enumerate(dias)]
        obs = dias_de_mes(periodos(bs, "1d"), [-1, 1], date(2009, 12, 1), date(2010, 3, 31), "mes")
        sesiones, (t1, t2) = backtest(obs, 2, 10000, .01, fraccion=.3)
        a1 = .3 * 10000 / 102
        self.assertAlmostEqual(t1.coste_entrada, .01 * a1)
        self.assertAlmostEqual(t1.pnl_bruto, a1 * 2)
        a2 = .3 * (10000 + t1.pnl_neto) / 106
        self.assertAlmostEqual(t2.pnl_bruto, a2 * 2)
        self.assertAlmostEqual(sesiones[-1].equity, 10000 + t1.pnl_neto + t2.pnl_neto)
        with self.assertRaisesRegex(ValueError, "apalancamiento"):
            backtest(obs, 2, 10000, .01, fraccion=1.5)

    def test_racha_incompleta_o_con_hueco_no_opera(self):
        bs = [barra(f"2015-03-02 {h:02}:45", 100 + h) for h in (0, 1, 3, 4)]
        obs = hora(periodos(bs, "1h"), [2, 3], None, None, "día")
        self.assertEqual(backtest(obs, 2, 10000, .125)[1], [])


if __name__ == "__main__":
    unittest.main()


class PlanH007(unittest.TestCase):
    def test_especificacion_corre_con_barras_sinteticas(self):
        import random
        from datetime import timedelta
        from laboratorio import ejecutar
        rng, precio, ts, bs = random.Random(1), 2000.0, datetime(2018, 1, 7, 18), []
        while ts < datetime(2018, 3, 3):
            if ts.hour != 17 and not (ts.weekday() == 5 or (ts.weekday() == 4 and ts.hour >= 17) or (ts.weekday() == 6 and ts.hour < 18)):
                precio += rng.choice([-.25, 0, .25])
                bs.append(Barra(ts, precio, precio))
            ts += timedelta(minutes=15)
        plan = "experimentos/H007-IS-REAL-001.md"
        spec = ejecutar.leer_plan(ejecutar.motor.RAIZ / plan)
        r, sesiones, operaciones = ejecutar.ejecutar(spec, plan, barras=bs, inicio=date(2018, 1, 1), fin=date(2018, 12, 31))
        self.assertTrue(r.experimento.sintetico)
        self.assertEqual(len(r.evidencia.desglose), 23)
        self.assertEqual(len(operaciones), 40)  # 8 semanas × 5 días
        self.assertTrue(all(o.entrada == o.salida for o in operaciones))
