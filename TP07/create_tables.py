import sqlite3
import pandas as pd
import numpy as np


def creer_tables():
    """Crée les tables de la base de données ALESC [cite: 1]"""
    connexion = sqlite3.connect("alesc.sqlite")
    curseur = connexion.cursor()

    # Table Logeur
    curseur.execute('''CREATE TABLE IF NOT EXISTS logeur (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          nom TEXT NOT NULL,
                                                          prenom TEXT NOT NULL,
                                                          numero_rue TEXT,
                                                          nom_rue TEXT,
                                                          code_postal TEXT,
                                                          ville TEXT)''')


    # Table logement
    curseur.execute('''CREATE TABLE IF NOT EXISTS logement (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            numero_rue TEXT,
                                                            nom_rue TEXT,
                                                            code_postal TEXT,
                                                            ville TEXT,
                                                            labellisation TEXT,
                                                            nom_logeur TEXT,
                                                            prenom_logeur TEXT,
                                                            type_logement TEXT,
                                                            logeur_id INTEGER NOT NULL,
                                                            FOREIGN KEY (logeur_id) REFERENCES logeur (id))''')


    # Table Etudiant
    curseur.execute('''CREATE TABLE IF NOT EXISTS etudiant (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                             nom TEXT NOT NULL,
                                                             prenom TEXT NOT NULL,
                                                             semestre TEXT,
                                                             numero_rue TEXT,
                                                             nom_rue TEXT,
                                                             code_postal TEXT,
                                                             ville TEXT,
                                                             logement_id INTEGER NOT NULL,
                                                             FOREIGN KEY (logement_id) REFERENCES logement(id))''')


    connexion.commit()
    connexion.close()
    print("Structure SQLite créée avec succès.")



def peupler_tables(file_logeurs, file_logements, file_etudiants):
    connexion = sqlite3.connect("alesc.sqlite")
    curseur = connexion.cursor()
    try:
        # 1. TRAITEMENT DES LOGEURS
        df_logeurs = pd.read_excel(file_logeurs)

        # Sélection des colonnes pour correspondre au INSERT
        cols_logeurs = ['nom', 'prenom', 'numero_rue', 'nom_rue', 'code_postal', 'ville']
        matrice_logeurs = df_logeurs[cols_logeurs].to_numpy()

        curseur.executemany(
            "INSERT INTO logeur (nom, prenom, numero_rue, nom_rue, code_postal, ville) VALUES (?, ?, ?, ?, ?, ?)",
            matrice_logeurs.tolist()
        )
        connexion.commit()
        print(f"Logeurs importés : {len(matrice_logeurs)}")
        # 2. TRAITEMENT DES LOGEMENTS
        df_logements = pd.read_excel(file_logements)

        # On doit récupérer les IDs générés dans la BDD pour les associer.
        df_db_logeurs = pd.read_sql("SELECT id as logeur_id, nom, prenom FROM logeur", connexion)

        # On joint le fichier Excel avec la BDD sur le nom et prénom
        df_logements_complet = df_logements.merge(df_db_logeurs, left_on=['nom_logeur', 'prenom_logeur'],
                                                  right_on=['nom', 'prenom'])

        # On prépare la matrice avec l'ID trouvé
        cols_logements = ['type_logement', 'label', 'numero_rue', 'nom_rue', 'code_postal', 'ville', 'logeur_id']
        matrice_logements = df_logements_complet[cols_logements].to_numpy()

        curseur.executemany(
            "INSERT INTO logement (type_logement, labellisation, numero_rue, nom_rue, code_postal, ville, logeur_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            matrice_logements.tolist()
        )
        connexion.commit()
        print(f"Logements importés : {len(matrice_logements)}")

        # 3. TRAITEMENT DES ÉTUDIANTS

        df_etudiants = pd.read_excel(file_etudiants)

        # On récupère les IDs des logements via l'adresse
        df_db_logements = pd.read_sql("SELECT id as logement_id, numero_rue, nom_rue, code_postal FROM logement",
                                      connexion)

        # On force le type string pour éviter les erreurs de jointure (15 vs "15")
        for col in ['numero_rue', 'nom_rue', 'code_postal']:
            df_etudiants[col] = df_etudiants[col].astype(str).str.strip()
            df_db_logements[col] = df_db_logements[col].astype(str).str.strip()

        # On joint le fichier étudiant avec la BDD sur l'adresse
        df_etudiants_complet = df_etudiants.merge(df_db_logements, on=['numero_rue', 'nom_rue', 'code_postal'])

        cols_etudiants = ['nom', 'prenom', 'semestre', 'numero_rue', 'nom_rue', 'code_postal', 'ville', 'logement_id']
        matrice_etudiants = df_etudiants_complet[cols_etudiants].to_numpy()

        curseur.executemany(
            "INSERT INTO etudiant (nom, prenom, semestre, numero_rue, nom_rue, code_postal, ville, logement_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            matrice_etudiants.tolist()
        )
        connexion.commit()
        print(f"Étudiants importés : {len(matrice_etudiants)}")

    except Exception as e:
        print(f"Erreur d'importation : {e}")
    finally:
        if connexion:
            connexion.close()


def verifier_donnees():
    """Affiche le résultat de la jointure pour vérifier le lien"""
    connexion = sqlite3.connect("alesc.sqlite")
    curseur = connexion.cursor()

    requete = '''
              SELECT etudiant.nom, logement.type_logement, logeur.nom
              FROM etudiant
                       JOIN logement ON etudiant.logement_id = logement.id
                       JOIN logeur ON logement.logeur_id = logeur.id LIMIT 5 \
              '''
    curseur.execute(requete)
    results = curseur.fetchall()
    print("\n--- Vérification des liens ---")
    for res in results:
        print(f"Succès : L'étudiant {res[0]} occupe un(e) {res[1]} géré(e) par {res[2]}.")
    connexion.close()


def main():
    creer_tables()
    peupler_tables("logeurs.xlsx", "logements.xlsx", "etudiants.xlsx")
    verifier_donnees()


if __name__ == '__main__':
    main()