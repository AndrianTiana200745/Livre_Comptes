# Livre_compte/controller/user_controller.py
from Livre_compte.model.user_model import UserModel

class UserController:
    def __init__(self):
        self.model = UserModel()

    def register(self, nom, prenom, mdp, tel="", adresse="", role="user"):
        return self.model.create_user(nom, prenom, mdp, tel, adresse, role)

    def login(self, identifiant, mdp):
        return self.model.auth(identifiant, mdp)

