import sqlite3

def creer_tables():
    """Creer les tables si elles n'existent pas"""
    try:
        # connexion a la BDD (création si elle n'existe pas)
        connexion = sqlite3.connect("alesc.sqlite")
        curseur = connexion.cursor()

        # script de creation de la table logeur
        requete_logeur = f'''CREATE TABLE IF NOT EXISTS logeur (
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               nom TEXT NOT NULL ,
               prenom TEXT  NOT NULL,
               numero_rue TEXT  ,
               nom_rue TEXT  ,
               code_postal TEXT  ,
               ville TEXT )'''
        curseur.execute(requete_logeur)

        requete_etudiant = f'''CREATE TABLE IF NOT EXISTS etudiant (
                       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                       nom TEXT NOT NULL ,
                       prenom TEXT  NOT NULL,
                       semestre TEXT,
                       numero_rue TEXT  ,
                       nom_rue TEXT  ,
                       code_postal TEXT  ,
                       ville TEXT,
                       logement_id int not null,
                       FOREIGN KEY (logement_id) REFERENCES logement(id))'''
        curseur.execute(requete_etudiant)

        requete_logement = f'''CREATE TABLE IF NOT EXISTS logement (
                               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                               type  TEXT,
                               labellisation INTEGER,
                               numero_rue TEXT  ,
                               nom_rue TEXT  ,
                               code_postal TEXT  ,
                               ville TEXT,
                               logeur_id INTEGER NOT NULL ,
                               FOREIGN KEY(logeur_id) REFERENCES logeur(id))'''
        curseur.execute(requete_logement)

        connexion.commit()

    except FileNotFoundError:
        print("fichier inexistant")
    finally:
        if connexion:
            curseur.close()
            connexion.close()
            print("tables créés avec succes !")


if __name__ == '__main__':
    creer_tables()



