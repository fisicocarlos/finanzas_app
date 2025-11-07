import locale
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


APP_NAME = "FINANZAS PERSONALES"
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

GOOGLE_DRIVE_FILE_ID = os.getenv("GOOGLE_DRIVE_FILE_ID")
GOOGLE_DRIVE_URL_TEMPLATE = (
    "https://docs.google.com/spreadsheets/d/{sheet_id}/export?"
    "format=csv&id={sheet_id}&gid={{gid}}"
).format(sheet_id=GOOGLE_DRIVE_FILE_ID)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Translations
TRANSLATIONS = {
    "en": {
        "expense": "expenses",
        "income": "incomes",
        "total": "total",
        "description": "description",
        "amount": "amount",
    },
    "es": {
        "expense": "gastos",
        "income": "ingresos",
        "total": "total",
        "description": "descripción",
        "amount": "Importe",
    },
}

MONTHS_ORDER = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]

# Logging
LOG_FILE = LOG_DIR / "app.logs"
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        # logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ],
)

logger = logging.getLogger(APP_NAME)
