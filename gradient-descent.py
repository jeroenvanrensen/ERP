import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def loaddata(psfname, imgname):
    psf = np.array(Image.open(psfname), dtype="float32")[:, :, 1]
    img = np.array(Image.open(imgname), dtype="float32")[:, :, 1]

    psf /= np.linalg.norm(psf.ravel())
    img /= np.linalg.norm(img.ravel())

    return psf, img


# def grad_descent(psf, img):


psfname = "2026-05-18/H1.png"
imgname = "2026-05-18/11.png"
iters = 10
psf, img = loaddata(psfname, imgname)
restored = grad_descent(psf, img)
