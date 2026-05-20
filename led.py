from neopixel import Neopixel

numpix = 93
strip = Neopixel(numpix, 0, 28, "GRB")
strip.brightness(10)

cross = [
    0,
    8,
    16,
    24,
    32,
    38,
    44,
    50,
    56,
    60,
    64,
    68,
    72,
    75,
    78,
    81,
    84,
    86,
    88,
    90,
    92,
]

for p in cross:
    strip.set_pixel(p, (255, 255, 255))


# strip.fill((255, 0, 0))
# strip.set_pixel_line(0, 16, (0, 255, 0))

strip.show()
