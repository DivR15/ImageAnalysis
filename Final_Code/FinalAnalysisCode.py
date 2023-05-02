# Team 23027 
# Created by: Divyansh Rathod
# Fluid Level Detection and Reagent Id for Multiple Bottles

# Import Libraries
import numpy as np
import cv2 as cv 
import os
import csv

img = cv.imread("Multi2B1S.jpg")
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
cv.imshow("", adjusted)
cv.waitKey(0)
cv.imwrite("Threshold.jpg", adjusted)

imGray = cv.cvtColor(adjusted, cv.COLOR_BGR2GRAY)
cv.imshow("", imGray)
cv.waitKey(0)

height, width= imGray.shape[:2]

print("Height: ", height)
print("Width: ", width)

# Find ratio of width of the bottles and draw the vertical lines identifying each bottle.

for i in range(width):
    color = 0
    color = color + imGray[int(height/2), i]
    if color >= 10:
        b1Start = i
        break

bigBRatio = int(width/3.65)
smallBRatio = int(width/6.35)
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

a = height/4.55
""" for i in range(width):
    imGray[int(a), i] = 255 """
cv.imshow("", imGray)
cv.waitKey(0)

# Identify the clips and draw lines

def clips(width, height, start, end):
    a = height/4.5
    for i in range(width):
        if (i > start) and (i < end):
            for b in range(start+1, end):
                color = 0
                color = color + imGray[int(a), b]
                if (color > 1):
                    first = b - 2
                    break

            for b in range(start+1, end):
                color = 0
                if (b > first + 5):
                    color = color + imGray[int(a), b]
                    # print("color: ", color)
                    if (color < 3):
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

def reagentDetection(first, second, height):
    h = int(height/4.7)
    pixelavg = [0,0,0]
    count = 0

    for w in range(first + 10, second - 15):
        pixelavg = pixelavg + img[h,w]
        img[h,w] = [0, 0, 0]
        count += 1
    pixelavg = pixelavg / count

    b, g, r = pixelavg
    print("r: ", int(r), "g: ", int(g), "b: ", int(b))

    if (r > 155) and (r < 170) and (g > 160) and (g < 170) and (b > 150) and (b < 165):
        reagentNo = 4
        reagent = "Reaction Buffer"
    elif (r > 0) and (r < 10) and (g > 60) and (g < 75) and (b > 60) and (b < 75):
        reagentNo = 5
        reagent = "Ultra CC1"
    elif (r > 170) and (r < 185) and (g > 70) and (g < 80) and (b > 20) and (b < 35):
        reagentNo = 6
        reagent = "Ultra CC2"
    elif (r > 35) and (r < 45) and (g > 35) and (g < 45) and (b > 38) and (b < 50):
        reagentNo = 7
        reagent = "Option"
    else:
        reagentNo = "Error"
        reagent = "Error"
    
    return reagentNo, reagent

    #cv.imshow("nat", nat)
    




# DEFINE FUNCTION: If the bottle width is corresponding to the big bottle, run the fluid detection for big bottle. Save the values in a dictionary and draw the lines.

