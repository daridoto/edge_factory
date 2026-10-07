import unittest
from datetime import date, datetime, timedelta

from laboratorio.datos import Barra, periodos
from laboratorio.festivos import festivos, pascua, vispera


class Calendario(unittest.TestCase):
    def test_pascua(self):
        for d in (date(2010, 4, 4), date(2011, 4, 24), date(2016, 3, 27), date(2019, 4, 21), date(2024, 3, 31)):
            self.assertEqual(pascua(d.year), d)

    def test_reglas_de_observado(self):
        self.assertEqual(festivos(2015)["independencia"], date(2015, 7, 3))   # sábado → viernes
        self.assertEqual(festivos(2021)["independencia"], date(2021, 7, 5))   # domingo → lunes
        self.assertEqual(festivos(2021)["navidad"], date(2021, 12, 24))
        self.assertEqual(festivos(2012)["ano_nuevo"], date(2012, 1, 2))
        self.assertNotIn("ano_nuevo", festivos(2022))                          # sábado: NYSE no cierra
        f = festivos(2020)
        self.assertEqual((f["presidentes"], f["memorial"], f["trabajo"], f["accion_gracias"], f["viernes_santo"]),
                         (date(2020, 2, 17), date(2020, 5, 25), date(2020, 9, 7), date(2020, 11, 26), date(2020, 4, 10)))

    def test_vispera_es_la_sesion_anterior(self):
        dias = {date(2020, 11, 23) + timedelta(i) for i in range(7) if i not in (3, 5, 6)}   # sin jueves 26 ni fin de semana
        self.assertEqual(vispera(dias), {date(2020, 11, 25): "accion_gracias"})
        self.assertEqual(vispera(dias, ["navidad"]), {})

    def test_festivo_que_es_sesion_falla(self):
        with self.assertRaises(ValueError):
            vispera({date(2020, 11, 25), date(2020, 11, 26), date(2020, 11, 27)})

    def test_ventana(self):
        from laboratorio.catalogo import festivos as ventana
        dias = [date(2020, 12, d) for d in (21, 22, 23, 24, 28, 29)]
        bs = [Barra(datetime(d.year, d.month, d.day, 16), 100.0 + i, 100.0 + i) for i, d in enumerate(dias)]
        obs = ventana(periodos(bs, "1d"), ["navidad"], None, None, "mes")
        self.assertEqual([(o.periodo.fin.ts.day, o.etiqueta) for o in obs if o.en_ventana], [(24, "navidad")])
        self.assertEqual({o.etiqueta for o in obs if not o.en_ventana}, {"resto"})

    def test_vispera_regla_sin_lista_de_sesiones(self):
        from laboratorio.festivos import vispera_regla
        v = vispera_regla(date(2012, 1, 1), date(2012, 12, 31))
        self.assertEqual(v[date(2012, 4, 5)], "viernes_santo")
        self.assertEqual(v[date(2012, 12, 24)], "navidad")
        self.assertEqual(v[date(2012, 2, 17)], "presidentes")
        self.assertEqual(len(v), 8)

    def test_solo_vispera_filtra_horas(self):
        from laboratorio.catalogo import hora, solo_vispera
        bs = [Barra(datetime(2012, 4, d, h, 45), 100.0 + h, 100.0 + h) for d in (4, 5) for h in (14, 15, 16)]
        obs = solo_vispera(hora(periodos(bs, "1h"), [15], None, None, "día"), ["viernes_santo"])
        self.assertEqual({o.periodo.fin.ts.date() for o in obs}, {date(2012, 4, 5)})
