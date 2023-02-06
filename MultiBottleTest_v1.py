# Team 23027 
# Created by: Divyansh Rathod
# Fluid Level Dection for Multiple Bottles

# Import Libraries

import cv2 as cv 
import os
import csv

# Read File and Gamma Conversion.

nat = cv.imread("") # Name of image here
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
cv.imwrite("Threshold.jpg", adjusted)

imGray = cv.cvtColor(adjusted, cv.COLOR_BGR2GRAY)

height, width= imGray.shape[:2]

print("Height: ", height)
print("Width: ", width)

# Use ratio of width of the bottles respective to the width of the picture and draw the vertical lines identifying each bottle.

bigBRatio = int(width/3.85)
smallBRatio = int(width/7.4)
b1Start = int(width/10)
b1End = b2Start = b1Start + bigBRatio
b2End = b3Start = b1End + smallBRatio
b3End = b4Start = b3Start + smallBRatio
b4End = width - b1Start

for i in range(height):
    imGray[i, b1Start] = 255
    imGray[i, b1End] = 255
    imGray[i, b2End] = 255
    imGray[i, b3End] = 255
    imGray[i, b4End] = 255

a = height/3.7

# DEFINE FUNCTION: Identify the clips and draw lines

def clips(width, height, start, end):
    for i in range(width):
        if (i > start) and (i < end):
            for b in range(start+1, end):
                color = 0
                color = color + imGray[int(a), b]
                if (color > 1):
                    first = b
                    break

            for b in range(start+1, end):
                color = 0
                if (b > first):
                    color = color + imGray[int(a), b]
                    if (color < 1):
                        second = b
                        break
            
    for b in range(height):
        imGray[b, first] = 255
        imGray[b, second] = 255
    
    return first, second

# DEFINE FUNCTION: If the bottle width is corresponding to the big bottle, run the fluid detection for big bottle. Save the values in a dictionary and draw the lines.

def bigBottleDetection(height, start, end, first, second):
    for j in range(height):
        pixelCount = 0
        pixelInt1 = 0
        for i in range(start+1, end):
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
    avgIntList = []
    avgInt10 = 0
    Int10 = 0
    prevInt10 = 0



    for j in range(height):
        if (j >= bottom + 45):
            pixelCount = 0
            pixelInt1 = 0
            for i in range(start+1, end):
                if (i < first) or (i > second):
                    if (imGray[height - (j+1), i] >= 25) and (imGray[height - (j+1), i] <= 120) :
                        pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
                        pixelCount = pixelCount + 1
            if (pixelCount != 0):
                avgInt = pixelInt1 / pixelCount

            if (len(avgIntList) < 10):
                avgIntList.append(avgInt)
            elif(len(avgIntList) >= 10):
                for k in range(len(avgIntList)):
                    Int10 = Int10 + avgIntList[k-1]
                avgInt10 = Int10 / 10
                Int10 = 0
                avgIntList = []

            if (prevInt10 == 0):
                prevInt10 = avgInt10
            else:
                diffInt10 = abs(avgInt10 - prevInt10)
                prevInt10 = avgInt10
            
                if (diffInt10 > 14):
                    top = j
                    break

    pixelInt1 = 0
    pixelCount = 0
    avgInt0 = 0

    for j in range(height):
        if (j >= top):
            pixelCount = 0
            pixelInt1 = 0
            for i in range(start+1, end):
                pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
                pixelCount = pixelCount + 1

            avgInt = pixelInt1 / pixelCount

            if (avgInt <= 40):
                bottleTop = j
                avgInt0 = 0
                break
            else:
                avgInt0 = avgInt

    for i in range(start+1, end):
        imGray[height - (bottom + 1), i] = 255
        imGray[height - (top + 1), i] = 255
        imGray[height - (bottleTop + 1), i] = 255

    pixelHeight = top - bottom
    bottleHeight = bottleTop - bottom
    print("Height of Liquid: ", pixelHeight)
    print("Height of Bottle: ", bottleHeight)

    heightRatio = 18/bottleHeight
    fluidHeight = pixelHeight * heightRatio
    fluidVolume = (389.2 * fluidHeight) - 224.41

    print("Fluid Volume: ", fluidVolume, "ml")
    print("width: ", width)
    print("Height: ", height)

    return fluidVolume


