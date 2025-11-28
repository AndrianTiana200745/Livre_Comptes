# -*- coding: utf-8 -*-
from Livre_compte.database.db import get_connection

# ============================================================
# CRUD Branche
# ============================================================
def add_branche(nom: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO branche (nom) VALUES (?)", (nom,))
    conn.commit()
    last_id = cur.lastrowid
    cur.close()
    conn.close()
    return last_id


def init_main_branche():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM branche WHERE nom = ?", ("Principale",))
    result = cur.fetchone()

    if result is None:
        cur.execute("INSERT INTO branche (nom) VALUES (?)", ("Principale",))
        conn.commit()
        main_id = cur.lastrowid
    else:
        main_id = result[0]

    cur.close()
    conn.close()
    return main_id


def list_branches():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nom FROM branche ORDER BY nom ASC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [{"id": row[0], "nom": row[1]} for row in rows]


def get_branche_by_id(id_branche: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nom FROM branche WHERE id = ?", (id_branche,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {"id": row[0], "nom": row[1]}
    return None


def count_branches() -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) FROM branche")
    (count,) = cur.fetchone()
    cur.close()
    conn.close()
    return int(count)


def update_branche(id_branche: int, new_name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE branche SET nom = ? WHERE id = ?", (new_name, id_branche))
    conn.commit()
    cur.close()
    conn.close()


def delete_branche(id_branche: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM branche WHERE id = ?", (id_branche,))
    conn.commit()
    cur.close()
    conn.close()

