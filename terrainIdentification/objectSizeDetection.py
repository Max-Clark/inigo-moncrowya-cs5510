import cv2
import numpy as np


FOCAL_LENGTH = 3.04  # mm
SENSOR_WIDTH = 3.68
SENSOR_HEIGHT = 2.76
# SENSOR_WIDTH_PIXELS = 3280
# SENSOR_HEIGHT_PIXELS = 2464
SENSOR_WIDTH_PIXELS = 1640
SENSOR_HEIGHT_PIXELS = 750  # Because I crop the height.


def getImageSizeInPixels(image):

    image = cv2.imread(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    twoDimage = image.reshape((-1, 3))
    twoDimage = np.float32(twoDimage)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 3
    attempts = 10
    ret, label, center = cv2.kmeans(twoDimage, K, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    result_image = res.reshape(image.shape)

    cv2.imwrite("resultImage.jpg", result_image)

    imageResultRead = cv2.imread("resultImage.jpg")

    # image = cv2.imread(image)
    #
    # img_grey = cv2.cvtColor(result_image, cv2.COLOR_BGR2GRAY)
    # # set a thresh
    # thresh = 100
    # # get threshold image
    # ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
    # # find contours
    # thresh = cv2.threshold(img_grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    gray = cv2.cvtColor(result_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 10, 200)


    contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # img_contours = np.zeros(result_image.shape)

    cv2.drawContours(imageResultRead, contours, -1, (0, 255, 0), 3)
    # contours = contours[0] if len(contours) == 2 else contours[1]
    maxWidth = 0

    for i, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        maxWidth = max(w, maxWidth)
        cv2.putText(result_image, str(w), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        cv2.rectangle(result_image, (x, y), (x + w, y + h), (36, 255, 12), 1)



    # create an empty image for contours
    # img_contours = np.zeros(img.shape)
    # draw the contours on the empty image
    # cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3)
    # save image
    cv2.imwrite('contours.png', result_image)

    # gray = cv2.cvtColor(img_contours, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # thresh = cv2.threshold(img_contours, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #
    # x,y,w,h = cv2.boundingRect(thresh)
    #
    # cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
    # # cv2.imshow("thresh", thresh)
    # cv2.imshow("image", image)
    # cv2.imwrite("image10.jpg", thresh)
    # cv2.imwrite("thresh.jpg", thresh)

    return maxWidth


def getObjectWidth(distance, image):

    objectWidthOnSensor = getObjectWidthOnSensor(image)

    return ((distance * objectWidthOnSensor) / FOCAL_LENGTH)


def getObjectWidthOnSensor(image):
    # TODO: Get the object width
    objectWidth = getImageSizeInPixels(image)


    return (SENSOR_WIDTH * objectWidth)/SENSOR_WIDTH_PIXELS  


