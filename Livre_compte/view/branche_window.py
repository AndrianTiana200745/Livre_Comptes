# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt

from Livre_compte.controller.branche_controller import (
    list_branches,
    add_branche,
    update_branche,
    delete_branche,
    init_main_branche
)


class BrancheWindow(QWidget):
    def __init__(self, on_refresh_callback=None):
        super().__init__()
        self.on_refresh_callback = on_refresh_callback

        self.setWindowTitle("Gestion des branches")
        self.resize(500, 420)

        layout = QVBoxLayout()

        # --- Titre ---
        title = QLabel("Gestion des Branches de l'Église")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # --- Table ---
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["ID", "Nom"])
        self.table.setColumnHidden(0, True)

        # Rendre le tableau responsive
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # colonne Nom étirable

        self.table.verticalHeader().setVisible(False)  # enlever les numéros de lignes

        layout.addWidget(self.table)

        # --- Ajout ---
        form_layout = QHBoxLayout()
        self.input_nom = QLineEdit()
        self.input_nom.setPlaceholderText("Nouvelle branche...")
        form_layout.addWidget(self.input_nom)

        add_btn = QPushButton("Ajouter")
        add_btn.clicked.connect(self.on_add_branche)
        form_layout.addWidget(add_btn)

        layout.addLayout(form_layout)

        # --- Modification ---
        mod_layout = QHBoxLayout()
        self.modify_input = QLineEdit()
        self.modify_input.setPlaceholderText("Nouveau nom...")
        mod_layout.addWidget(self.modify_input)

        btn_modify = QPushButton("Modifier")
        btn_modify.clicked.connect(self.on_modify_branche)
        mod_layout.addWidget(btn_modify)

        layout.addLayout(mod_layout)

        # --- Suppression ---
        btn_delete = QPushButton("Supprimer branche sélectionnée")
        btn_delete.clicked.connect(self.on_delete_branche)
        layout.addWidget(btn_delete)

        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        self.branches = list_branches()

        for b in self.branches:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(b["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(b["nom"]))

    def on_add_branche(self):
        nom = self.input_nom.text().strip()
        if not nom:
            QMessageBox.warning(self, "Erreur", "Entrez un nom de branche.")
            return

        add_branche(nom)
        QMessageBox.information(self, "Succès", "Branche ajoutée.")
        self.input_nom.clear()
        self.refresh_table()

        if self.on_refresh_callback:
            self.on_refresh_callback()

    def on_modify_branche(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Sélectionnez une branche.")
            return

        id_b = int(self.table.item(row, 0).text())
        new_name = self.modify_input.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Erreur", "Nom vide.")
            return

        update_branche(id_b, new_name)
        QMessageBox.information(self, "Succès", "Branche modifiée.")
        self.modify_input.clear()
        self.refresh_table()

        if self.on_refresh_callback:
            self.on_refresh_callback()

    def on_delete_branche(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Sélectionnez une branche.")
            return

        id_b = int(self.table.item(row, 0).text())
        nom = self.table.item(row, 1).text()

        if nom == "Principale":
            QMessageBox.warning(self, "Erreur", "Impossible de supprimer la branche principale.")
            return

        confirm = QMessageBox.question(
            self, "Confirmer", f"Supprimer '{nom}' ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            delete_branche(id_b)
            QMessageBox.information(self, "Succès", "Branche supprimée.")
            self.refresh_table()

            if self.on_refresh_callback:
                self.on_refresh_callback()

