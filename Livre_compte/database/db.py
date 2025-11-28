# database/db.py
import sqlite3
from pathlib import Path

# >>> Correction : définir correctement le chemin de la base <<<
BASE_DIR = Path(__file__).resolve().parent       # dossier /database
DB_PATH = BASE_DIR / "livrecompte.db"            # fichier BD

def get_connection():
    # S’assure que le dossier existe
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(
        str(DB_PATH),
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )

    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    sql_path = BASE_DIR / "init_db.sql"

    if not sql_path.exists():
        raise FileNotFoundError(f"❌ Fichier introuvable : {sql_path}")

    sql = sql_path.read_text(encoding="utf-8")

    with get_connection() as conn:
        conn.executescript(sql)

