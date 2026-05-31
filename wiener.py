import cv2
import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft2, fftshift, ifft2
from scipy.signal.windows import kaiser


def wiener_deconvolution(blurred_img, kernel, K=0.01):
    # 1. Ensure the kernel is the same size as the image by padding with zeros
    # This aligns the frequency domains
    # dummy = np.zeros_like(blurred_img)
    # kh, kw = kernel.shape
    # dummy[:kh, :kw] = kernel

    # 2. Transform image and PSF to frequency domain
    G = fft2(blurred_img)
    H = fft2(kernel)
    H = H / np.max(H)

    # 3. Apply the Wiener Formula:
    # W = conj(H) / (|H|^2 + K)
    # Result = G * W
    H_conj = np.conj(H)
    H_sq_mag = np.abs(H) ** 2

    W = H_conj / (H_sq_mag + K)
    F_hat = G * W

    # 4. Transform back to spatial domain
    deconvolved = np.fft.fftshift(np.real(ifft2(F_hat)))

    # 5. Shift the result to fix the zero-padding offset
    return deconvolved


def apply_tukey_window(image, alpha):
    win = np.outer(kaiser(image.shape[0], alpha), kaiser(image.shape[1], alpha))
    return image * win


# --- Usage Example ---
# Load image as grayscale float
img = cv2.imread("images/points9,0.5.png")[:, :, 1] / 255.0
img = apply_tukey_window(img, 0.25)

# Define a simple 5x5 blur kernel (Point Spread Function)
psf = cv2.imread("images/psf9,0.5.png")[:, :, 1] / 255.0

# Deconvolve with K (adjust K based on noise levels)
result = wiener_deconvolution(img, psf, K=10**0)

# Clip values to [0, 1] for display
result = np.clip(result, 0, 1)

plt.imshow(result, cmap="gray")
plt.axis("off")
plt.show()
