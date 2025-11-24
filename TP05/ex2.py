import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np


def main():
    #charge et affichage de l'image
    image = plt.imread('citroen.jpg')
    plt.figure()
    plt.imshow(image)
    plt.show()
    # on normalise l'image
    image_norm = image.astype(np.float32) / 255.0
    R = image_norm[:, :, 0]
    G = image_norm[:, :, 1]
    B = image_norm[:, :, 2]
    # On calcule les paramètres pour le HSV
    Cmin = np.min(image_norm, axis=2)
    Cmax = np.max(image_norm, axis=2)
    delta = Cmax - Cmin
    V = Cmax
    #on calcule S
    cond1 = (Cmax == 0)
    cond2 = (Cmax != 0)
    condition = [cond1, cond2]
    choix1 = 0
    choix2 = delta / Cmax
    S = np.select(condition, [choix1, choix2], default=choix1)
    #on calcule H
    cond_delta0 = (delta == 0)
    cond_r = (Cmax == R)
    cond_g = (Cmax == G)
    cond_b = (Cmax == B)
    conditions = [cond_delta0, cond_r, cond_g, cond_b]
    choix_delta0 = 0
    choix_r = ((G - B) / delta) % 6
    choix_g = ((B - R) / delta) + 2
    choix_b = ((R - G) / delta) + 4
    choix = [choix_delta0, choix_r, choix_g, choix_b]
    H = np.select(conditions, choix, default=0)
    H = H / 6
    #on charge l'image en HSV en image_hsv
    image_hsv = np.dstack((H, S, V))
    #on affiche l'image pour voir que les valeurs soient bien calculés 
    image2 = colors.hsv_to_rgb(image_hsv)
    plt.figure()
    plt.imshow(image2)
    plt.show()
    #on sépare H, S et V pour déterminer les seuils
    H_im = image_hsv[:, :, 0]
    S_im = image_hsv[:, :, 1]
    V_im = image_hsv[:, :, 2]
    plt.figure(figsize=(15, 4))
    #affichage de "H"
    plt.subplot(131)
    im_h = plt.imshow(H_im, cmap='hsv')
    plt.colorbar(im_h)
    plt.title('H')
    #Affichage de "S"
    plt.subplot(132)
    im_s = plt.imshow(S_im, cmap='gray')
    plt.colorbar(im_s)
    plt.title('S')
    #affichage de "V"
    plt.subplot(133)
    im_v = plt.imshow(V_im, cmap='gray')
    plt.colorbar(im_v)
    plt.title('V')
    plt.show()
    #Création de la masque avec les valeurs sortis de l'affichage de H,S et V
    Masque = (H > 0.525) & (H < 0.75) & (S > 0.3) & (V > 0.3)
    plt.figure()
    plt.imshow(Masque)
    plt.show()
    #Création de l'image avec la voiture rouge à l'aide de la masque
    image_rouge = image_hsv.copy()
    image_rouge[:,:,0][Masque] = 0.05
    image_rouge_RGB=colors.hsv_to_rgb(image_rouge)
    plt.figure()
    plt.imshow(image_rouge_RGB)
    plt.show()




if __name__ == '__main__':
    main()