def bigBottleDetection(height, start, end, first, second):
    for j in range(10, height):
        pixelCount = 0
        pixelInt1 = 0
        for i in range(start+1, end):
            pixelInt1 = pixelInt1 + imGray[height - (j+1), i]
            pixelCount = pixelCount + 1

        avgInt = pixelInt1 / pixelCount
        #print("avgInt: ", avgInt)
        #print("avgInt0 = ", avgInt0)

        if (avgInt >= 15):
            bottom = j
            avgInt0 = 0
            break
        else:
            avgInt0 = avgInt

    pixelInt1 = 0
    pixelCount = 0
    pixelCount2 = 0
    pixelInt2 = 0

    for j in range(height):
        if (j >= bottom + 100):
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
            print("Diff: ", diff)
            if (diff >= 5):
                top = j + 5
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
            #print("avgInt: ", avgInt)
            #print("avgInt0 = ", avgInt0)

            if (avgInt <= 36):
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

    heightRatio = 17/bottleHeight
    fluidHeight = pixelHeight * heightRatio
    fluidVolume = int((389.2 * fluidHeight) - 224.41)

    print("Fluid Volume: ", fluidVolume, "ml")
    print("width: ", width)
    print("Height: ", height)

    if fluidVolume < 1500:
        fluidVolume = "Needs to be filled"    

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
        #print("avgInt: ", avgInt)
        #print("avgInt0 = ", avgInt0)

        if (avgInt >= 12):
            bottom = j
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
        if (j >= bottom + 95):
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
            print("Diff: ", diff)
            if (diff >= 3):
                top = j + 5
                break
            diff = 0 
            
    pixelInt1 = 0
    pixelCount = 0
    avgInt0 = 0

    for j in range(height):
        if (j >= top + 15):
            pixelCount = 0
            pixelInt1 = 0
            for i in range(start+1, end):
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
    fluidVolume = int((166.67 * fluidHeight))

    print("Fluid Volume: ", fluidVolume, "ml")

    if fluidVolume < 750:
        fluidVolume = "Needs to be filled"

    return fluidVolume


# Based on width of each bottle, run the big or small fluid detction function.

clip1S, clip1E = clips(width,height,b1Start,b1End)
bottle1 = bigBottleDetection(height, b1Start, b1End, clip1S, clip1E)
reagentNo1, reagent1 = reagentDetection(clip1S, clip1E, height)
if type(bottle1) != str:
    toFill1 = 4800 - int(bottle1)
else:
    toFill1 = "Upto 4800 ml"

#cv.imshow("Final", imGray)
#cv.waitKey(0)

clip2S, clip2E = clips(width,height,b2Start,b2End)
bottle2 = smallBottleDetection(height, b2Start, b2End, clip2S, clip2E)
reagentNo2, reagent2 = reagentDetection(clip2S, clip2E, height)
if type(bottle2) != str:
    toFill2 = 2400 - int(bottle2)
else:
    toFill2 = "Upto 2400 ml"

#cv.imshow("Final", imGray)
#cv.waitKey(0)

clip3S, clip3E = clips(width,height,b3Start,b3End)
bottle3 = smallBottleDetection(height, b3Start, b3End, clip3S, clip3E)
reagentNo3, reagent3 = reagentDetection(clip3S, clip3E, height)
if type(bottle3) != str:
    toFill3 = 2400 - int(bottle3)
else:
    toFill3 = "Upto 2400 ml"

#cv.imshow("Final", imGray)
#cv.waitKey(0)

clip4S, clip4E = clips(width,height,b4Start,b4End)
bottle4 = bigBottleDetection(height, b4Start, b4End, clip4S, clip4E)
reagentNo4, reagent4 = reagentDetection(clip4S, clip4E, height)
if type(bottle4) != str:
    toFill4 = 4800 - int(bottle4)
else:
    toFill4 = "Upto 4800 ml"

#cv.imshow("Final", imGray)
#cv.waitKey(0)

# Display the fianl picture with all the lines.

cv.imshow("Final", imGray)
cv.waitKey(0)

# Export the dictionary to a csv file.

header = ["Number", "Reagent", "Value", "Fill"]
dataDict =  [{"Number": reagentNo1, "Reagent": reagent1, "Value" : bottle1, "Fill" : toFill1 },
{"Number": reagentNo2, "Reagent": reagent2, "Value" : bottle2, "Fill" : toFill2}, 
{"Number": reagentNo3, "Reagent": reagent3, "Value" : bottle3, "Fill" : toFill3}, 
{"Number": reagentNo4, "Reagent": reagent4, "Value" : bottle4, "Fill" : toFill4}]

filename = "ULTRABulkReagents_Data.csv"
with open(filename, "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    writer.writerows(dataDict)

cv.destroyAllWindows()
