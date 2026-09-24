import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

from laboratorio import motor
from fixtura import experimento

RAIZ = Path(__file__).resolve().parents[1]


class Resultados(unittest.TestCase):
    def test_guardar_cargar_indice_y_ficha(self):
        resumen, sesiones, operaciones = experimento()
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "X"
            motor.guardar(d, resumen, sesiones, operaciones)
            self.assertEqual(sorted(p.name for p in d.iterdir()), ["equity.csv", "ficha.md", "operaciones.csv", "resumen.json"])
            self.assertEqual(motor.cargar(d), (resumen, sesiones, operaciones))
            self.assertIn("DATOS SINTÉTICOS", (d / "ficha.md").read_text())
            with self.assertRaises(FileExistsError):
                motor.guardar(d, resumen, sesiones, operaciones)
            filas = motor.reconstruir_indice(tmp)
            self.assertEqual([f["id"] for f in filas], [resumen.experimento.id])
            original = (d / "ficha.md").read_text()
            (d / "ficha.md").write_text("")
            cli = subprocess.run([sys.executable, "-m", "laboratorio", "ficha", str(d)], cwd=RAIZ, capture_output=True, text=True)
            self.assertEqual(cli.returncode, 0, cli.stderr)
            self.assertEqual((d / "ficha.md").read_text(), original)

    def test_csv_manipulado_no_carga(self):
        resumen, sesiones, operaciones = experimento()
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "X"
            motor.guardar(d, resumen, sesiones, operaciones)
            lineas = (d / "equity.csv").read_text().splitlines()
            del lineas[next(i for i, l in enumerate(lineas[1:], 1) if l.split(",")[2] not in ("0.0", "-0.0"))]
            (d / "equity.csv").write_text("\n".join(lineas) + "\n")
            with self.assertRaisesRegex(ValueError, "concilia"):
                motor.cargar(d)


if __name__ == "__main__":
    unittest.main()
