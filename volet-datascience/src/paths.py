from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = DATA_DIR / "output"

RELEVES_PATH = RAW_DIR / "releves_consommation.csv"
METEO_PATH = RAW_DIR / "meteo.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)