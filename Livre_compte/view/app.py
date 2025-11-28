import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt

from Livre_compte.view.branche_window import BrancheWindow
from Livre_compte.view.main_window import MainWindow
from Livre_compte.view.user_window import UserWindow
from Livre_compte.utils.path import resource_path


class AppWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()

        # Convertir sqlite3.Row en dict si nécessaire
        if not isinstance(current_user, dict):
            current_user = dict(current_user)

        self.current_user = current_user

        self.setWindowTitle(f"Livre de Compte - Menu Principal ({self.current_user['nomUtilisateur']})")
        self.setWindowIcon(QIcon(resource_path("assets/ico.png")))
        self.setMinimumSize(400, 300)

        self.branche_window = None
        self.main_window = None
        self.user_window = None    # <-- AJOUT

        layout = QVBoxLayout()

        # --- Titre ---
        title = QLabel("Menu Principal")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # --- Boutons ---
        self.btn_branche = QPushButton("Gérer les Branches")
        self.btn_branche.clicked.connect(self.open_branche_window)
        layout.addWidget(self.btn_branche)

        self.btn_main = QPushButton("Gérer le Livre de Compte")
        self.btn_main.clicked.connect(self.open_main_window)
        layout.addWidget(self.btn_main)

        # --- BOUTON POUR GÉRER LES UTILISATEURS ---
        self.btn_user = QPushButton("Gérer les Utilisateurs")
        self.btn_user.clicked.connect(self.open_user_window)
        layout.addWidget(self.btn_user)

        btn_logout = QPushButton("Déconnexion")
        btn_logout.clicked.connect(self.logout)
        layout.addWidget(btn_logout)

        self.setLayout(layout)

        # Appliquer les permissions selon le rôle
        self.apply_permissions()

    # --------------------------
    # Permissions selon le rôle
    # --------------------------
    def apply_permissions(self):
        role = self.current_user.get("role", "user")

        if role == "admin":
            self.btn_branche.setEnabled(True)
            self.btn_main.setEnabled(True)
            self.btn_user.setEnabled(True)  # <-- AJOUT
        else:
            # Un user simple ne peut pas gérer les branches ni les utilisateurs
            self.btn_branche.setEnabled(False)
            self.btn_user.setEnabled(False)
            self.btn_main.setEnabled(True)

    # --------------------------
    # Ouverture des fenêtres
    # --------------------------
    def open_branche_window(self):
        self.branche_window = BrancheWindow()
        self.branche_window.show()

    def open_main_window(self):
        self.main_window = MainWindow(current_user=self.current_user)
        self.main_window.show()

    def open_user_window(self):
        self.user_window = UserWindow()
        self.user_window.show()

    def logout(self):
        from Livre_compte.view.login_window import LoginWindow

        for w in (self.branche_window, self.main_window, self.user_window):
            if w:
                w.close()

        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    fake_user = {"nomUtilisateur": "adminTest", "role": "admin"}
    window = AppWindow(current_user=fake_user)
    window.show()

    sys.exit(app.exec())

