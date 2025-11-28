# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QPushButton, QLineEdit, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt

from Livre_compte.controller.user_controller import UserController


class UserWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestion des Utilisateurs")
        self.setMinimumSize(700, 500)

        self.controller = UserController()

        layout = QVBoxLayout()

        # Title
        title = QLabel("Gestion des Utilisateurs")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Table
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nom", "Prénom", "Identifiant", "Téléphone", "Adresse", "Rôle"
        ])
        self.table.setColumnHidden(0, True)  # ID invisible
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # FORMULAIRE AJOUT
        form_add = QHBoxLayout()

        self.in_nom = QLineEdit()
        self.in_nom.setPlaceholderText("Nom")
        form_add.addWidget(self.in_nom)

        self.in_prenom = QLineEdit()
        self.in_prenom.setPlaceholderText("Prénom")
        form_add.addWidget(self.in_prenom)

        self.in_mdp = QLineEdit()
        self.in_mdp.setPlaceholderText("Mot de passe")
        self.in_mdp.setEchoMode(QLineEdit.EchoMode.Password)
        form_add.addWidget(self.in_mdp)

        self.in_tel = QLineEdit()
        self.in_tel.setPlaceholderText("Téléphone")
        form_add.addWidget(self.in_tel)

        self.in_addr = QLineEdit()
        self.in_addr.setPlaceholderText("Adresse")
        form_add.addWidget(self.in_addr)

        self.in_role = QComboBox()
        self.in_role.addItems(["user", "admin"])
        form_add.addWidget(self.in_role)

        btn_add = QPushButton("Ajouter")
        btn_add.clicked.connect(self.add_user)
        form_add.addWidget(btn_add)

        layout.addLayout(form_add)

        # FORMULAIRE MODIFICATION
        form_mod = QHBoxLayout()

        self.mod_nom = QLineEdit()
        self.mod_nom.setPlaceholderText("Nouveau nom")
        form_mod.addWidget(self.mod_nom)

        self.mod_prenom = QLineEdit()
        self.mod_prenom.setPlaceholderText("Nouveau prénom")
        form_mod.addWidget(self.mod_prenom)

        self.mod_tel = QLineEdit()
        self.mod_tel.setPlaceholderText("Téléphone")
        form_mod.addWidget(self.mod_tel)

        self.mod_addr = QLineEdit()
        self.mod_addr.setPlaceholderText("Adresse")
        form_mod.addWidget(self.mod_addr)

        self.mod_role = QComboBox()
        self.mod_role.addItems(["user", "admin"])
        form_mod.addWidget(self.mod_role)

        btn_mod = QPushButton("Modifier")
        btn_mod.clicked.connect(self.modify_user)
        form_mod.addWidget(btn_mod)

        layout.addLayout(form_mod)

        # Delete button
        btn_delete = QPushButton("Supprimer utilisateur sélectionné")
        btn_delete.clicked.connect(self.delete_user)
        layout.addWidget(btn_delete)

        self.setLayout(layout)
        self.load_users()

    # -------------------------------------------------------
    # Load users
    # -------------------------------------------------------
    def load_users(self):
        from Livre_compte.database.db import get_connection

        self.table.setRowCount(0)

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM utilisateur ORDER BY id DESC")
            rows = cursor.fetchall()

            for row in rows:
                r = self.table.rowCount()
                self.table.insertRow(r)

                self.table.setItem(r, 0, QTableWidgetItem(str(row["id"])))
                self.table.setItem(r, 1, QTableWidgetItem(row["nom"]))
                self.table.setItem(r, 2, QTableWidgetItem(row["prenom"]))
                self.table.setItem(r, 3, QTableWidgetItem(row["nomUtilisateur"]))
                self.table.setItem(r, 4, QTableWidgetItem(row["numTelephone"]))
                self.table.setItem(r, 5, QTableWidgetItem(row["adresse"]))
                self.table.setItem(r, 6, QTableWidgetItem(row["role"]))

    # -------------------------------------------------------
    # Add user
    # -------------------------------------------------------
    def add_user(self):
        nom = self.in_nom.text().strip()
        prenom = self.in_prenom.text().strip()
        mdp = self.in_mdp.text().strip()
        tel = self.in_tel.text().strip()
        addr = self.in_addr.text().strip()
        role = self.in_role.currentText()

        if not nom or not prenom or not mdp:
            QMessageBox.warning(self, "Erreur", "Nom, prénom et mot de passe obligatoires.")
            return

        identifiant = self.controller.register(nom, prenom, mdp, tel, addr, role)

        QMessageBox.information(self, "Succès",
                                f"Utilisateur ajouté.\nIdentifiant généré : {identifiant}")

        self.in_nom.clear()
        self.in_prenom.clear()
        self.in_mdp.clear()
        self.in_tel.clear()
        self.in_addr.clear()

        self.load_users()

    # -------------------------------------------------------
    # Modify user
    # -------------------------------------------------------
    def modify_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un utilisateur.")
            return

        user_id = int(self.table.item(row, 0).text())
        role = self.table.item(row, 6).text()

        if role == "admin" and self.mod_role.currentText() == "user":
            confirm = QMessageBox.question(
                self, "Confirmer",
                "Voulez-vous rétrograder cet admin en utilisateur ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm != QMessageBox.StandardButton.Yes:
                return

        nom = self.mod_nom.text().strip() or self.table.item(row, 1).text()
        prenom = self.mod_prenom.text().strip() or self.table.item(row, 2).text()
        tel = self.mod_tel.text().strip() or self.table.item(row, 4).text()
        addr = self.mod_addr.text().strip() or self.table.item(row, 5).text()
        new_role = self.mod_role.currentText()

        from Livre_compte.database.db import get_connection

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE utilisateur
                SET nom=?, prenom=?, numTelephone=?, adresse=?, role=?
                WHERE id=?
            """, (nom, prenom, tel, addr, new_role, user_id))
            conn.commit()

        QMessageBox.information(self, "Succès", "Utilisateur modifié.")
        self.load_users()

        self.mod_nom.clear()
        self.mod_prenom.clear()
        self.mod_tel.clear()
        self.mod_addr.clear()

    # -------------------------------------------------------
    # Delete user
    # -------------------------------------------------------
    def delete_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un utilisateur.")
            return

        user_id = int(self.table.item(row, 0).text())
        role = self.table.item(row, 6).text()

        if role == "admin":
            QMessageBox.warning(self, "Erreur", "Impossible de supprimer un administrateur.")
            return

        confirm = QMessageBox.question(
            self, "Confirmer", "Supprimer cet utilisateur ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        from Livre_compte.database.db import get_connection

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM utilisateur WHERE id=?", (user_id,))
            conn.commit()

        QMessageBox.information(self, "Succès", "Utilisateur supprimé.")
        self.load_users()

