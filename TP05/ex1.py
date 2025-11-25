import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt

def charge_temperatures(ficher: str) -> np.ndarray:
    """Charge le fichier .npy."""
    return np.load(ficher)

def afficher_coubers(reel: np.ndarray, estime: np.ndarray) -> None:
    """Affiche les courbes de température réelle et estimée"""
    plt.plot(reel, color="crimson", label='Température réelle')
    plt.plot(estime, color="royalblue", label='Température estimée')
    plt.xlabel("Indice")
    plt.ylabel("Température")
    plt.legend()
    plt.title("Température réelle et estimée")
    plt.grid(True)
    plt.show()

def temperature_estimee(mesure: np.ndarray) -> np.ndarray:
    """Calcule la température estimée"""
    return 10 * mesure - 10

def erreur(reel: np.ndarray, estime: np.ndarray) -> np.ndarray:
    """Renvoie l’erreur entre la température estimée et la température réelle"""
    return estime - reel

def afficher_histogramme(erreur: np.ndarray) -> None:
    """Affiche l’histogramme des erreurs de température"""
    plt.hist(erreur, bins=15, color='mediumorchid', edgecolor='indigo')
    plt.xlabel("Erreur (°C)")
    plt.ylabel("Fréquence")
    plt.title("Histogramme des erreurs")
    plt.grid(True)
    plt.show()

def calculer_rmse(reel: np.ndarray, estime: np.ndarray) -> float:
    """Calcule la RMSE entre les températures réelle et estimée"""
    return float(np.sqrt(np.mean((reel - estime) ** 2)))

def lisser_tension(mesure: np.ndarray, taille: int = 5) -> np.ndarray:
    """Lisse la tension mesurée avec un filtre médian"""
    return medfilt(mesure, kernel_size=taille)

def afficher_erreurs(erreur: np.ndarray, lissee: np.ndarray) -> None:
    """Affiche les histogrammes des erreurs brute et lissée"""
    plt.hist(erreur,
             bins=15,
             alpha=0.5,
             edgecolor="black",
             color="lightgreen",
             label="Erreur brute")
    plt.hist(lissee,
             bins=15,
             alpha=0.5,
             edgecolor="black",
             label="Erreur lissée")

    plt.xlabel("Erreur")
    plt.ylabel("Fréquence")
    plt.title("Histogrammes des erreurs de température")
    plt.legend()
    plt.grid(True)
    plt.show()

def afficher_courbes_filtrage(reel: np.ndarray, mesure: np.ndarray, filtre: np.ndarray) -> None:
    """Affiche les courbes réelle, mesurée et filtrée sur un même graphique"""
    plt.plot(reel, label="Réelle", color="blue")
    plt.plot(mesure, label="Mesurée", color="green")
    plt.plot(filtre, label="Filtrée", color="orange")
    plt.xlabel("Indice")
    plt.ylabel("Température")
    plt.title("Températures")
    plt.legend()
    plt.grid(True)
    plt.show()

def main() -> None:
    # Question 1
    temp = charge_temperatures("temperatures.npy")

    # Question 2
    reel = temp[:, 0]
    mesure = temp[:, 1]
    estime = temperature_estimee(mesure)
    afficher_coubers(reel, estime)

    # Question 3
    erreurs_brutes = erreur(reel, estime)
    afficher_histogramme(erreurs_brutes)

    # Question 4
    rmse = calculer_rmse(reel, estime)
    print(f"RMSE : {rmse:.3f}")

    # Question 5
    lissee = lisser_tension(mesure)

    # Question 6
    filtre = temperature_estimee(lissee)
    erreurs_lissees = erreur(reel, filtre)
    afficher_erreurs(erreurs_brutes, erreurs_lissees)
    afficher_courbes_filtrage(reel, mesure, filtre)

if __name__ == "__main__":
    main()
