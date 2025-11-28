# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QDateEdit, QLineEdit,
    QFormLayout, QMessageBox, QSpinBox, QFileDialog
)
from PyQt6.QtCore import QDate

from Livre_compte.controller.finance_controller import (
    list_branches, add_entree, add_depense, update_entree, update_depense,
    delete_entree, delete_depense, get_global_view
)
from Livre_compte.database.db import init_db
from Livre_compte.view.modify_dialog import ModifyDialog

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime


def export_global_to_pdf(entrees, depenses, path="export.pdf", title="Export Livre de Compte"):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, title)
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Date export: {datetime.now().isoformat()}")
    y -= 20

    c.drawString(40, y, "Entrées:")
    y -= 20
    for e in entrees:
        line = f"{e['date_entre']} - {e['designation']} - {float(e['montant']):.2f} ({e['branche_nom']})"
        c.drawString(60, y, line)
        y -= 14
        if y < 80:
            c.showPage()
            y = height - 50

    y -= 10
    c.drawString(40, y, "Dépenses:")
    y -= 20
    for d in depenses:
        line = f"{d['date_sortie']} - {d['designation']} - {float(d['montant']):.2f} ({d['branche_nom']})"
        c.drawString(60, y, line)
        y -= 14
        if y < 80:
            c.showPage()
            y = height - 50
    c.save()
    return path


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Livre de compte - Église")
        self.resize(1000, 700)

        layout = QVBoxLayout()

        # -------------------- FILTRES --------------------
        filter_layout = QHBoxLayout()

        self.branch_combo = QComboBox()
        self.load_branch_combobox()
        filter_layout.addWidget(QLabel("Branche:"))
        filter_layout.addWidget(self.branch_combo)

        self.year_spin = QSpinBox()
        self.year_spin.setRange(2000, 2100)
        self.year_spin.setValue(QDate.currentDate().year())
        filter_layout.addWidget(QLabel("Année:"))
        filter_layout.addWidget(self.year_spin)

        self.month_combo = QComboBox()
        self.month_combo.addItem("Tous", None)
        for i, name in enumerate([
            "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
        ], start=1):
            self.month_combo.addItem(name, i)
        filter_layout.addWidget(QLabel("Mois:"))
        filter_layout.addWidget(self.month_combo)

        layout.addLayout(filter_layout)

        # -------------------- TABLE --------------------
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Type", "Designation", "Montant", "Date", "Branche"]
        )
        layout.addWidget(self.table)

        # -------------------- ACTIONS --------------------
        action_layout = QHBoxLayout()

        btn_delete = QPushButton("Supprimer")
        btn_delete.clicked.connect(self.delete_selected)
        action_layout.addWidget(btn_delete)

        btn_modify = QPushButton("Modifier")
        btn_modify.clicked.connect(self.load_modify_dialog)
        action_layout.addWidget(btn_modify)

        btn_export = QPushButton("Exporter PDF")
        btn_export.clicked.connect(self.export_pdf)
        action_layout.addWidget(btn_export)

        layout.addLayout(action_layout)

        # -------------------- TOTALS --------------------
        self.totals_label = QLabel("")
        layout.addWidget(self.totals_label)

        # -------------------- FORMULAIRE AJOUT --------------------
        form_layout = QFormLayout()

        self.designation_input = QLineEdit()
        self.montant_input = QLineEdit()
        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.form_branch = QComboBox()
        self.load_form_branch()

        form_layout.addRow("Designation:", self.designation_input)
        form_layout.addRow("Montant:", self.montant_input)
        form_layout.addRow("Date:", self.date_input)
        form_layout.addRow("Branche:", self.form_branch)

        btn_add_entree = QPushButton("Ajouter entrée")
        btn_add_depense = QPushButton("Ajouter dépense")

        btn_add_entree.clicked.connect(self.on_add_entree)
        btn_add_depense.clicked.connect(self.on_add_depense)

        form_layout.addRow(btn_add_entree, btn_add_depense)
        layout.addLayout(form_layout)

        self.setLayout(layout)

        self.branch_combo.currentIndexChanged.connect(self.refresh_global_view)
        self.year_spin.valueChanged.connect(self.refresh_global_view)
        self.month_combo.currentIndexChanged.connect(self.refresh_global_view)

        self.refresh_global_view()

    # ----------------------------------------------------------------------
    def load_branch_combobox(self):
        self.branch_combo.clear()
        self.branch_combo.addItem("Toute l'église", None)
        for b in list_branches():
            self.branch_combo.addItem(b["nom"], b["id"])

    def load_form_branch(self):
        self.form_branch.clear()
        for b in list_branches():
            self.form_branch.addItem(b["nom"], b["id"])

    # ----------------------------------------------------------------------
    def refresh_global_view(self):
        id_branche = self.branch_combo.currentData()
        year = self.year_spin.value()
        month = self.month_combo.currentData()

        entrees, depenses = get_global_view(id_branche, year, month)

        self.current_view_all = []

        for e in entrees:
            self.current_view_all.append({
                "type": "Entrée",
                "id": e["id"],
                "designation": e["designation"],
                "montant": e["montant"],
                "date": e["date_entre"],
                "branche_nom": e["branche_nom"],
                "id_branche": e["id_branche"]
            })

        for d in depenses:
            self.current_view_all.append({
                "type": "Dépense",
                "id": d["id"],
                "designation": d["designation"],
                "montant": d["montant"],
                "date": d["date_sortie"],
                "branche_nom": d["branche_nom"],
                "id_branche": d["id_branche"]
            })

        # TABLE
        self.table.setRowCount(0)
        for item in self.current_view_all:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(item["type"]))
            self.table.setItem(row, 1, QTableWidgetItem(item["designation"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(item["montant"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(item["date"])))
            self.table.setItem(row, 4, QTableWidgetItem(item["branche_nom"]))

        # TOTALS
        total_e = sum(e["montant"] for e in entrees)
        total_d = sum(d["montant"] for d in depenses)
        solde = total_e - total_d

        self.totals_label.setText(
            f"Total Entrées: {total_e}  -  Total Dépenses: {total_d}  -  Solde: {solde}"
        )

    # ----------------------------------------------------------------------
    def delete_selected(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.current_view_all):
            QMessageBox.warning(self, "Erreur", "Aucune ligne sélectionnée ou invalide.")
            return

        item = self.current_view_all[row]

        confirm = QMessageBox.question(
            self, "Confirmer", f"Supprimer : {item['designation']} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        if item["type"] == "Entrée":
            delete_entree(item["id"])
        else:
            delete_depense(item["id"])

        self.refresh_global_view()

    # ----------------------------------------------------------------------
    def load_modify_dialog(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.current_view_all):
            QMessageBox.warning(self, "Erreur", "Aucune ligne sélectionnée ou invalide.")
            return

        item = self.current_view_all[row]
        branches = list_branches()

        dlg = ModifyDialog(
            item,
            branches,
            lambda newdata: self.save_modification(item, newdata)
        )
        dlg.exec()

    # ----------------------------------------------------------------------
    def save_modification(self, old_item, newdata):
        if old_item["type"] == "Entrée":
            update_entree(old_item["id"], newdata["designation"], newdata["montant"], newdata["date"], newdata["id_branche"])
        else:
            update_depense(old_item["id"], newdata["designation"], newdata["montant"], newdata["date"], newdata["id_branche"])

        QMessageBox.information(self, "Succès", "Modification enregistrée.")
        self.refresh_global_view()

    # ----------------------------------------------------------------------
    def on_add_entree(self):
        try:
            montant = float(self.montant_input.text())
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Montant invalide")
            return

        add_entree(
            self.designation_input.text(),
            montant,
            self.date_input.date().toPyDate(),
            self.form_branch.currentData()
        )
        self.refresh_global_view()

    def on_add_depense(self):
        try:
            montant = float(self.montant_input.text())
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Montant invalide")
            return

        add_depense(
            self.designation_input.text(),
            montant,
            self.date_input.date().toPyDate(),
            self.form_branch.currentData()
        )
        self.refresh_global_view()

    # ----------------------------------------------------------------------
    def export_pdf(self):
        id_branche = self.branch_combo.currentData()
        year = self.year_spin.value()
        month = self.month_combo.currentData()
        entrees, depenses = get_global_view(id_branche, year, month)

        path, _ = QFileDialog.getSaveFileName(self, "Exporter en PDF", "export.pdf", "PDF Files (*.pdf)")
        if not path:
            return

        export_global_to_pdf(entrees, depenses, path)
        QMessageBox.information(self, "Export PDF", f"Export terminé : {path}")


def main():
    init_db()
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

