import cv2
import numpy as np
import trackpy as tp


def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def find_sizes(n, tape, led):
    image = cv2.imread(f"results/result{n},{tape}cm,{led}cm.png")[:, :, 1]
    trackpy_result = tp.locate(image, 21, minmass=1_000)
    # tp.annotate(trackpy_result, image)
    trackpy_result = trackpy_result.to_numpy()

    # Extract x,y,mass-values
    points = np.array(
        [
            (trackpy_result[i, 1], trackpy_result[i, 0], trackpy_result[i, 2])
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

    distances = []
    for point in points:
        for point_ in points:
            distances.append(distance(point, point_))

    width, height = np.unique(distances)[-2:]
    return (width, height)


ns = [1]
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

for n in ns:
    for tape in tape_distances:
        for led in led_distances:
            result = find_sizes(n, tape, led)
            if result == False:
                print("Skipped")
            if result != False:
                width, height = result
                sizes.append((int(n), float(tape), float(led), width, height))

headers = "n,tape,led,width,height"
np.savetxt("sizes.csv", sizes, delimiter=",", fmt="%s", header=headers, comments="")
