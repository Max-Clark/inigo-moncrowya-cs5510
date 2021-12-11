# from picamera import PiCamera
import pigpio
import cv2
import time
from terrainIdentification.objectSizeDetection import *
from mobility.CarRun import *
from vision.topCamera import *
from sensors.mb1040.sensor_test import *
from picamera import PiCamera
import os


FOCAL_LENGTH = 3.04  # mm
SENSOR_WIDTH = 3.68
SENSOR_HEIGHT = 2.76
SENSOR_WIDTH_PIXELS = 3280
SENSOR_HEIGHT_PIXELS = 2464


RUN_TIME = 60.0
SAMPLE_TIME = 0.5

IN_GPIO = 4  # Named 18 by RPi
pi = pigpio.pi()
p = PwmMeasure(pi, IN_GPIO)

def getPicture():
    camera = PiCamera()
    camera.capture("snapshot.jpg")
    camera.close()
    
    print("Cheese!")
    takePicture()
    print("Done!")



def cropPicture():
    img = cv2.imread("snapshot.jpg")
    cropped_image = img[1250:2000, 820:2460]
    cv2.imwrite('croppedimage.png', img)
    
    return 'croppedimage.png'

def getDistance():
    start = time.time()

    time.sleep(SAMPLE_TIME)

    f = p.frequency()
    pw = p.pulse_width()
    dc = p.duty_cycle()

    return ((pw / 147) * 2.54) / 100

        # print(f'f={f}, pw={pw}, dc={dc}')
        # print(f'inches={pw / 147}, cm={(pw / 147) * 2.54}, m={((pw / 147) * 2.54) / 100}')


def main():

    attemptsToMove = 0    
    distanceTravelled = 0
    motor_init()
    try:
        while True:
            distance = getDistance()
            print(f"Distance: {distance}")
            
            if distance > 1:
                run(1)
                brake(1)
                
               # spin_left(1.2)
               # brake(1.2)
               # leftArea = getDistance()
               # spin_right(2.4)
               # brake(2.4)
               # rightArea = getDistance()
               # spin_left(1.2)
               # brake(1.2)


#                with open("distanceTracker.txt", 'a') as f:
#                    f.write(str(leftArea))
#                    f.write(" ")
#                    f.write(str(rightArea))
#                    f.write("\n")


                attemptsToMove = 0
                distanceTravelled = 0

            else:
                getPicture()
                croppedImage = cropPicture()
                objectWidth = getObjectWidth(distance, croppedImage)
                print(f"Object Width: {objectWidth}")
                #  Assume .5 meters per second
                spin_right(1.2)
                brake(1.2)
                distanceSpin = getDistance()
                print(f"Distance After Spin {distanceSpin}")
                if distanceSpin < 1:
                    attemptsToMove = 4
                else:
                    run(((objectWidth + .3) * 0.8))
                    brake(((objectWidth + 0.3) * 0.8))
                    spin_left(1.2)
                    brake(1.2)
                    attemptsToMove += 1
                    distanceTravelled += (objectWidth + 0.3) * 0.8

                if attemptsToMove > 3:
                    back(distanceTravelled)
                    brake(distanceTravelled)
                    spin_right(1.2)
                    brake(1.2)
                    distanceTravelled = 0
                    attemptsToMove = 0
                    

    except KeyboardInterrupt:
        pass



main()

#croppedImage = cropPicture()
#print(getObjectWidth(3, 'croppedimage1.png'))
# getImageSizeInPixels('croppedimage1.png')
# print(getImageSizeInPixels('croppedimage1.png'))

