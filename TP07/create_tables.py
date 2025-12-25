import sqlite3
import pandas as pd
import numpy as np


def creer_tables():
    """Crée les tables de la base de données ALESC [cite: 1]"""
    connexion = sqlite3.connect("alesc.sqlite")
    curseur = connexion.cursor()

    # Table Logeurs
    curseur.execute('''CREATE TABLE IF NOT EXISTS logeurs (nom TEXT NOT NULL,
                                                          prenom TEXT NOT NULL,
                                                          numero_rue TEXT,
                                                          nom_rue TEXT,
                                                          code_postal TEXT,
                                                          ville TEXT,
                                                          id INTEGER PRIMARY KEY AUTOINCREMENT)''')

    # Table logements
    curseur.execute('''CREATE TABLE IF NOT EXISTS logements (numero_rue TEXT,
                                                            nom_rue TEXT,
                                                            code_postal TEXT,
                                                            ville TEXT,
                                                            label TEXT,
                                                            nom_logeur TEXT,
                                                            prenom_logeur TEXT,
                                                            type_logement TEXT,
                                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            logeur_id INTEGER NOT NULL,
                                                            FOREIGN KEY (logeur_id) REFERENCES logeur (id))''')

    # Table Etudiants
    curseur.execute('''CREATE TABLE IF NOT EXISTS etudiants (nom TEXT NOT NULL,
                                                             prenom TEXT NOT NULL,
                                                             semestre TEXT,
                                                             numero_rue TEXT,
                                                             nom_rue TEXT,
                                                             code_postal TEXT,
                                                             ville TEXT,
                                                             id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                             logement_id INTEGER NOT NULL,
                                                             FOREIGN KEY (logement_id) REFERENCES logement(id))''')

    connexion.commit()
    connexion.close()
    print("Structure SQLite créée avec succès.")
def conv_excel_to_numpy(file):
    F=pd.read_excel(file)
    F.to_numpy()
    return F

def peupler_base_numpy(Matrice1,Matrice2,Matrice3):
    """Importe les données via des matrices NumPy"""
    connexion = sqlite3.connect("alesc.sqlite")
    curseur = connexion.cursor()
    liste_de_valeurs_1 = [tuple(f) for f in Matrice1]
    liste_de_valeurs_2= [tuple(f) for f in Matrice2]
    liste_de_valeurs_3= [tuple(f) for f in Matrice3]


    instruction1 = f"INSERT INTO logeurs VALUES(?,?,?,?,?,?)"
    instruction2 = f"INSERT INTO logements VALUES(?,?,?,?,?,?,?,?)"
    instruction3 = f"INSERT INTO etudiants VALUES(?,?,?,?,?,?,?)"

    curseur.executemany(instruction1,liste_de_valeurs_1)
    curseur.executemany(instruction2, liste_de_valeurs_2)
    curseur.executemany(instruction3, liste_de_valeurs_3)

    connexion.commit()
    connexion.close()


def main():
    creer_tables()
    Matrice1 = conv_excel_to_numpy("logeurs.xlsx")
    Matrice2 = conv_excel_to_numpy("logements.xlsx")
    Matrice3 = conv_excel_to_numpy("etudiants.xlsx")
    peupler_base_numpy(Matrice1,Matrice2,Matrice3)


if __name__ == '__main__':
    main()