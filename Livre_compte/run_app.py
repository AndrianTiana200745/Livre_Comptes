import sys
from pathlib import Path
# Ajoute la racine du projet au PYTHONPATH pour permettre les imports de package
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# lance le module comme package
import runpy
runpy.run_module("Livre_compte.view.main_window", run_name="__main__")

