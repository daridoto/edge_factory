import json
from pathlib import Path
import tempfile
import unittest

from pydantic import ValidationError

from laboratorio.contratos import ESQUEMAS, Operacion, Resumen, exportar_esquemas
from laboratorio.proteccion import exigir_is
from fixtura import experimento

RAIZ = Path(__file__).resolve().parents[1]


class Contratos(unittest.TestCase):
    def setUp(self):
        self.resumen = experimento()[0]
        self.datos = self.resumen.model_dump(mode="json")

    def invalido(self, frase):
        with self.assertRaisesRegex(ValidationError, frase):
            Resumen.model_validate(self.datos)

    def test_resumen_valido_y_estable(self):
        self.assertEqual(Resumen.model_validate(self.datos), self.resumen)
        self.assertEqual(self.resumen, experimento()[0])

    def test_esquemas_exportados_al_dia(self):
        with tempfile.TemporaryDirectory() as tmp:
            exportar_esquemas(tmp)
            for nombre in ESQUEMAS:
                self.assertEqual(json.loads((Path(tmp) / f"{nombre}.schema.json").read_text()),
                                 json.loads((RAIZ / "esquemas" / f"{nombre}.schema.json").read_text()), nombre)

    def test_oos_bloqueado_en_el_contrato(self):
        self.datos["experimento"]["fin"] = "2021-01-04"
        self.invalido("BLOQUEADO")
        self.datos["experimento"]["fin"] = "2020-12-31"
        self.datos["experimento"]["muestra"] = "OOS"
        self.invalido("muestra")
        for inicio, fin in (("2009-09-26", "2010-01-01"), ("2020-01-01", "2021-01-01")):
            with self.assertRaisesRegex(ValueError, "BLOQUEADO"):
                exigir_is(inicio, fin)

    def test_campo_desconocido_y_no_finito(self):
        self.datos["extra"] = 1
        self.invalido("extra")
        del self.datos["extra"]
        self.datos["evidencia"]["valor"] = float("nan")
        self.invalido("finite")

    def test_metrica_null_sin_motivo(self):
        self.datos["metricas"]["sharpe"] = None
        self.datos["no_calculables"].pop("sharpe", None)
        self.invalido("sin motivo")

    def test_pnl_neto_de_operacion(self):
        with self.assertRaisesRegex(ValidationError, "pnl_neto"):
            Operacion(id="x", entrada="2019-01-01", salida="2019-01-02", pnl_bruto=1, coste_entrada=0, coste_salida=0, pnl_neto=2)


if __name__ == "__main__":
    unittest.main()
