import matplotlib.pyplot as plt
import numpy as np
image = plt.imread('citroen.jpg')
plt.imshow(image)
plt.show()
def convert_HSV(image):
    image_norm = image.astype.(np.float32) / 255.0
    R = image_norm[:, :, 0]
    G= image_norm[:, :, 1]
    B= image_norm[:, :, 2]
    Cmin= np.min(image_norm, axis=2)
    Cmax= np.max(image_norm, axis=2)
    delta=Cmax-Cmin
    V=Cmax
    cond1=  (Cmax==0)
    cond2 = (Cmax!=0)
    condition=[cond1,cond2]
    choix1 = 0
    choix2 = delta/Cmax
    S= np.select(condition,[choix1,choix2],default=choix1)
    cond_delta0 = (delta == 0)
    cond_r = (Cmax == R)
    cond_g = (Cmax == G)
    cond_b = (Cmax == B)
    conditions = [cond_delta0, cond_r, cond_g, cond_b]
    choix_delta0 = 0
    choix_r=((G-B)/delta)% 6
    choix_g=((B-R)/delta)+ 2
    choix_b=((R-G)/delta)+ 4
    choix=[choix_delta0, choix_r, choix_g, choix_b]
    H = np.select(conditions, choix, default=0)
    H = H/6
    return np.dstack((H, S, V))
image2=plt.colors.HSV_to_RGB(convert_HSV(image))
plt.imshow(image2)
plt.show()
