# Livre_compte/model/user_model.py
import bcrypt
from Livre_compte.database.db import get_connection

class UserModel:

    def generer_identifiant(self, nom, prenom):
        base = (nom[0] + prenom).lower()
        identifiant = base
        n = 1

        with get_connection() as conn:
            cursor = conn.cursor()
            while cursor.execute(
                "SELECT 1 FROM utilisateur WHERE nomUtilisateur=?",
                (identifiant,)
            ).fetchone():
                identifiant = f"{base}{n}"
                n += 1

        return identifiant

    def create_user(self, nom, prenom, mdp, tel, adresse, role="user"):
        identifiant = self.generer_identifiant(nom, prenom)

        hashed = bcrypt.hashpw(mdp.encode('utf-8'), bcrypt.gensalt())

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO utilisateur (nom, prenom, nomUtilisateur, motDePasse, numTelephone, adresse, role)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nom, prenom, identifiant, hashed, tel, adresse, role))
            conn.commit()

        return identifiant

    def auth(self, identifiant, mdp):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM utilisateur
                WHERE nomUtilisateur=?
            """, (identifiant,))
            row = cursor.fetchone()
            if row and bcrypt.checkpw(mdp.encode('utf-8'), row["motDePasse"]):
                return row
            return None
    def create_default_admin(self):
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM utilisateur 
                WHERE nom='Admin' AND prenom='Principal'
            """)
            existe = cursor.fetchone()

            if existe:
                return False   # Aucun admin créé

            # Création admin
            nom = "Admin"
            prenom = "Principal"
            mdp = "admin123"
            tel = "0000000000"
            adresse = "Système"

            identifiant = "admin"
            hashed = bcrypt.hashpw(mdp.encode('utf-8'), bcrypt.gensalt())

            cursor.execute("""
                INSERT INTO utilisateur (nom, prenom, nomUtilisateur, motDePasse, numTelephone, adresse, role)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nom, prenom, identifiant, hashed, tel, adresse, "admin"))
            conn.commit()

            return True   # Admin créé

