import matplotlib.pyplot as plt
import numpy as np
import scipy.odr as odr

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
led_distances = np.array([5, 7, 9, 11, 13, 15]) - 0.4

for led in led_distances:
    sizes = data[data[:, 2] == float(led)]

    xs = []
    ys = []
    y_errors = []

    for entry in sizes:
        if entry[0] == 2:
            continue
        xs.append(entry[1])
        ys.append(0.5 * (entry[3] + entry[5]))
        y_errors.append(0.5 * np.sqrt(entry[4] ** 2 + entry[6] ** 2))

    plt.errorbar(xs, ys, y_errors, label=f"{led}cm")

plt.xlabel("Tape distance (cm)")
plt.ylabel("Square size (px)")
plt.legend(loc=1)
plt.show()

# x1s = []
# x1_errors = []
# y1s = []
# y1_errors = []

# x2s = []
# x2_errors = []
# y2s = []
# y2_errors = []

# T_err = 0.01  # cm
# L_err = 0.05  # cm

# for entry in data:
#     if entry[0] == 1:
#         x1s.append(entry[1] / (entry[2]))
#         x1_errors.append(
#             np.sqrt(T_err**2 / entry[2] ** 2 + L_err**2 * entry[1] ** 2 / entry[2] ** 4)
#         )
#         y1s.append(0.5 * (entry[3] + entry[5]))
#         y1_errors.append(0.5 * np.sqrt(entry[4] ** 2 + entry[6] ** 2))
#     if entry[0] == 2:
#         x2s.append(entry[1] / (entry[2]))
#         x2_errors.append(
#             np.sqrt(T_err**2 / entry[2] ** 2 + L_err**2 * entry[1] ** 2 / entry[2] ** 4)
#         )
#         y2s.append(0.5 * (entry[3] + entry[5]))
#         y2_errors.append(0.5 * np.sqrt(entry[4] ** 2 + entry[6] ** 2))


# def func(params, x):
#     return params[0] * x


# p0 = [6000]

# # n = 1
# odr_model = odr.Model(func)
# odr_data = odr.RealData(x1s, y1s, sy=y1_errors, sx=x1_errors)
# odr_obj = odr.ODR(odr_data, odr_model, beta0=p0)
# odr_res = odr_obj.run()
# par_best = odr_res.beta
# [slope] = par_best
# # (8a) De beste schatters voor de parameters
# par_best = odr_res.beta
# # (8b) De (EXTERNE!) onzekerheden voor deze parameters
# par_sig_ext = odr_res.sd_beta
# # (8c) De (INTERNE!) covariantiematrix
# par_cov = odr_res.cov_beta
# print(" De (INTERNE!) covariantiematrix  = \n", par_cov)
# # (8d) De chi-kwadraat en de gereduceerde chi-kwadraat van deze aanpassing
# chi2 = odr_res.sum_square
# print("\n Chi-squared         = ", chi2)
# chi2red = odr_res.res_var
# print(" Reduced chi-squared = ", chi2red, "\n")
# # (8e) Een compacte weergave van de belangrijkste resultaten als output
# odr_res.pprint()

# xplot = np.linspace(np.min(x1s), np.max(x1s), num=1500)
# plt.plot(xplot, func(par_best, xplot), "r-", linewidth=2, label="Beste fit", c="blue")

# # n = 2
# odr_model = odr.Model(func)
# odr_data = odr.RealData(x2s, y2s, sy=y2_errors, sx=x2_errors)
# odr_obj = odr.ODR(odr_data, odr_model, beta0=p0)
# odr_res = odr_obj.run()
# par_best = odr_res.beta
# [slope] = par_best
# # (8a) De beste schatters voor de parameters
# par_best = odr_res.beta
# # (8b) De (EXTERNE!) onzekerheden voor deze parameters
# par_sig_ext = odr_res.sd_beta
# # (8c) De (INTERNE!) covariantiematrix
# par_cov = odr_res.cov_beta
# print(" De (INTERNE!) covariantiematrix  = \n", par_cov)
# # (8d) De chi-kwadraat en de gereduceerde chi-kwadraat van deze aanpassing
# chi2 = odr_res.sum_square
# print("\n Chi-squared         = ", chi2)
# chi2red = odr_res.res_var
# print(" Reduced chi-squared = ", chi2red, "\n")
# # (8e) Een compacte weergave van de belangrijkste resultaten als output
# odr_res.pprint()

# xplot = np.linspace(np.min(x1s), np.max(x1s), num=1500)
# plt.plot(xplot, func(par_best, xplot), "r-", linewidth=2, label="Beste fit", c="orange")

# plt.errorbar(x1s, y1s, yerr=y1_errors, xerr=x1_errors, fmt=".", c="blue")
# plt.errorbar(x2s, y2s, yerr=y2_errors, xerr=x2_errors, fmt=".", c="orange")
# plt.xlabel("T/L (AU)")
# plt.ylabel("Size (px)")
# plt.show()
