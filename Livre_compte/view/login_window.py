# Livre_compte/view/login_window.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from Livre_compte.controller.user_controller import UserController
from Livre_compte.view.app import AppWindow
from Livre_compte.view.register_window import RegisterWindow
from Livre_compte.utils.path import resource_path

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setWindowIcon(QIcon(resource_path("assets/ico.png")))
        self.setMinimumSize(350, 250)

        self.controller = UserController()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Connexion")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.identifiant = QLineEdit()
        self.identifiant.setPlaceholderText("Identifiant")
        self.mdp = QLineEdit()
        self.mdp.setEchoMode(QLineEdit.EchoMode.Password)
        self.mdp.setPlaceholderText("Mot de passe")

        layout.addWidget(self.identifiant)
        layout.addWidget(self.mdp)

        btn_login = QPushButton("Se connecter")
        btn_login.clicked.connect(self.login)
        layout.addWidget(btn_login)

        btn_register = QPushButton("Créer un compte")
        btn_register.clicked.connect(self.open_register)
        layout.addWidget(btn_register)

        self.setLayout(layout)

    def login(self):
        user = self.controller.login(self.identifiant.text(), self.mdp.text())
        if not user:
            QMessageBox.warning(self, "Erreur", "Identifiant ou mot de passe incorrect.")
            return

        self.open_app(user)

    def open_app(self, user):
        user = dict(user)
        self.app = AppWindow(current_user=user)
        self.app.show()
        self.close()

    def open_register(self):
        self.reg = RegisterWindow()
        self.reg.show()

