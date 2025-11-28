# Livre_compte/view/register_window.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from PyQt6.QtCore import Qt
from Livre_compte.controller.user_controller import UserController

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Créer un compte")
        self.setMinimumSize(400, 380)

        self.controller = UserController()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Créer un compte utilisateur")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.nom = QLineEdit(); self.nom.setPlaceholderText("Nom")
        self.prenom = QLineEdit(); self.prenom.setPlaceholderText("Prénom")
        self.mdp = QLineEdit(); self.mdp.setPlaceholderText("Mot de passe"); self.mdp.setEchoMode(QLineEdit.EchoMode.Password)
        self.tel = QLineEdit(); self.tel.setPlaceholderText("Téléphone")
        self.adresse = QLineEdit(); self.adresse.setPlaceholderText("Adresse")

        # Sélecteur de rôle
        self.role = QComboBox()
        self.role.addItems(["user"])

        layout.addWidget(self.nom)
        layout.addWidget(self.prenom)
        layout.addWidget(self.mdp)
        layout.addWidget(self.tel)
        layout.addWidget(self.adresse)
        layout.addWidget(QLabel("Rôle :"))
        layout.addWidget(self.role)

        btn = QPushButton("Créer le compte")
        btn.clicked.connect(self.register)
        layout.addWidget(btn)

        self.setLayout(layout)

    def register(self):
        if not self.nom.text() or not self.prenom.text() or not self.mdp.text():
            QMessageBox.warning(self, "Erreur", "Veuillez remplir les champs obligatoires.")
            return

        identifiant = self.controller.register(
            self.nom.text(),
            self.prenom.text(),
            self.mdp.text(),
            self.tel.text(),
            self.adresse.text(),
            self.role.currentText()
        )

        QMessageBox.information(self, "Compte créé",
            f"Compte créé avec succès !\nVotre identifiant est : {identifiant}")

        self.close()

