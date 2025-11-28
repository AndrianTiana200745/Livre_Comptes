from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Branche:
    id: Optional[int]
    nom: str

@dataclass
class Entree:
    id: Optional[int]
    designation: str
    montant: float
    date_entre: date
    id_branche: int

@dataclass
class Depense:
    id: Optional[int]
    designation: str
    montant: float
    date_sortie: date
    id_branche: int

@dataclass
class User:
    id: Optional[int]
    nom: str
    prenom: str
    nomUtilisateur: str
    motDePasse: str
    numTelephone: str
    adresse: str
    role: str

