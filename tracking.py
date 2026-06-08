import os

import cv2
import numpy as np
import trackpy as tp


def distance(point1, point2):
    d = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    error = (
        np.sqrt(
            (point1[3] ** 2 + point2[3] ** 2)
            * ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        )
        / d
    )

    return d, error


def find_sizes(n, tape, led):
    filename = f"results/result{n},{tape}cm,{led}cm.png"
    image = cv2.imread(filename)[:, :, 1]
    trackpy_result = tp.locate(image, 21, minmass=1000)
    # tp.annotate(trackpy_result, image)
    trackpy_result = trackpy_result.to_numpy()

    # Extract x,y,mass,size-values
    points = np.array(
        [
            (
                trackpy_result[i, 1],
                trackpy_result[i, 0],
                trackpy_result[i, 2],
                trackpy_result[i, 3],
            )
            for i in range(0, np.shape(trackpy_result)[0])
        ]
    )

    if len(points) < 4:
        return False
        # raise Exception(f"ERROR: NOT 4 POINTS (GOT {len(points)} POINTS)")

    # print(
    #     "minimal brightness: "
    #     + str(int(np.floor(points[np.argsort(points[:, 2])][-4][2])))
    # )
    points = points[np.argsort(points[:, 2])][-4:]

    right = points[np.argmax(points[:, 0])]
    left = points[np.argmin(points[:, 0])]
    top = points[np.argmin(points[:, 1])]
    bottom = points[np.argmax(points[:, 1])]

    width, width_error = distance(right, left)
    height, height_error = distance(top, bottom)

    return (width, width_error, height, height_error)

    # print(points)
    # print(right_index, left_index, top_index, bottom_index)

    # distances = []
    # for point in points:
    #     for point_ in points:
    #         distances.append(distance(point, point_))

    # width, height = np.unique(distances)[-2:]
    # return (width, height)


ns = [1, 2]
tape_distances = [
    "0_1",
    "0_125",
    "0_15",
    "0_175",
    "0_2",
    "0_225",
    "0_25",
    "0_275",
    "0_3",
]
led_distances = ["5", "7", "9", "11", "13", "15"]

sizes = []

skip = [
    (1, "0_3", "5"),
    (1, "0_3", "7"),
    (1, "0_3", "9"),
    (1, "0_25", "5"),
    (1, "0_25", "7"),
    (1, "0_225", "5"),
    (1, "0_275", "5"),
    (1, "0_275", "7"),
    (2, "0_175", "5"),
    (2, "0_2", "5"),
    (2, "0_225", "5"),
    (2, "0_25", "5"),
    (2, "0_25", "7"),
    (2, "0_275", "5"),
    (2, "0_275", "7"),
    (2, "0_275", "9"),
    (2, "0_3", "5"),
    (2, "0_3", "7"),
]

for n in ns:
    for tape in tape_distances:
        for led in led_distances:
            if (n, tape, led) in skip:
                print("Skipped....")
                continue

            result = find_sizes(n, tape, led)
            if result == False:
                print("FAILURE")
            if result != False:
                width, width_error, height, height_error = result
                sizes.append(
                    (
                        int(n),
                        float(tape.replace("_", ".")),
                        float(led) - 0.4,
                        width,
                        width_error,
                        height,
                        height_error,
                    )
                )

headers = "n,tape,led,width,width_error,height,height_error"
np.savetxt("sizes.csv", sizes, delimiter=",", fmt="%s", header=headers, comments="")
