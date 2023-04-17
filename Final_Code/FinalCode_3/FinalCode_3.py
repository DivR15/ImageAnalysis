# Team 23027 
# Created by: Divyansh Rathod
# Fluid Level Detection and Reagent Id for Multiple Bottles

# Import Libraries

import os
import numpy as np
import cv2 as cv 
import csv
from datetime import date
import time
import pandas as pd
from tabulate import tabulate

# Read File and Gamma Conversion.

img = cv.imread("FARTest2B1S.jpg")
#cv.imshow("1", img)
#cv.waitKey(0)

height, width = img.shape[:2]
print("height: ", height)
print("width: ", width)

img = img[30:430, 100:660]
cv.imshow("2", img)
cv.waitKey(0)

# Read File and Gamma Conversion.
day = date.today()
day = day.strftime("%m_%d_%Y")
print(day)
time_ = time.strftime("%H_%M", time.localtime())
print(time_)

imageTitle = str(day) + "_" + str(time_) + ".jpg"
print(imageTitle)
cv.imwrite(imageTitle, img)
nat_2 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#cv.imshow("", nat_2)
#cv.waitKey(0)

def gammaCorrection(src, gamma):
    invGamma = 1 / gamma

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv.LUT(src, table)

gamma = 0.70      # change the value here to get different result
adjusted = gammaCorrection(nat_2, gamma=gamma)
#cv.imshow("", adjusted)
#cv.waitKey(0)
cv.imwrite("Threshold.jpg", adjusted)

imGray = cv.cvtColor(adjusted, cv.COLOR_BGR2GRAY)
#cv.imshow("", imGray)
#cv.waitKey(0)

height, width= imGray.shape[:2]

print("Height: ", height)
print("Width: ", width)

# Find ratio of width of the bottles and draw the vertical lines identifying each bottle.

for i in range(width):
    color = 0
    color = color + imGray[int(height/2), i]
    if color >= 20:
        b1Start = i
        break

bigBRatio = int(width/3.60)
smallBRatio = int(width/6.50)
# b1Start = int(width/20)
b1End = b2Start = b1Start + bigBRatio
b2End = b3Start = b1End + smallBRatio
b3End = b4Start = b3Start + smallBRatio

for i in range(width):
    color = 0
    color = color + imGray[int(height/2), width - i - 1]
    if color >= 30:
        b4End = i
# b4End = b4Start + bigBRatio

for i in range(height):
    imGray[i, b1Start] = 255
    imGray[i, b1End] = 255
    imGray[i, b2End] = 255
    imGray[i, b3End] = 255
    imGray[i, b4End] = 255

a = height/4.65
""" for i in range(width):
    imGray[int(a), i] = 255 """
#cv.imshow("", imGray)
#cv.waitKey(0)

# Identify the clips and draw lines

def clips(imGray, width, height, start, end):
    a = height/4.85
    for i in range(width):
        if (i > start) and (i < end):
            for b in range(start+1, end):
                color = 0
                color = color + imGray[int(a), b]
                if (color > 6):
                    first = b - 2
                    break

            for b in range(start+1, end):
                color = 0
                if (b > first + 5):
                    color = color + imGray[int(a), b]
                    # print("color: ", color)
                    if (color < 6):
                        second = b + 2
                        #print("B: ", b)
                        break
        
    # print("START: ", start)
    # print("END: ", end)
    # print("FIRST: ", first)
    # print("SECOND: ", second)
    for b in range(height):
        imGray[b, first] = 255
        imGray[b, second] = 255
    
    return first, second

def reagentDetection(img, first, second, height):
    h = int(height/5.85)
    pixelavg = [0,0,0]
    count = 0

    for w in range(first + 10, second - 15):
        pixelavg = pixelavg + img[h,w]
        img[h,w] = [0, 0, 0]
        count += 1
    pixelavg = pixelavg / count

    b, g, r = pixelavg
    print("r: ", int(r), "g: ", int(g), "b: ", int(b))

    if (r > 35) and (r < 60) and (g > 90) and (g < 120) and (b > 50) and (b < 75):
        reagentNo = 4
        reagent = "Reaction Buffer"
    elif (r > 0) and (r < 20) and (g > 65) and (g < 80) and (b > 30) and (b < 50):
        reagentNo = 5
        reagent = "Ultra CC1"
    elif (r > 90) and (r < 110) and (g > 30) and (g < 45) and (b > 20) and (b < 35):
        reagentNo = 6
        reagent = "Ultra CC2"
    elif (r > 5) and (r < 35) and (g > 30) and (g < 80) and (b > 10) and (b < 45):
        reagentNo = 7
        reagent = "Option"
    else:
        reagentNo = "Error"
        reagent = "Error"
    
    #cv.imshow("nat", img)
    #cv.waitKey(0)

    return reagentNo, reagent

# DEFINE FUNCTION: If the bottle width is corresponding to the big bottle, run the fluid detection for big bottle. Save the values in a dictionary and draw the lines.

