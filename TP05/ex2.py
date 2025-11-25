import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

def charger_et_afficher_image(path: str) -> np.ndarray:
    """Charge l'image RGB et l'affiche"""
    image = plt.imread(path)
    plt.figure()
    plt.imshow(image)
    plt.title("Image originale")
    plt.axis("off")
    return image

def convertir_rgb_normalise(image: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Normalise l'image dans [0,1] et renvoie R,G,B"""
    image_norm = image.astype(np.float32) / 255.0
    R = image_norm[:, :, 0]
    G = image_norm[:, :, 1]
    B = image_norm[:, :, 2]
    return image_norm, R, G, B

def rgb_to_hsv(R: np.ndarray, G: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Convertit une image RGB normalisée en HSV"""
    Cmin = np.min(np.dstack((R, G, B)), axis=2)
    Cmax = np.max(np.dstack((R, G, B)), axis=2)
    delta = Cmax - Cmin

    V = Cmax

    cond1 = (Cmax == 0)
    cond2 = (Cmax != 0)
    S = np.select([cond1, cond2], [0, delta / Cmax], default=0)

    cond_delta0 = (delta == 0)
    cond_r = (Cmax == R)
    cond_g = (Cmax == G)
    cond_b = (Cmax == B)

    choix_delta0 = 0
    choix_r = ((G - B) / delta) % 6
    choix_g = ((B - R) / delta) + 2
    choix_b = ((R - G) / delta) + 4

    H = np.select([cond_delta0, cond_r, cond_g, cond_b],
                  [choix_delta0, choix_r, choix_g, choix_b],
                  default=0)
    H = H / 6.0
    image_hsv = np.dstack((H, S, V))
    return image_hsv

def afficher_image_hsv_reconstruite(image_hsv: np.ndarray):
    """Affiche l'image HSV reconvertie en RGB pour vérification"""
    image_rgb = colors.hsv_to_rgb(image_hsv)
    plt.figure()
    plt.imshow(image_rgb)
    plt.title("Image reconstruite")
    plt.axis("off")
    plt.show()


def afficher_canaux_hsv(image_hsv: np.ndarray):
    """Affiche séparément les canaux H, S, V avec des colorbars"""
    H = image_hsv[:, :, 0]
    S = image_hsv[:, :, 1]
    V = image_hsv[:, :, 2]

    plt.figure(figsize=(15, 4))

    plt.subplot(131)
    im_h = plt.imshow(H, cmap='hsv')
    plt.colorbar(im_h)
    plt.title('H')

    plt.subplot(132)
    im_s = plt.imshow(S, cmap='gray')
    plt.colorbar(im_s)
    plt.title('S')

    plt.subplot(133)
    im_v = plt.imshow(V, cmap='gray')
    plt.colorbar(im_v)
    plt.title('V')
    plt.show()
    return H, S, V

def creer_masque(H, S, V):
    """Crée un masque pour isoler la carrosserie"""
    masque = (H > 0.525) & (H < 0.75) & (S > 0.3) & (V > 0.3)
    plt.figure()
    plt.imshow(masque, cmap="gray")
    plt.title("Masque")
    plt.axis("off")
    plt.show()
    return masque


def recolorer(image_hsv: np.ndarray, masque: np.ndarray) -> np.ndarray:
    """Change la teinte de la voiture en rouge"""
    image_modifiee = image_hsv.copy()
    image_modifiee[:, :, 0][masque] = 0.05  # teinte rouge
    image_rgb = colors.hsv_to_rgb(image_modifiee)
    plt.figure()
    plt.imshow(image_rgb)
    plt.title("Voiture recolorée")
    plt.axis("off")
    plt.show()
    return image_rgb


def main():
    # Charger l'image
    image = charger_et_afficher_image("citroen.jpg")

    # Normaliser + séparer les canaux
    image_norm, R, G, B = convertir_rgb_normalise(image)

    # Convertir RGB → HSV
    image_hsv = rgb_to_hsv(R, G, B)

    # Vérification
    afficher_image_hsv_reconstruite(image_hsv)

    # Afficher les canaux séparés pour décider des seuils
    H, S, V = afficher_canaux_hsv(image_hsv)

    # Créer masque
    masque = creer_masque(H, S, V)

    # Appliquer recoloration
    recolorer(image_hsv, masque)

if __name__ == "__main__":
    main()
