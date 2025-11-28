from ..database.db import get_connection
from datetime import date
from typing import List, Tuple
import sqlite3

# ============================================================
# BRANCHES CRUD
# ============================================================
def add_branche(nom: str) -> int:
    with get_connection() as conn:
        cur = conn.execute("INSERT INTO branche(nom) VALUES (?)", (nom,))
        return cur.lastrowid

def list_branches() -> List[sqlite3.Row]:
    with get_connection() as conn:
        cur = conn.execute("SELECT id, nom FROM branche ORDER BY nom")
        return cur.fetchall()

def update_branche(id_branche: int, new_name: str):
    with get_connection() as conn:
        conn.execute("UPDATE branche SET nom = ? WHERE id = ?", (new_name, id_branche))

def delete_branche(id_branche: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM branche WHERE id = ?", (id_branche,))


# ============================================================
# ENTRÉES CRUD
# ============================================================
def add_entree(designation: str, montant: float, date_entre: date, id_branche: int):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO argent_entrer(designation, montant, date_entre, id_branche) VALUES (?, ?, ?, ?)",
            (designation, montant, date_entre.isoformat(), id_branche)
        )

def update_entree(id_entree: int, designation: str, montant: float, date_entre: date, id_branche: int):
    with get_connection() as conn:
        conn.execute(
            """UPDATE argent_entrer
               SET designation = ?, montant = ?, date_entre = ?, id_branche = ?
               WHERE id = ?""",
            (designation, montant, date_entre.isoformat(), id_branche, id_entree)
        )

def delete_entree(id_entree: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM argent_entrer WHERE id = ?", (id_entree,))


# ============================================================
# DÉPENSES CRUD
# ============================================================
def add_depense(designation: str, montant: float, date_sortie: date, id_branche: int):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO argent_depense(designation, montant, date_sortie, id_branche) VALUES (?, ?, ?, ?)",
            (designation, montant, date_sortie.isoformat(), id_branche)
        )

def update_depense(id_depense: int, designation: str, montant: float, date_sortie: date, id_branche: int):
    with get_connection() as conn:
        conn.execute(
            """UPDATE argent_depense
               SET designation = ?, montant = ?, date_sortie = ?, id_branche = ?
               WHERE id = ?""",
            (designation, montant, date_sortie.isoformat(), id_branche, id_depense)
        )

def delete_depense(id_depense: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM argent_depense WHERE id = ?", (id_depense,))


# ============================================================
# VUES GLOBALES
# ============================================================
def get_global_view(id_branche: int | None, year: int | None = None, month: int | None = None) -> Tuple[list, list]:
    with get_connection() as conn:
        where_e, where_d = [], []
        params_e, params_d = [], []

        if id_branche is not None:
            where_e.append("id_branche = ?"); params_e.append(id_branche)
            where_d.append("id_branche = ?"); params_d.append(id_branche)

        if year is not None:
            where_e.append("strftime('%Y', date_entre) = ?"); params_e.append(str(year))
            where_d.append("strftime('%Y', date_sortie) = ?"); params_d.append(str(year))

        if month is not None:
            where_e.append("strftime('%m', date_entre) = ?"); params_e.append(f"{month:02d}")
            where_d.append("strftime('%m', date_sortie) = ?"); params_d.append(f"{month:02d}")

        q_e = "SELECT e.*, b.nom AS branche_nom FROM argent_entrer e JOIN branche b ON e.id_branche=b.id"
        q_d = "SELECT d.*, b.nom AS branche_nom FROM argent_depense d JOIN branche b ON d.id_branche=b.id"

        if where_e: q_e += " WHERE " + " AND ".join(where_e)
        if where_d: q_d += " WHERE " + " AND ".join(where_d)

        return conn.execute(q_e, params_e).fetchall(), conn.execute(q_d, params_d).fetchall()

def total_from_rows(rows) -> float:
    return sum(float(r["montant"]) for r in rows) if rows else 0.0

