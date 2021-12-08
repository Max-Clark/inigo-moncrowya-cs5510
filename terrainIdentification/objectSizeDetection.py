import cv2

FOCAL_LENGTH = 3.04  # mm
SENSOR_WIDTH = 3.68
SENSOR_HEIGHT = 2.76
SENSOR_WIDTH_PIXELS = 3280
SENSOR_HEIGHT_PIXELS = 2464


def getImageSizeInPixels(image):
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GausianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    x,y,w,h = cv2.boundingRect(thresh)

    return x,y,w,h

def getObjectWidth(distance, image):

    if distance 

    objectWidthOnSensor = getObjectWidthOnSensor(image)
    
    


    
def getObjectHeight(distance, image):
    objectHeightOnSensor = getObjectHeightOnSensor(image)


def getObjectWidthOnSensor(image):
    # TODO: Get the object width



    x,y,objectWidth,objectHeight = getImageSizeInPixels(image)


    return (SENSOR_WIDTH * objectWidth)/SENSOR_WIDTH_PIXELS  


def getObjectHeightOnSensor(image):
    pass