def bigBottleDetection(imGray, height, start, end, first, second):
    for j in range(10, height):
        pixelCount = 0
        pixelInt1 = 0
        for i in range(start+1, end):
            pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
            pixelCount = pixelCount + 1

        avgInt = pixelInt1 / pixelCount
        #print("avgInt: ", avgInt)
        #print("avgInt0 = ", avgInt0)

        if (avgInt >= 10):
            bottom = j - 5
            avgInt0 = 0
            break
        else:
            avgInt0 = avgInt

    pixelInt1 = 0
    pixelCount = 0
    pixelCount2 = 0
    pixelInt2 = 0

    for j in range(height):
        if (j >= bottom + 75):
            pixelCount = 0
            pixelInt1 = 0
            pixelCount2 = 0
            pixelInt2 = 0
            for i in range(start+1, end):
                if (i < first) or (i > second):
                    if (imGray[height - (j+1), i] >= 20) and (imGray[height - (j+1), i] <= 120):
                        pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
                        pixelCount = pixelCount + 1
                    if (imGray[height - ((j+10)+1), i] >= 20) and (imGray[height - ((j+10)+1), i] <= 120):
                        pixelInt2 = pixelInt2 + imGray[height - ((j+5)+1), i]
                        pixelCount2 = pixelCount2 + 1

            if (pixelCount != 0) and (pixelCount2 != 0):
                avgInt1 = pixelInt1 / pixelCount
                avgInt2 = pixelInt2 / pixelCount2
            
            diff = abs(avgInt2 - avgInt1)
            #print("Diff: ", diff)
            if (diff >= 2):
                top = j + 10
                break

    pixelInt1 = 0
    pixelCount = 0
    avgInt0 = 0

    for j in range(height):
        if (j >= top):
            pixelCount = 0
            pixelInt1 = 0
            for i in range(start+1, end):
                if (i < first - 5) or (i > second + 5):
                    pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
                    pixelCount = pixelCount + 1

            avgInt = pixelInt1 / pixelCount
            #print("avgInt: ", avgInt)
            #print("avgInt0 = ", avgInt0)

            if (avgInt <= 10):
                bottleTop = j - 30
                avgInt0 = 0
                break
            else:
                avgInt0 = avgInt

    for i in range(start+1, end):
        imGray[height - (bottom + 1), i] = 255
        imGray[height - (top + 1), i] = 255
        imGray[height - (bottleTop + 1), i] = 0

    pixelHeight = top - bottom
    bottleHeight = bottleTop - bottom
    print("Height of Liquid: ", pixelHeight)
    print("Height of Bottle: ", bottleHeight)

    heightRatio = 17/bottleHeight
    fluidHeight = pixelHeight * heightRatio
    fluidVolume = int((353 * fluidHeight))

    print("Fluid Volume: ", fluidVolume, "ml")
    print("Fluid Height: ", fluidHeight )
    print("width: ", width)
    print("Height: ", height)

    if fluidVolume < 1500:
        fluidVolume = "Needs to be filled"    

    return fluidVolume


# DEFINE FUNCTION:Repeat the same for the small bottle with the small bottle code.

def smallBottleDetection(imGray, height, start, end, first, second):
    avgInt0 = 0
    for j in range(height):
        pixelCount = 0
        pixelInt1 = 0
        for i in range(start+1, end):
            if (imGray[height - (j+1), i] < 255):
                pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
                pixelCount = pixelCount + 1

        avgInt = pixelInt1 / pixelCount
        #print("avgInt: ", avgInt)
        #print("avgInt0 = ", avgInt0)

        if (avgInt >= 12):
            bottom = j - 5
            #print("Bottom: ", bottom)
            avgInt0 = 0
            break
        else:
            avgInt0 = avgInt

    pixelInt1 = 0
    pixelCount = 0
    pixelCount2 = 0
    pixelInt2 = 0

    for j in range(height):
        if (j >= bottom + 80):
            pixelCount = 0
            pixelInt1 = 0
            pixelInt2 = 0
            pixelCount2 = 0
            for i in range(start+1, end):
                if (i < first) or (i > second):
                    if (imGray[height - (j+1), i] >= 20) and (imGray[height - (j+1), i] <= 120) :
                        pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
                        pixelCount = pixelCount + 1
                    if (imGray[height - ((j+10)+1), i] >= 20) and (imGray[height - ((j+10)+1), i] <= 120):
                        pixelInt2 = pixelInt2 + imGray[height - ((j+5)+1), i]
                        pixelCount2 = pixelCount2 + 1

            if (pixelCount != 0) and (pixelCount2 != 0):
                avgInt1 = pixelInt1 / pixelCount
                avgInt2 = pixelInt2 / pixelCount2
            
            diff = abs(avgInt2 - avgInt1)
            #print("Diff: ", diff)
            if (diff >= 1.7):
                top = j + 10
                break
            
    pixelInt1 = 0
    pixelCount = 0
    avgInt0 = 0

    for j in range(height):
        if (j >= top + 15):
            pixelCount = 0
            pixelInt1 = 0
            for i in range(start+1, end):
                if (i < first) or (i > second):
                    pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
                    pixelCount = pixelCount + 1

            avgInt = pixelInt1 / pixelCount
            #print("avgInt: ", avgInt)
            #print("avgInt0 = ", avgInt0)

            if (avgInt <= 10):
                bottleTop = j - 25
                avgInt0 = 0
                break
            else:
                avgInt0 = avgInt

    for i in range(start+1, end):
        imGray[height - (bottom + 1), i] = 255
        imGray[height - (top + 1), i] = 255
        imGray[height - (bottleTop + 1), i] = 0

    pixelHeight = top - bottom
    bottleHeight = bottleTop - bottom
    print("Height of Liquid: ", pixelHeight)
    print("Height of Bottle: ", bottleHeight)

    heightRatio = 18/bottleHeight
    fluidHeight = pixelHeight * heightRatio
    fluidVolume = int((166.67 * fluidHeight))

    print("Fluid Volume: ", fluidVolume, "ml")

    if fluidVolume < 750:
        fluidVolume = "Needs to be filled"

    return fluidVolume

