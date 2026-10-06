"""Tabla de variantes: precios por hora, sesión previa, señal, serie y desfase; contrato y validación del libro."""
import csv
from datetime import date, datetime, timedelta
from pathlib import Path
import random
import tempfile
import unittest

from pydantic import ValidationError

from laboratorio import ejecutar, motor
from laboratorio.contratos import Resumen
from laboratorio.datos import Barra, cargar_serie
from laboratorio.variantes import desfase, previa, tabla

PLAN = "experimentos/H-007-deriva-nocturna-es/H007-IS-REAL-002-od-tabla-variantes.md"


def barras_es(inicio=datetime(2018, 1, 7, 18), fin=datetime(2018, 3, 3), semilla=1):
    """ES sintético de 15 min con la sesión de Globex (cierra viernes 17:00, abre domingo 18:00; pausa a las 17)."""
    rng, precio, ts, bs = random.Random(semilla), 2000.0, inicio, []
    while ts < fin:
        if ts.hour != 17 and not (ts.weekday() == 5 or (ts.weekday() == 4 and ts.hour >= 17) or (ts.weekday() == 6 and ts.hour < 18)):
            precio += rng.choice([-.25, 0, .25])
            bs.append(Barra(ts, precio, precio))
        ts += timedelta(minutes=15)
    return bs


class Calendario(unittest.TestCase):
    def test_desfase_2010(self):
        # EE. UU.: 14-mar y 7-nov; Europa: 28-mar y 31-oct
        for d, esperado in [("2010-03-12", False), ("2010-03-15", True), ("2010-03-26", True), ("2010-03-29", False),
                            ("2010-07-01", False), ("2010-10-29", False), ("2010-11-01", True), ("2010-11-05", True),
                            ("2010-11-08", False)]:
            with self.subTest(d):
                self.assertEqual(desfase(date.fromisoformat(d)), esperado)

    def test_previa_del_lunes_es_el_viernes(self):
        self.assertEqual(previa(date(2018, 1, 15)), date(2018, 1, 12))
        self.assertEqual(previa(date(2018, 1, 16)), date(2018, 1, 15))


class Tabla(unittest.TestCase):
    def test_precios_senal_y_serie(self):
        p = {"2018-01-12 15:00": 100, "2018-01-12 16:00": 99,            # viernes: 15:15 -> 16:15 = -1 %
             "2018-01-15 01:15": 50, "2018-01-15 01:45": 51, "2018-01-15 02:45": 53, "2018-01-15 03:15": 54,
             "2018-01-16 01:45": 60}                                     # martes: falta la salida
        bs = [Barra(datetime.fromisoformat(ts), c, c) for ts, c in sorted(p.items())]
        filas = tabla(bs, "15min", {"OD": ["02:00", "03:00"], "OD+": ["01:30", "03:30"]}, ["15:15", "16:15"],
                      {date(2018, 1, 12): 21.5})
        self.assertEqual([(f.fecha.isoformat(), f.ventana, f.entrada, f.salida) for f in filas],
                         [("2018-01-15", "OD", 51, 53), ("2018-01-15", "OD+", 50, 54)])
        f = filas[0]
        self.assertEqual(f.previa, date(2018, 1, 12))
        self.assertAlmostEqual(f.senal, -.01)
        self.assertEqual(f.serie, 21.5)
        self.assertFalse(f.desfase)

    def test_sin_datos_previos_quedan_vacios(self):
        bs = [Barra(datetime(2018, 1, 16, h, m), 10, 10) for h, m in [(1, 45), (2, 45)]]
        f, = tabla(bs, "15min", {"OD": ["02:00", "03:00"]}, ["15:15", "16:15"], {})
        self.assertIsNone(f.senal)
        self.assertIsNone(f.serie)


class SerieVIX(unittest.TestCase):
    def test_filtra_is_antes_de_leer_valores(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "vix.csv"
            with p.open("w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["Date", "Open", "High", "Low", "Close", "Volume", "Turnover"])
                w.writerows([["2008-10-10", 0, 0, 0, "NO SE DEBE LEER", 0, 0], ["2015-08-24", 0, 0, 0, 40.74, 0, 0],
                             ["2021-01-04", 0, 0, 0, "TAMPOCO", 0, 0]])
            self.assertEqual(cargar_serie("VIX 1d", ruta=p), {date(2015, 8, 24): 40.74})


class PlanH007Variantes(unittest.TestCase):
    def ejecutar(self):
        spec = ejecutar.leer_plan(ejecutar.motor.RAIZ / PLAN)
        bs = barras_es()
        vix = {d: 15 + (d.toordinal() % 20) for d in {b.ts.date() for b in bs}}
        return ejecutar.ejecutar(spec, PLAN, barras=bs, serie=vix, hoy=date(2026, 10, 5),
                                 inicio=date(2018, 1, 1), fin=date(2018, 12, 31))

    def test_base_reproduce_el_libro_y_guarda(self):
        r, sesiones, operaciones, al_100, filas = self.ejecutar()
        self.assertEqual(r.variantes.filas, len(filas))
        self.assertEqual(r.ficheros.variantes, "variantes.csv")
        base = [f for f in filas if f.ventana == "OD"]
        self.assertEqual(len(base), len(operaciones))
        self.assertAlmostEqual(sum(f.salida - f.entrada for f in base), sum(o.pnl_bruto for o in operaciones))
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "X"
            with self.assertRaisesRegex(ValueError, "variantes"):
                motor.guardar(d, r, sesiones, operaciones, al_100)
            motor.guardar(d, r, sesiones, operaciones, al_100, filas)
            self.assertTrue((d / "variantes.csv").exists())
            self.assertEqual(motor.cargar(d), (r, sesiones, operaciones))
            # una salida manipulada en la base deja de reproducir el libro
            texto = (d / "variantes.csv").read_text().splitlines()
            i = next(k for k, linea in enumerate(texto) if ",OD," in linea)
            campos = texto[i].split(",")
            campos[4] = str(float(campos[4]) + 1)
            texto[i] = ",".join(campos)
            (d / "variantes.csv").write_text("\n".join(texto) + "\n")
            with self.assertRaisesRegex(ValueError, "no reproduce"):
                motor.cargar(d)

    def test_contrato_exige_fichero(self):
        r = self.ejecutar()[0]
        datos = r.model_dump(mode="json")
        datos["ficheros"]["variantes"] = None
        with self.assertRaisesRegex(ValidationError, "variantes.csv"):
            Resumen.model_validate(datos)


if __name__ == "__main__":
    unittest.main()
