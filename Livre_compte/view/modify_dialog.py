# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QDateEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate


class ModifyDialog(QDialog):
    def __init__(self, data, branches, on_save_callback):
        super().__init__()
        self.setWindowTitle("Modifier une ligne")
        self.resize(350, 250)

        self.data = data
        self.on_save_callback = on_save_callback

        layout = QFormLayout()
        self.setLayout(layout)

        # Champs
        self.input_designation = QLineEdit(data["designation"])
        self.input_montant = QLineEdit(str(data["montant"]))

        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)

        date_val = data["date"]

        if hasattr(date_val, "strftime"):
            date_val = date_val.strftime("%Y-%m-%d")

        self.input_date.setDate(QDate.fromString(str(date_val), "yyyy-MM-dd"))

        self.input_branche = QComboBox()
        for b in branches:
            self.input_branche.addItem(b["nom"], b["id"])

        self.input_branche.setCurrentIndex(
            self.input_branche.findData(data["id_branche"])
        )

        layout.addRow("Désignation:", self.input_designation)
        layout.addRow("Montant:", self.input_montant)
        layout.addRow("Date:", self.input_date)
        layout.addRow("Branche:", self.input_branche)

        btn_save = QPushButton("Enregistrer")
        btn_save.clicked.connect(self.save)
        layout.addRow(btn_save)

    def save(self):
        try:
            montant = float(self.input_montant.text())
        except:
            QMessageBox.warning(self, "Erreur", "Montant invalide")
            return

        new_data = {
            "designation": self.input_designation.text(),
            "montant": montant,
            "date": self.input_date.date().toPyDate(),
            "id_branche": self.input_branche.currentData()
        }

        self.on_save_callback(new_data)
        self.accept()

