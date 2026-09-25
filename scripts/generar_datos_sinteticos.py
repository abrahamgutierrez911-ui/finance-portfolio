from pathlib import Path
import sys


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from automates.demo_data import guardar_datasets  # noqa: E402


if __name__ == "__main__":
    conteos = guardar_datasets(RAIZ / "data" / "synthetic")
    for nombre, filas in conteos.items():
        print(f"Creado {nombre}: {filas:,} filas")
