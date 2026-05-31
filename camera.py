import cv2 as cv

camera = cv.VideoCapture(0)

if camera.isOpened():
    # Read several frames to let auto-exposure settle
    # for _ in range(30):
    #     camera.read()

    # Now capture the actual image
    ret, frame = camera.read()
    if ret:
        cv.imwrite("image.png", frame)
else:
    print("Camera not opened.")

camera.release()