# Based on width of each bottle, run the big or small fluid detction function.

try:
    clip1S, clip1E = clips(imGray, width,height,b1Start,b1End)
    bottle1 = bigBottleDetection(imGray, height, b1Start, b1End, clip1S, clip1E)
    reagentNo1, reagent1 = reagentDetection(img, clip1S, clip1E, height)
    if type(bottle1) != str:
        toFill1 = 4800 - int(bottle1)
        if toFill1 < 0:
            toFill1 = "No Need to Fill"

    else:
        toFill1 = "Upto 4800 ml"

    #cv.imshow("Final", imGray)
    #cv.waitKey(0)

    clip2S, clip2E = clips(imGray, width,height,b2Start,b2End)
    bottle2 = smallBottleDetection(imGray, height, b2Start, b2End, clip2S, clip2E)
    reagentNo2, reagent2 = reagentDetection(img, clip2S, clip2E, height)
    if type(bottle2) != str:
        toFill2 = 2400 - int(bottle2)
        if toFill2 < 0:
            toFill2 = "No Need to Fill"
    else:
        toFill2 = "Upto 2400 ml"

    #cv.imshow("Final", imGray)
    #cv.waitKey(0)

    clip3S, clip3E = clips(imGray, width,height,b3Start,b3End)
    bottle3 = smallBottleDetection(imGray, height, b3Start, b3End, clip3S, clip3E)
    reagentNo3, reagent3 = reagentDetection(img, clip3S, clip3E, height)
    if type(bottle3) != str:
        toFill3 = 2400 - int(bottle3)
        if toFill3 < 0:
            toFill3 = "No Need to Fill"
    else:
        toFill3 = "Upto 2400 ml"

    #cv.imshow("Final", imGray)
    #cv.waitKey(0)

    clip4S, clip4E = clips(imGray, width,height,b4Start,b4End)
    bottle4 = bigBottleDetection(imGray, height, b4Start, b4End, clip4S, clip4E)
    reagentNo4, reagent4 = reagentDetection(img, clip4S, clip4E, height)
    if type(bottle4) != str:
        toFill4 = 4800 - int(bottle4)
        if toFill4 < 0:
            toFill4 = "No Need to Fill"
    else:
        toFill4 = "Upto 4800 ml"

    #cv.imshow("Final", imGray)
    #cv.waitKey(0)

    # Display the final picture with all the lines.

    cv.imshow("Final", imGray)
    cv.waitKey(0)

    # Export the dictionary to a csv file.
 
    dataDict = {
        "Date": [day] * 4,
        "Time": [time.strftime("%H:%M", time.localtime())] * 4,
        "Number": [reagentNo1, reagentNo2, reagentNo3, reagentNo4],
        "Reagent": [reagent1, reagent2, reagent3, reagent4],
        "Value": [bottle1, bottle2, bottle3, bottle4],
        "Fill": [toFill1, toFill2, toFill3, toFill4]
    }
    filename = "ULTRABulkReagents_Data.csv"
    df = pd.DataFrame(dataDict)
    df.to_csv("ULTRABulkReagents_Data.csv", mode = "a", index=False, header=True)


    table1 = [["Number", "Reagent", "Value", "Fill"], [reagentNo1, reagent1, bottle1, toFill1], [reagentNo2, reagent2, bottle2, toFill2], [reagentNo3, reagent3, bottle3, toFill3], [reagentNo4, reagent4, bottle4, toFill4]]
    print(tabulate(table1, headers = 'firstrow', tablefmt='fancy_grid'))

except IndexError:
    print("Unable to analyze. Volume might be too low")

cv.destroyAllWindows()
