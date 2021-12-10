from picamera import PiCamera
import cv2
import time
import objectSizeDetection

FOCAL_LENGTH = 3.04  # mm
SENSOR_WIDTH = 3.68
SENSOR_HEIGHT = 2.76
SENSOR_WIDTH_PIXELS = 3280
SENSOR_HEIGHT_PIXELS = 2464


def getPicture():
    camera = PiCamera()

    camera.capture("snapshot.jpg")
    camera.close()



def cropPicture():
    img = cv2.imread("snapshot.jpg")
    cropped_image = img[80:]

    return cropped_image


def getDistance():
    GPIO.output(TrigPin, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(TrigPin, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin, GPIO.LOW)
    

    begin = time.time()
    while not GPIO.input(EchoPin):
        t4 = time.time()
        if (t4 - t3) > 0.03:
            return -1
        t1 = time.time()
        while GPIO.input(EchoPin):
        t5 = time.time()
        if (t5 - t1) > 0.03:
            return -1

        t2 = time.time()
        time.sleep(0.01)

    #   print "distance is %d " % (((t2 - t1)* 340 / 2) * 100)
    time.sleep(0.01)
    return ((t2 - t1) * 340 / 2) * 100


def main():
    

    while True:
        distance = getDistance()

        if distance < 7:
            getPicture()
            croppedImage = cropPicture()
            getObjectWidth(distance, croppedImage) 
                       



