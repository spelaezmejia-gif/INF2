import sqlite3
import pandas as pd
import numpy as np


def creer_tables():
    """Crée les tables de la base de données ALESC [cite: 1]"""
    connexion = sqlite3.connect("alesc.sqlite")
    curseur = connexion.cursor()

    # Table logeur (Responsable du logement) [cite: 14]
    curseur.execute('''CREATE TABLE IF NOT EXISTS logeur (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          nom TEXT NOT NULL,
                                                          prenom TEXT NOT NULL,
                                                          nom_rue TEXT,
                                                          code_postal TEXT,
                                                          ville TEXT)''')

    # Table logement (Type: chambre, studio, etc.) [cite: 7, 10]
    curseur.execute('''CREATE TABLE IF NOT EXISTS logement( id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            type TEXT,
                                                            labellisation INTEGER,
                                                            numero_rue TEXT,
                                                            nom_rue TEXT,
                                                            code_postal TEXT,
                                                            ville TEXT,
                                                            logeur_id INTEGER NOT NULL,
                                                            FOREIGN KEY (logeur_id) REFERENCES logeur (id))''')

    # Table etudiant (Ex: Ménan) [cite: 2]
    curseur.execute('''CREATE TABLE IF NOT EXISTS etudiant ( id INTEGER PRIMARY KEY AUTOINCREMENT, 
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


def peupler_base_numpy(file_lgr, file_lgm, file_etd):
    """Importe les données via des matrices NumPy [cite: 19, 20]"""
    connexion = sqlite3.connect("alesc.sqlite")
    curseur = connexion.cursor()

    try:
        # 1. TRAITEMENT DES LOGEURS
        df_lgr = pd.read_csv(file_lgr)
        # Conversion explicite en matrice NumPy pour l'insertion [cite: 20]
        matrice_lgr = np.array(df_lgr)
        curseur.executemany(
            "INSERT INTO logeur (nom, prenom, numero_rue, nom_rue, code_postal, ville) VALUES (?,?,?,?,?,?)",
            matrice_lgr.tolist()
        )
        connexion.commit()

        # 2. TRAITEMENT DES LOGEMENTS (Mapping Logeur -> Logement)
        df_lgm = pd.read_csv(file_lgm)
        # On récupère les IDs créés pour faire la liaison [cite: 5, 15]
        df_map_lgr = pd.read_sql("SELECT id as logeur_id, nom, prenom FROM logeur", connexion)

        # Jointure Pandas pour retrouver le logeur_id par le nom/prénom
        df_lgm_final = df_lgm.merge(df_map_lgr, left_on=['nom_logeur', 'prenom_logeur'], right_on=['nom', 'prenom'])

        # Sélection des colonnes et transformation en matrice NumPy
        selection_lgm = df_lgm_final[
            ['type_logement', 'label', 'numero_rue', 'nom_rue', 'code_postal', 'ville', 'logeur_id']]
        matrice_lgm = selection_lgm.to_numpy()

        curseur.executemany(
            "INSERT INTO logement (type, labellisation, numero_rue, nom_rue, code_postal, ville, logeur_id) VALUES (?,?,?,?,?,?,?)",
            matrice_lgm.tolist()
        )
        connexion.commit()

        # 3. TRAITEMENT DES ETUDIANTS (Mapping Logement -> Etudiant via l'adresse)
        df_etd = pd.read_csv(file_etd)
        # On récupère les IDs des logements pour l'affectation [cite: 4, 15]
        df_map_lgm = pd.read_sql("SELECT id as logement_id, numero_rue, nom_rue, code_postal FROM logement", connexion)

        # Jointure sur l'adresse (numero, rue, CP) pour identifier le logement
        df_etd_final = df_etd.merge(df_map_lgm, on=['numero_rue', 'nom_rue', 'code_postal'])

        # Matrice NumPy finale pour les étudiants (dont Ménan [cite: 2])
        selection_etd = df_etd_final[
            ['nom', 'prenom', 'semestre', 'numero_rue', 'nom_rue', 'code_postal', 'ville', 'logement_id']]
        matrice_etd = np.array(selection_etd)

        curseur.executemany(
            "INSERT INTO etudiant (nom, prenom, semestre, numero_rue, nom_rue, code_postal, ville, logement_id) VALUES (?,?,?,?,?,?,?,?)",
            matrice_etd.tolist()
        )
        connexion.commit()
        print(f"Importation terminée : {len(matrice_etd)} étudiants insérés.")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        connexion.close()


def verifier_coherence():
    """Vérifie que les liens entre tables existent bien"""
    connexion = sqlite3.connect("alesc.sqlite")
    df_verif = pd.read_sql('''
                           SELECT e.nom as Etudiant, l.type as Logement, o.nom as Logeur
                           FROM etudiant e
                                    JOIN logement l ON e.logement_id = l.id
                                    JOIN logeur o ON l.logeur_id = o.id LIMIT 5
                           ''', connexion)
    print("\n--- Aperçu des données liées ---")
    print(df_verif)
    connexion.close()


if __name__ == '__main__':
    # Fichiers sources détectés
    f1 = "logeurs.xlsx"
    f2 = "logements.xlsx"
    f3 = "etudiants.xlsx"

    creer_tables()
    peupler_base_numpy(f1, f2, f3)
    verifier_coherence()