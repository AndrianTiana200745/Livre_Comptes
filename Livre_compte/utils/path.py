import sys, os

def resource_path(relative_path):
    """Permet d’accéder aux fichiers en mode normal ou PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(".")

    return os.path.join(base, relative_path)