# DEFINE FUNCTION:Repeat the same for the small bottle with the small bottle code.

def smallBottleDetection(height, start, end, first, second):
    avgInt0 = 0
    for j in range(height):
        pixelCount = 0
        pixelInt1 = 0
        for i in range(start+1, end):
            if (imGray[height - (j+1), i] < 255):
                pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
                pixelCount = pixelCount + 1

        avgInt = pixelInt1 / pixelCount

        if (avgInt >= 20):
            bottom = j
            avgInt0 = 0
            break
        else:
            avgInt0 = avgInt

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
            for i in range(start+1, end):
                if (i < first) or (i > second):
                    if (imGray[height - (j+1), i] >= 25) and (imGray[height - (j+1), i] <= 120) :
                        pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
                        pixelCount = pixelCount + 1
            if (pixelCount != 0):
                avgInt = pixelInt1 / pixelCount

            if (len(avgIntList) < 5):
                avgIntList.append(avgInt)
            elif(len(avgIntList) >= 5):
                for k in range(len(avgIntList)):
                    Int10 = Int10 + avgIntList[k-1]
                avgInt10 = Int10 / 5
                Int10 = 0
                avgIntList = []

            if (prevInt10 == 0):
                prevInt10 = avgInt10
            else:
                diffInt10 = abs(avgInt10 - prevInt10)
                prevInt10 = avgInt10
            
                if (diffInt10 > 5):
                    top = j
                    break

    pixelInt1 = 0
    pixelCount = 0
    avgInt0 = 0

    for j in range(height):
        if (j >= top):
            pixelCount = 0
            pixelInt1 = 0
            for i in range(start+1, end):
                pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
                pixelCount = pixelCount + 1

            avgInt = pixelInt1 / pixelCount

            if (avgInt <= 40):
                bottleTop = j
                avgInt0 = 0
                break
            else:
                avgInt0 = avgInt

    for i in range(start+1, end):
        imGray[height - (bottom + 1), i] = 255
        imGray[height - (top + 1), i] = 255
        imGray[height - (bottleTop + 1), i] = 255

    pixelHeight = top - bottom
    bottleHeight = bottleTop - bottom
    print("Height of Liquid: ", pixelHeight)
    print("Height of Bottle: ", bottleHeight)

    heightRatio = 18/bottleHeight
    fluidHeight = pixelHeight * heightRatio
    fluidVolume = (166.67 * fluidHeight)

    print("Fluid Volume: ", fluidVolume, "ml")
    return fluidVolume


# Based on width of each bottle, run the big or small fluid detction function.

clip1S, clip1E = clips(width,height,b1Start,b1End)
bottle1 = bigBottleDetection(height, b1Start, b1End, clip1S, clip1E)

cv.imshow("Bottle 1", imGray)
cv.waitKey(0)

clip2S, clip2E = clips(width,height,b2Start,b2End)
bottle2 = smallBottleDetection(height, b2Start, b2End, clip2S, clip2E)

cv.imshow("Bottle 2", imGray)
cv.waitKey(0)

clip3S, clip3E = clips(width,height,b3Start,b3End)
bottle3 = smallBottleDetection(height, b3Start, b3End, clip3S, clip3E)

cv.imshow("Bottle 3", imGray)
cv.waitKey(0)

clip4S, clip4E = clips(width,height,b4Start,b4End)
bottle4 = bigBottleDetection(height, b4Start, b4End, clip4S, clip4E)

cv.imshow("Bottle 4", imGray)
cv.waitKey(0)

# Display the fianl picture with all the lines.

cv.imshow("Final", imGray)
cv.waitKey(0)

# Export the dictionary to a csv file.

header = ["Bottle", "Value"]
dataDict =  [{"Bottle": 1, "Value" : bottle1},
{"Bottle": 2, "Value" : bottle2}, 
{"Bottle": 3, "Value" : bottle3}, 
{"Bottle": 4, "Value" : bottle4}  ]

filename = "ULTRABulkReagents_Data.csv"
with open(filename, "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    writer.writerows(dataDict)


