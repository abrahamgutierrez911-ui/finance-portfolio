from pathlib import Path
import sys


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from automates.pipeline import ejecutar_pipeline  # noqa: E402


if __name__ == "__main__":
    resultado = ejecutar_pipeline(RAIZ / "data" / "synthetic", RAIZ / "output")
    print(f"Pipeline completado. Reportes por fondeador: {resultado['cantidad_reportes']}")
    print("Bitácora: output/bitacora_ejecucion.csv")
