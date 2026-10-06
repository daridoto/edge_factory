"""`ejecutar <plan>` corre un experimento; `indice` reconstruye indice.csv; `ficha <dir>` valida y regenera ficha.md;
`referencia <dir>…` añade el riesgo al 100 % a experimentos guardados antes del esquema 2.1."""
import argparse
from pathlib import Path
import sys

from . import ejecutar, motor
from .presentacion import render


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="comando", required=True)
    ej = sub.add_parser("ejecutar", help="Ejecuta la especificación de un plan y guarda resultados/<H-NNN-nombre>/<ID>-<variante>/")
    ej.add_argument("plan", type=Path)
    sub.add_parser("indice", help="Reconstruye resultados/indice.csv validando cada experimento")
    ficha = sub.add_parser("ficha", help="Valida un experimento y regenera su ficha.md")
    ficha.add_argument("directorio", type=Path)
    ref = sub.add_parser("referencia", help="Añade la referencia al 100 %% a experimentos guardados (reejecuta y verifica)")
    ref.add_argument("directorios", type=Path, nargs="+")
    args = parser.parse_args()
    try:
        if args.comando == "ejecutar":
            print(f"Ficha: {ejecutar.main(args.plan) / 'ficha.md'}")
        elif args.comando == "referencia":
            for d in args.directorios:
                r = ejecutar.anadir_referencia(d).referencia
                print(f"{d.name}: DD al 100 % {r.max_drawdown:.2%} ({r.pico} → {r.valle})")
            motor.reconstruir_indice()
        elif args.comando == "indice":
            print(f"{len(motor.reconstruir_indice())} experimento(s) en {motor.RESULTADOS / 'indice.csv'}")
        else:
            resumen, _, _ = motor.cargar(args.directorio)
            (args.directorio / "ficha.md").write_text(render(resumen))
            print(f"Ficha: {args.directorio / 'ficha.md'}")
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
