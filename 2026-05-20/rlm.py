import cv2
import numpy as np


def richardson_lucy(image, psf, iterations=30, clip=True, eps=1e-12):
    """
    Voert Richardson-Lucy deconvolutie uit.

    Parameters
    ----------
    image : np.ndarray
        Invoerbeeld (bijv. geladen met cv2.imread(..., cv2.IMREAD_GRAYSCALE)).
    psf : np.ndarray
        Point Spread Function (PSF), ook als NumPy-array.
        Dit is jouw "nulimage".
    iterations : int
        Aantal iteraties.
    clip : bool
        Als True, resultaat clippen naar [0, 1].
    eps : float
        Kleine waarde om deling door nul te voorkomen.

    Returns
    -------
    np.ndarray
        Hersteld beeld als float-array in bereik [0, 1].
    """

    # Converteer naar float64 en normaliseer naar [0,1]
    image = image.astype(np.float64)
    if image.max() > 1.0:
        image /= 255.0

    psf = psf.astype(np.float64)
    if psf.max() > 1.0:
        psf /= 255.0

    # Normaliseer PSF zodat som = 1
    psf_sum = psf.sum()
    if psf_sum <= 0:
        raise ValueError("PSF bevat geen geldige waarden.")
    psf /= psf_sum

    # Gespiegelde PSF
    psf_mirror = np.flip(psf)

    # Startschatting
    estimate = np.full_like(image, 0.5)

    for _ in range(iterations):
        # Convolutie van huidige schatting met PSF
        conv_estimate = cv2.filter2D(  # De cv2.filter geeft basically een convolutie
            estimate, -1, psf, borderType=cv2.BORDER_REPLICATE
        )

        # Vermijd deling door nul
        relative_blur = image / (conv_estimate + eps)

        # Correctiefactor
        correction = cv2.filter2D(
            relative_blur, -1, psf_mirror, borderType=cv2.BORDER_REPLICATE
        )

        # Update
        estimate *= correction

        if clip:
            estimate = np.clip(estimate, 0.0, 1.0)

    return estimate


if __name__ == "__main__":
    # Lees vervaagd beeld in (grijswaarden)
    image = cv2.imread("18.png")

    # Lees PSF ("nulimage") in
    psf = cv2.imread("H5.png")

    if image is None:
        raise FileNotFoundError("blurred.png niet gevonden.")
    if psf is None:
        raise FileNotFoundError("psf.png niet gevonden.")

    # Deconvolutie uitvoeren
    result = richardson_lucy(image, psf, iterations=1000)

    # Terug naar 8-bit voor opslaan
    result_uint8 = (result * 255).astype(np.uint8)

    # Opslaan
    cv2.imwrite("deconvolved.png", result_uint8)

    # Tonen
    cv2.imshow("Input", image)
    cv2.imshow("PSF", psf)
    cv2.imshow("Resultaat", result_uint8)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Optioneel, mocht de code traag zijn: vervang cv2.filter2D(image,-1,kernel) door bijvoorbeeld fftconvolve(image, psf, mode = 'same')
