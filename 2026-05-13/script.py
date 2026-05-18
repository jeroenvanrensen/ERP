import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import restoration

Y = cv2.imread("Y2.tif")[:, :, 1] / 255
H = cv2.imread("H2.tif")[:, :, 1] / 255
X = restoration.wiener(Y, H, balance=10**-5)

plt.imshow(X, cmap="gray")
plt.axis("off")
plt.show()
