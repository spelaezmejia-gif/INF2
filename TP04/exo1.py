import math
import os
def extraire_pi():
    """Nettoyage des élements de ponctuation"""
    with open('poeme.txt') as f:
        contenu = f.read()
        texte_nettoye = contenu.replace(",", " ").replace(".", " ").replace("'", " ") \
            .replace("?", " ").replace("!", " ").replace("\n", " ")

        """Sauvegarde des mots sans ponctuation dans des chaines de caractères individuelles"""
        mots = texte_nettoye.split(" ")

        mots_propres=[]
        """Nettoyage des mots vides qui peuvent alterer le programme"""
        for m in mots:
            if m != "":
                mots_propres.append(m)
        pi = float(0)
        i = 0
        """Écriture de pi en utilisant les puissances de 10"""
        for m in mots_propres:
            pi += float(len(m)%10) * (10.0 ** float(i))
            i -= 1

    return (pi)
def creer_fichier_pi():
    """Création du fichier qui va contenir pi"""
    with open('pi.txt','x'):
        pass


def ecrire_pi():
    """Écriture de pi dans le fichier crée"""
    with open("pi.txt",'w') as f:
        f.write(str(extraire_pi()))


def main():
    print(os.getcwd())
    print(f"Valeur calculé : {extraire_pi()}")
    print(f"Valeur importé : {math.pi}")
    print(extraire_pi()==math.pi)
    creer_fichier_pi()
    ecrire_pi()


if __name__ == '__main__':
    main()
