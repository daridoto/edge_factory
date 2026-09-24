import math
import statistics
import unittest

from laboratorio.contratos import Sesion
from laboratorio.motor import metricas, validar_contabilidad
from fixtura import muestra_pequena


def m(sesiones=None, operaciones=None):
    s, o = muestra_pequena()
    return metricas(100, sesiones if sesiones is not None else s, operaciones if operaciones is not None else o)


class Metricas(unittest.TestCase):
    def test_calculadas_a_mano(self):
        r, motivos, _ = m()
        for clave, esperado in {"esperanza": 1, "tasa_acierto": .5, "payoff": 8/6, "profit_factor": 8/6,
                                "rentabilidad_total": .02, "max_drawdown": 6/108, "costes": 4,
                                "peso_costes": 4/14, "exposicion": .5, "pnl_neto": 2}.items():
            self.assertAlmostEqual(getattr(r, clave), esperado, msg=clave)
        self.assertIsNone(r.rentabilidad_anual)
        self.assertIsNone(r.max_recuperacion)
        self.assertEqual(r.drawdown_abierto, 2)
        self.assertIn("rentabilidad_anual", motivos)

    def test_retornos_incluyen_capital_inicial_y_dias_sin_posicion(self):
        ret = [-.01, 108/99-1, 107/108-1, 102/107-1]
        r, _, _ = m()
        self.assertAlmostEqual(r.sharpe, math.sqrt(252)*statistics.mean(ret)/statistics.stdev(ret))
        self.assertAlmostEqual(r.sortino, math.sqrt(252)*statistics.mean(ret)/math.sqrt(sum(min(x, 0)**2 for x in ret)/4))
        self.assertAlmostEqual(r.rotacion, sum(20/e for e in [100, 99, 108, 107]))

    def test_sin_operaciones_da_null_con_motivo(self):
        s, _ = muestra_pequena()
        s = [x.model_copy(update=dict(equity=100, coste=0, pnl_bruto=0, nocional=0, exposicion=0)) for x in s]
        r, motivos, _ = m(s, [])
        for clave in ("sharpe", "sortino", "esperanza", "payoff", "profit_factor", "peso_costes"):
            self.assertIsNone(getattr(r, clave))
            self.assertTrue(motivos[clave])
        self.assertEqual(r.max_recuperacion, 0)

    def test_recuperacion_desde_pico_inicial(self):
        s, o = muestra_pequena()
        s = [x.model_copy(update=dict(equity=e)) for x, e in zip(s, [90, 95, 100, 110])]
        r, _, _ = m(s, o)
        self.assertAlmostEqual(r.max_drawdown, .1)
        self.assertEqual(r.max_recuperacion, 3)

    def test_anualizacion_con_un_anio(self):
        s = [Sesion(fecha=f"2019-01-01", equity=100 * 1.001**i, pnl_bruto=0, coste=0, nocional=0, exposicion=0)
             for i in range(1, 253)]
        r, _, _ = metricas(100, s, [])
        self.assertAlmostEqual(r.rentabilidad_anual, 1.001**252-1)


class Contabilidad(unittest.TestCase):
    def invalida(self, frase, sesiones=None, operaciones=None, inicio="2019-01-01", fin="2019-01-04"):
        s, o = muestra_pequena()
        with self.assertRaisesRegex(ValueError, frase):
            validar_contabilidad(100, inicio, fin, sesiones if sesiones is not None else s,
                                 operaciones if operaciones is not None else o)

    def test_muestra_valida(self):
        validar_contabilidad(100, "2019-01-01", "2019-01-04", *muestra_pequena())

    def test_equity_no_concilia(self):
        s, _ = muestra_pequena()
        s[0] = s[0].model_copy(update=dict(coste=2))
        self.invalida("no concilia", sesiones=s)

    def test_costes_de_operaciones_no_concilian(self):
        _, o = muestra_pequena()
        o[0] = o[0].model_copy(update=dict(coste_entrada=2, pnl_neto=7))
        self.invalida("no concilian", operaciones=o)

    def test_operacion_duplicada_o_fuera_de_muestra(self):
        _, o = muestra_pequena()
        self.invalida("duplicada", operaciones=[o[0], o[0]])
        self.invalida("fuera de la muestra", operaciones=[o[0].model_copy(update=dict(salida="2019-01-09"))])

    def test_fechas_y_cobertura(self):
        s, _ = muestra_pequena()
        self.invalida("fechas únicas", sesiones=[s[0], s[0], s[2], s[3]])
        self.invalida("fechas únicas", sesiones=[])

    def test_oos_bloqueado(self):
        self.invalida("BLOQUEADO", inicio="2021-01-04", fin="2021-01-07")


if __name__ == "__main__":
    unittest.main()
