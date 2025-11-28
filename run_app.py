from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet
import sys
from Livre_compte.view.login_window import LoginWindow
from Livre_compte.database.init_db import initialize_database
from Livre_compte.controller.branche_controller import init_main_branche
from Livre_compte.model.user_model import UserModel



def main():
    initialize_database()
    admin_created = UserModel().create_default_admin()
    init_main_branche()

    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')

    login = LoginWindow()
    login.show()

    # ➜ Afficher un message si admin créé
    if admin_created:
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("Information")
        msg.setText("Un administrateur par défaut a été créé.\n\nIdentifiant : admin\nMot de passe : admin123")
        msg.exec()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

