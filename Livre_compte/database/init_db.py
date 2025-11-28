import os
import sys
from pathlib import Path

def resource_path(relative_path: str):
    """Donne le vrai chemin du fichier, même dans PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def initialize_database():
    from Livre_compte.database.db import get_connection
    
    sql_path = resource_path("Livre_compte/database/init_db.sql")

    # Lire le fichier SQL
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()

