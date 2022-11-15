# Team 23027 
# Created by: Divyansh Rathod
# Fluid Level Dection for Big Bottle

import numpy as np
import pandas as pd
import cv2 as cv 
#from google.colab.patches import cv2_imshow # for image display
#from skimage import io
from PIL import Image 
import matplotlib.pylab as plt
import os

path1 = "" # Path of Original Image

''' Use Gamma correction on the original image to further highlight the amount of liquid in the bottle '''

nat = cv.imread(path1)
nat_2 = cv.cvtColor(nat, cv.COLOR_BGR2RGB)
cv.imshow("", nat_2)
cv.waitKey(0)

def gammaCorrection(src, gamma):
    invGamma = 1 / gamma

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv.LUT(src, table)


gamma = 0.3      # change the value here to get different result
adjusted = gammaCorrection(nat_2, gamma=gamma)
cv.imshow("", adjusted)
cv.waitKey(0)

directory = "" # Directory in which to save the corrected image
os.chdir(directory)
cv.imwrite("Threshold.jpg", adjusted)

''' Load the image, get the pixel intensities and the number of pixels in the image'''
''' Convert the image to grayscale for further analysis '''

imGray = cv.cvtColor(adjusted, cv.COLOR_BGR2GRAY)
cv.imshow("", imGray)
cv.waitKey(0)

height, width= imGray.shape[:2]

''' Initialize the variables, and run for-loops to find pixel intensities. Then take the average value of the pixel intensities of a row'''
''' Using the average value, compare it to a predetermined threshold and find the height of the bottom and top of the bottle and the fluid level'''

pixelInt1 = 0
pixelCount = 0
avgInt0 = 0


for j in range(height):
    pixelCount = 0
    pixelInt1 = 0
    for i in range(width):
        pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
        pixelCount = pixelCount + 1

    avgInt = pixelInt1 / pixelCount
    #print("avgInt: ", avgInt)
    #print("avgInt0 = ", avgInt0)

    if (avgInt >= 20):
        bottom = j
        avgInt0 = 0
        break
    else:
        avgInt0 = avgInt

pixelInt1 = 0
pixelCount = 0
avgInt0 = 0

for j in range(height):
    if (j >= bottom):
        pixelCount = 0
        pixelInt1 = 0
        for i in range(width):
            pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
            pixelCount = pixelCount + 1

        avgInt = pixelInt1 / pixelCount
        #print("avgInt: ", avgInt)
        #print("avgInt0 = ", avgInt0)

        if (avgInt >= 110):
            top = j
            avgInt0 = 0
            break
        else:
            avgInt0 = avgInt

pixelInt1 = 0
pixelCount = 0
avgInt0 = 0

for j in range(height):
    if (j >= top):
        pixelCount = 0
        pixelInt1 = 0
        for i in range(width):
            pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
            pixelCount = pixelCount + 1

        avgInt = pixelInt1 / pixelCount
        #print("avgInt: ", avgInt)
        #print("avgInt0 = ", avgInt0)

        if (avgInt <= 65):
            bottleTop = j
            avgInt0 = 0
            break
        else:
            avgInt0 = avgInt

''' Using the height values, draw a white line for each of the values.'''

for i in range(width):
    imGray[height - (bottom + 1), i] = 255
    imGray[height - (top + 1), i] = 255
    imGray[height - (bottleTop + 1), i] = 255


cv.imshow("", imGray)
cv.waitKey(0)

''' Use bottle specific calculations to convert height from pixels into fluid volume. '''

pixelHeight = top - bottom
bottleHeight = bottleTop - bottom
print("Height of Liquid: ", pixelHeight)
print("Height of Bottle: ", bottleHeight)

heightRatio = 17.5/bottleHeight
fluidHeight = pixelHeight * heightRatio
fluidVolume = (208.5 * fluidHeight)

print("Fluid Volume: ", int(fluidVolume), "ml")
