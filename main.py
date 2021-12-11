# from picamera import PiCamera
import pigpio
import cv2
import time
from terrainIdentification.objectSizeDetection import *
from mobility.CarRun import *
from sensors.mb1040.sensor_test import *
from picamera import PiCamera

motor_init()
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
    cropped_image = img[1250:2000, 820:2460]
    cv2.imwrite('croppedimage1.png', cropped_image)


    return cropped_image

def getDistance():
    IN_GPIO = 4  # Named 18 by RPi
    RUN_TIME = 60.0
    SAMPLE_TIME = 0.5

    pi = pigpio.pi()
    p = PwmMeasure(pi, IN_GPIO)
    start = time.time()

    while (True):
        time.sleep(SAMPLE_TIME)

        f = p.frequency()
        pw = p.pulse_width()
        dc = p.duty_cycle()

        return ((pw / 147) * 2.54) / 100

        # print(f'f={f}, pw={pw}, dc={dc}')
        # print(f'inches={pw / 147}, cm={(pw / 147) * 2.54}, m={((pw / 147) * 2.54) / 100}')


def main():
    
    try:
        while True:
            run(1)
            distance = getDistance()
            print(distance)

            if distance < 7:
                getPicture()
                croppedImage = cropPicture()
                objectWidth = getObjectWidth(distance, croppedImage)
                print(objectWidth)
                #  Assume .5 meters per second
                right(0.5)
                time.sleep(2)
                run((objectWidth / .5) * 100)
                time.sleep(2)
                left(0.5)


                time.sleep(5)
    except KeyboardInterrupt:
        pass



main()

#croppedImage = cropPicture()
#print(getObjectWidth(3, 'croppedimage1.png'))
# getImageSizeInPixels('croppedimage1.png')
# print(getImageSizeInPixels('croppedimage1.png'))

