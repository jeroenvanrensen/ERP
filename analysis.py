import cv2
import numpy as np
import trackpy as tp

image = cv2.imread("results/result.png")[:, :, 1]
trackpy_result = tp.locate(image, 21, minmass=2000).to_numpy()
points = [
    (trackpy_result[i, 1], trackpy_result[i, 0])
    for i in range(0, np.shape(trackpy_result)[0])
]  # Extract x,y-values

if len(points) != 4:
    raise Exception(f"ERROR: NOT 4 POINTS (GOT {len(points)} POINTS)")


def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


distances = []
for point in points:
    for point_ in points:
        distances.append(distance(point, point_))

width, height = np.unique(distances)[-2:]
print(width, height)
