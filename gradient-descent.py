import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def loaddata(psfname, imgname):
    psf = np.array(Image.open(psfname), dtype="float32")[:, :, 1]
    img = np.array(Image.open(imgname), dtype="float32")[:, :, 1]

    psf /= np.linalg.norm(psf.ravel())
    img /= np.linalg.norm(img.ravel())

    return psf, img


def nextPower2(n):
    return int(2 ** np.ceil(np.log2(n)))


def initMatrices(psf):
    pixel_start = (np.max(psf) + np.min(psf)) / 2
    x = np.ones(psf.shape) * pixel_start

    init_shape = psf.shape
    padded_shape = [nextPower2(2 * n - 1) for n in init_shape]
    starti = (padded_shape[0] - init_shape[0]) // 2
    endi = starti + init_shape[0]
    startj = (padded_shape[1] // 2) - (init_shape[1] // 2)
    endj = startj + init_shape[1]
    hpad = np.zeros(padded_shape)
    hpad[starti:endi, startj:endj] = psf

    H = np.fft.fft2(np.fft.ifftshift(hpad), norm="ortho")
    Hadj = np.conj(H)

    def crop(X):
        return X[starti:endi, startj:endj]

    def pad(v):
        vpad = np.zeros(padded_shape).astype(np.complex64)
        vpad[starti:endi, startj:endj] = v
        return vpad

    v = np.real(pad(x))

    return H, Hadj, v, crop, pad


def calcA(H, vk, crop):
    Vk = np.fft.fft2(np.fft.ifftshift(vk))
    return crop(np.fft.fftshift(np.fft.ifft2(H * Vk)))


def calcAHerm(Hadj, diff, pad):
    xpad = pad(diff)
    X = np.fft.fft2(np.fft.ifftshift(xpad))
    return np.fft.fftshift(np.fft.ifft2(Hadj * X))


def grad(Hadj, H, vk, b, crop, pad):
    Av = calcA(H, vk, crop)
    diff = Av - b
    return np.real(calcAHerm(Hadj, diff, pad))


def grad_descent(psf, img, iters):
    H, Hadj, v, crop, pad = initMatrices(psf)

    alpha = np.real(1.8 / (np.max(Hadj * H)))

    vk = v
    tk = 1
    xk = v

    for _ in range(iters):
        x_k1 = xk
        gradient = grad(Hadj, H, vk, img, crop, pad)
        vk -= alpha * gradient
        xk = np.maximum(vk, 0)
        t_k1 = (1 + np.sqrt(1 + 4 * tk**2)) / 2
        vk = xk + (tk - 1) / t_k1 * (xk - x_k1)
        tk = t_k1

    return np.maximum(crop(vk), 0)


def restore_image(tape, led):
    start_time = time.perf_counter()

    psfname = f"measurements/psf/{tape}cm/psf{tape}cm,{led}cm.png"
    imgname = f"measurements/points/{tape}cm/points{tape}cm,{led}cm.png"

    iters = 10**4
    psf, img = loaddata(psfname, imgname)
    restored = grad_descent(psf, img, iters)

    cv2.imwrite(
        f"results/result{tape}cm,{led}cm.png",
        (restored / np.max(restored) * 255).astype(np.uint8),
    )

    end_time = time.perf_counter()
    execution_time = (end_time - start_time) / 60
    print(f"Finished tape {tape}cm, led {led}cm ({execution_time:.1f}min).")


tape_distances = [
    "0.1",
    "0.125",
    "0.15",
    "0.175",
    "0.2",
    "0.225",
    "0.25",
    "0.275",
    "0.3",
]
led_distances = ["5", "7", "9", "11", "13", "15"]

for tape in tape_distances:
    for led in led_distances:
        restore_image(tape, led)
