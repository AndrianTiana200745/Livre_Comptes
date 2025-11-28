-- database/init_db.sql
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS utilisateur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    nomUtilisateur TEXT NOT NULL UNIQUE,
    motDePasse TEXT NOT NULL,
    numTelephone TEXT,
    adresse TEXT,
    role TEXT NOT NULL DEFAULT 'user'   -- <== AJOUT DU ROLE
);

CREATE TABLE IF NOT EXISTS branche (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS argent_depense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    designation TEXT NOT NULL,
    montant REAL NOT NULL,
    date_sortie DATE NOT NULL,
    id_branche INTEGER NOT NULL,
    FOREIGN KEY(id_branche) REFERENCES branche(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS argent_entrer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    designation TEXT NOT NULL,
    montant REAL NOT NULL,
    date_entre DATE NOT NULL,
    id_branche INTEGER NOT NULL,
    FOREIGN KEY(id_branche) REFERENCES branche(id) ON DELETE CASCADE
);

