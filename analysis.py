import matplotlib.pyplot as plt
import numpy as np

data = np.genfromtxt("sizes.csv", delimiter=",", skip_header=1)

tape_distances = [
    0.1,
    0.125,
    0.15,
    0.175,
    0.2,
    0.225,
    0.25,
    0.275,
    0.3,
]
led_distances = [5, 7, 9, 11, 13, 15]

for led in led_distances:
    sizes = data[data[:, 1] == float(led)]

    xs = []
    ys = []
    y_errors = []

    for entry in sizes:
        xs.append(entry[0])
        ys.append(0.5 * (entry[2] + entry[3]))
        y_errors.append(np.abs(entry[2] - entry[3]))

    plt.errorbar(xs, ys, y_errors, label=f"{led}cm")

plt.xlabel("Tape distance (cm)")
plt.ylabel("Square size (px)")
plt.legend(loc=2)
plt.show()
