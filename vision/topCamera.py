import cv2

def takePicture():
    cam = cv2.VideoCapture(0)

    ret, frame = cam.read()

    cv2.imwrite(f'UnpredictableDangerousHuman.png', frame)

    cam.release()
    cv2.destroyAllWindows()
