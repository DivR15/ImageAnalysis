# Team 23027 
# Created by: Divyansh Rathod
# Fluid Level Dection for Big Bottle

'''Thresold values in this code rely on the conditions in which the pictures were taken and can be chnaged based on the picture'''

import numpy as np
import cv2 as cv
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

directory = "" # Directory in which to save the thresholded image
os.chdir(directory)
cv.imwrite("Threshold.jpg", adjusted)

''' Load the image, get the pixel intensities and the number of pixels in the image'''
''' Convert the image to grayscale for further analysis '''

imGray = cv.cvtColor(adjusted, cv.COLOR_BGR2GRAY)
cv.imshow("Gray Scale Image ", imGray)
cv.waitKey(0)

height, width= imGray.shape[:2]

''' Initialize the variables, and run for-loops to find pixel intensities. Then take the average value of the pixel intensities of a row'''
''' Using the average value, compare it to a predetermined threshold and find the height of the bottom and top of the bottle and the fluid level'''

pixelInt1 = 0
pixelCount = 0
avgInt0 = 0

''' Loop over the pixel intensities at the top of the picture from the right to find where the clip starts, draw a vertical line there. '''
'''Repeat the process from the left and find where the clip ends, draw a vertical line there'''
'''These values can be skipped while looping through the bottle as clip color can affect the algorithm and should be discarded'''

a = height/6

for b in range(width):
    color = 0
    color = color + imGray[int(a), b]
    if (color > 1):
        first = b
        break

for b in range(width):
    color = 0
    color = color + imGray[int(a), width - (b+1)]
    print("color: ", color)
    if (color > 1):
        second = width - (b+1)
        break


for b in range(height):
    imGray[b, first] = 255
    imGray[b, second] = 255

'''The for loop takes the intensities of the rows starting from the bottom and moves up until it detects the bottom of the bottle'''

for j in range(height):
    pixelCount = 0
    pixelInt1 = 0
    for i in range(width):
        pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
        pixelCount = pixelCount + 1

    avgInt = pixelInt1 / pixelCount
    #print("avgInt: ", avgInt)
    #print("avgInt0 = ", avgInt0)

    if (avgInt >= 10):
        bottom = j
        avgInt0 = 0
        break
    else:
        avgInt0 = avgInt

'''The next for loop starts from 60 pixels above the bottle bottom to eliminate the shadow produces near the bottom and takes the average of 5 rows of pixels.'''
'''The change in these averages are compared and the fluid level is detected.'''

pixelInt1 = 0
pixelCount = 0
avgInt0 = 0
avgIntList = []
avgInt10 = 0
Int10 = 0
prevInt10 = 0


for j in range(height):
    if (j >= bottom + 60):
        pixelCount = 0
        pixelInt1 = 0
        for i in range(width):
            if (i < first) or (i > second):
                if (imGray[height - (j+1), i] >= 25) and (imGray[height - (j+1), i] <= 120) :
                    pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
                    pixelCount = pixelCount + 1
        if (pixelCount != 0):
            avgInt = pixelInt1 / pixelCount
        # print("avgInt: ", avgInt)
        # print("avgInt0 = ", avgInt0)

        if (len(avgIntList) < 5):
            #print("len: ", len(avgIntList))
            avgIntList.append(avgInt)
        elif(len(avgIntList) >= 5):
            for k in range(len(avgIntList)):
                #print("Int: ", avgIntList[k-1])
                Int10 = Int10 + avgIntList[k-1]
                #print("Int10: ", Int10)
            avgInt10 = Int10 / 5
            Int10 = 0
            avgIntList = []
            #print("###################################################")

        if (prevInt10 == 0):
            prevInt10 = avgInt10
        else:
            diffInt10 = abs(avgInt10 - prevInt10)
            print("Diff: ", diffInt10)
            prevInt10 = avgInt10
        
            if (diffInt10 > 5):
                top = j
                break

'''The final loop starts after the fluid level and takes the pixel intensities of rows until it detects the top of the bottle'''

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

        if (avgInt <= 40):
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


''' Use bottle specific calculations to convert height from pixels into fluid volume. '''

cv.imshow("", imGray)
cv.waitKey(0)

pixelHeight = top - bottom
bottleHeight = bottleTop - bottom
print("Height of Liquid: ", pixelHeight)
print("Height of Bottle: ", bottleHeight)

heightRatio = 18/bottleHeight
fluidHeight = pixelHeight * heightRatio
fluidVolume = (166.67 * fluidHeight) # Value of the equation may change based on the bottle

print("Fluid Volume: ", fluidVolume, "ml")
print("width: ", width)

