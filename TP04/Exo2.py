import csv
#creation de la classe etudiant
class Etudiant:
    def __init__(self,nom,a,gpa,connais_python):
        """Initialise un objet étudiant avec un nom type str, une année de naissance de type entier,
        un gpa de type float et un booléen qui décrit si l'étudiant connait python"""
        self._nom=nom
        self._annee_naissance = a
        self._gpa = gpa
        self._connais_python = connais_python

    @property
    def nom(self):
        return self._nom

    @property
    def annee_naissance(self):
        return self._annee_naissance

    @property
    def gpa(self):
        return self._gpa

    @property
    def connais_python(self):
        return self._connais_python
#setters et getters
    @nom.setter
    def nom(self,nom):
        if isinstance(nom,str):
            self._nom = nom

    @nom.getter
    def nom(self):
        return self._nom

    @annee_naissance.setter
    def annee_naissance(self,a):
        if isinstance(a,int):
            self._annee_naissance = a

    @annee_naissance.getter
    def annee_naissance(self):
        return self._annee_naissance

    @gpa.setter
    def gpa(self,gpa):
        if isinstance(gpa,float):
            self._gpa = gpa

    @gpa.getter
    def gpa(self):
        return self._gpa

    @connais_python.setter
    def connais_python(self,connais_python):
        if isinstance(connais_python, bool):
            self._connais_python = connais_python

    @connais_python.getter
    def connais_python(self):
        return self._connais_python
#fomctions
    def to_dict(self):
        """Transforme l'objet étudiant dans un dictionnaire"""
        etudico={}
        etudico["nom"]=self.nom
        etudico["annee_naissance"]=self.annee_naissance
        etudico["gpa"]=self.gpa
        etudico["connais_python"]=self.connais_python
        return etudico
#methode de classe
    @classmethod
    def from_dict(cls, d):
        """Crée un étudiant depuis un dictionnaire."""
        return cls(d["nom"], int(d["annee_naissance"]), float(d["gpa"]), bool(d["connais_python"]))

#Creation de la classe groupe
class Groupe:
    def __init__(self):
        """Initialise la liste d'étudiants."""
        self._etudiants=[]
#fonctions
    def ajouter_etudiant(self,etudiant):
        """Ajoute un étudiant au groupe."""
        if isinstance(etudiant,Etudiant):
            self._etudiants.append(etudiant)

    def sauvegarder_csv(self, nom_fichier):
        """Sauvegarde les étudiants dans un fichier CSV."""
        if not self._etudiants:
            print("Aucun étudiant.")
            return

        champs = list(self._etudiants[0].to_dict().keys())

        with open(nom_fichier, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=champs)
            writer.writeheader()
            for etu in self._etudiants:
                writer.writerow(etu.to_dict())
#methode de classe
    @classmethod
    def charger_csv(cls, nom_fichier):
        """Charge un groupe depuis un CSV."""
        groupe = cls()
        with open(nom_fichier, "r", encoding="utf-8") as f:
            for ligne in csv.DictReader(f):
                groupe.ajouter_etudiant(Etudiant.from_dict(ligne))
        return groupe
def main():
    e1 = Etudiant("Yasmin", 2003, 3.8, True)
    e2 = Etudiant("Samuel", 2002, 3.5, False)
    e3 = Etudiant("Camille", 2000, 3.9, True)
    e4 = Etudiant("Lucas", 2003, 3.2, False)
    e5 = Etudiant("Élodie", 2002, 3.7, True)

    groupe = Groupe()
    groupe.ajouter_etudiant(e1)
    groupe.ajouter_etudiant(e2)
    groupe.ajouter_etudiant(e3)
    groupe.ajouter_etudiant(e4)
    groupe.ajouter_etudiant(e5)

    groupe.sauvegarder_csv("etudiants.csv")
    groupe2 = Groupe.charger_csv("etudiants.csv")

    for etu in groupe2._etudiants:
        print(etu.to_dict())


if __name__ == "__main__":
    main()
