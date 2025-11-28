# Livre Comptes

**Application de gestion comptable multi-branche, avec interface graphique (PyQt6) permettant la gestion d'entrées et de dépenses, le suivi des soldes par branche et l'exportation de la synthèse en PDF.**

## Table des matières

- [Description](#description)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Organisation du code](#organisation-du-code)
- [Contributeurs](#contributeurs)
- [Licence](#licence)

## Description

Livre_Comptes est une application desktop conçue pour faciliter la gestion des finances associatives, d’entreprises ou personnelles, multi-branche. Elle permet de gérer les entrées et sorties d’argent, d’organiser les opérations par branche, de consulter les soldes et d’exporter l’ensemble des mouvements au format PDF. Le projet repose sur Python (PyQt6 pour l’interface graphique), avec une base de données SQLite intégrée.

## Fonctionnalités

- **Authentification utilisateur** (incluant la création d’un compte admin par défaut lors de la première utilisation).
- **Gestion multi-branche** : Ajout, modification, suppression de branches.
- **Opérations financières** :
  - Ajout d’entrées (recettes)
  - Ajout de dépenses
  - Modification et suppression de chaque opération
- **Affichage synthétique** :
  - Tableau dynamique des mouvements (entrées/dépenses) filtrable par branche, année, mois.
  - Calcul automatique des soldes, totaux entrées, totaux dépenses.
- **Export PDF** :
  - Génération d’un rapport global exportable au format PDF.
- **Interface graphique moderne** : style matérial design via qt-material.

## Installation

### Prérequis

- **Python 3.10+** recommandé
- **pip** (gestionnaire de paquets Python)

### Installation des dépendances

Rendez-vous dans le dossier `Livre_compte/` puis lancez :

```bash
pip install -r requirement.txt
```

### Premier Lancement

Exécutez le fichier principal :

```bash
python run_app.py
```

Au premier lancement, un administrateur par défaut est créé :
- **Identifiant** : `admin`
- **Mot de passe** : `admin123`

## Utilisation

1. **Connexion** : Connectez-vous en tant qu’administrateur ou utilisateur.
2. **Gestion des branches** : Rendez-vous dans le module dédié pour créer/modifier/supprimer des branches.
3. **Ajout d’entrées/dépenses** : Saisir les opérations financières, avec désignation, montant, date et branche associée.
4. **Modification/Suppression** : Les opérations peuvent être modifiées ou supprimées via l’interface de synthèse.
5. **Synthèse et export** : Visualisez le bilan global par branche/période, puis exportez en PDF.

## Organisation du code

- **view/**
  - `main_window.py` : Fenêtre principale (gestion, affichage synthétique, export PDF)
  - `login_window.py` : Fenêtre de connexion
  - `branche_window.py` : Gestion des branches
- **controller/**
  - `finance_controller.py` : Logique métier des opérations (CRUD entrées/dépenses)
  - `branche_controller.py` : Gestion des branches (CRUD)
- **model/**
  - `user_model.py` : Logiciel de gestion des utilisateurs
- **database/**
  - `db.py` : Connexion et initialisation de la base SQLite
  - `init_db.sql` : Script de création des tables
- **utils/**
  - `export_pdf.py` : Utilitaires pour l’export PDF
- **run_app.py** : Point d’entrée principal de l’application

## Contributeurs

- **AndrianTiana200745** (https://github.com/AndrianTiana200745)

## Licence

Ce projet est ouvert sous licence MIT (sauf indication contraire).

---

N’hésitez pas à ouvrir des issues ou pull requests pour suggérer des améliorations ou reportez des bugs!
