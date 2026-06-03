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

# for led in led_distances:
#     sizes = data[data[:, 2] == float(led)]

#     xs = []
#     ys = []
#     y_errors = []

#     for entry in sizes:
#         if entry[0] == 2:
#             continue
#         xs.append(entry[1])
#         ys.append(0.5 * (entry[3] + entry[5]))
#         y_errors.append(0.5 * np.sqrt(entry[4] ** 2 + entry[6] ** 2))

#     plt.errorbar(xs, ys, y_errors, label=f"{led}cm")

# plt.xlabel("Tape distance (cm)")
# plt.ylabel("Square size (px)")
# plt.legend(loc=1)
# plt.show()

x1s = []
x1_errors = []
y1s = []
y1_errors = []

x2s = []
x2_errors = []
y2s = []
y2_errors = []

T_err = 0.005  # cm
L_err = 0.05  # cm

for entry in data:
    if entry[0] == 1:
        x1s.append(entry[1] / (entry[2]))
        x1_errors.append(
            np.sqrt(T_err**2 / entry[2] ** 2 + L_err**2 * entry[1] ** 2 / entry[2] ** 4)
        )
        y1s.append(0.5 * (entry[3] + entry[5]))
        y1_errors.append(0.5 * np.sqrt(entry[4] ** 2 + entry[6] ** 2))
    if entry[0] == 2:
        x2s.append(entry[1] / (entry[2]))
        x2_errors.append(
            np.sqrt(T_err**2 / entry[2] ** 2 + L_err**2 * entry[1] ** 2 / entry[2] ** 4)
        )
        y2s.append(0.5 * (entry[3] + entry[5]))
        y2_errors.append(0.5 * np.sqrt(entry[4] ** 2 + entry[6] ** 2))

plt.errorbar(x1s, y1s, yerr=y1_errors, xerr=x1_errors, fmt=".")
plt.errorbar(x2s, y2s, yerr=y2_errors, xerr=x2_errors, fmt=".")
plt.xlabel("T/L (AU)")
plt.ylabel("Size (px)")
plt.show()
