# Team 23027 
# Created by: Divyansh Rathod
# Fluid Level Dection for Big Bottle


import numpy as np
import pandas as pd
import cv2  
from PIL import Image 
import matplotlib.pylab as plt
import os

path1 = " " # Path of Original Image

''' Use Gamma correction on the original image to further highlight the amount of liquid in the bottle '''

nat = cv2.imread(path1)
nat_2 = cv2.cvtColor(nat, cv2.COLOR_BGR2RGB)
cv2.imshow("", nat_2)
cv2.waitKey(0)

def gammaCorrection(src, gamma):
    invGamma = 1 / gamma

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(src, table)


gamma = 0.3      # change the value here to get different result
adjusted = gammaCorrection(nat_2, gamma=gamma)
cv2.imshow("", adjusted)
cv2.waitKey(0)

im = adjusted

''' Apply Thresholds and subtract two images to highlight the liquid inside the bottles'''

ret1, img1 = cv2.threshold(im, 20, 255, cv2.THRESH_BINARY)
cv2.imshow('Image1', img1)
cv2.waitKey(0)
ret2, img2 = cv2.threshold(im, 80, 255, cv2.THRESH_BINARY)
cv2.imshow('Image2', img2)
cv2.waitKey(0)
cv2.imshow('double_threshold', img1 - img2)
cv2.waitKey(0)

im = img1 -img2

directory = "" # Directory in which to save the thresholded image
os.chdir(directory)
cv2.imwrite("Threshold.jpg", im)

''' Load the image, get the pixel intensities and the number of pixels in the image'''

path2 = "" # Path of saved thresholded image
im = Image.open(path2)

pixel_map = im.load()
width, height = im.size
print("Height: ", height)
print("Width: ", width)

blackCount = 0
colorCount = 0

''' Run a for loop for each row of pixels starting from the bottom of the image, take a ratio of the number of black pixels and colored pixels.'''
''' Using the ratios, determine the top and bottom lines along with the top of the bottle '''

for j in range(height):
    for i in range(width):
        if pixel_map[i,(height - (j+1))] == (0,0,0):
            blackCount = blackCount + 1
        else:
            colorCount = colorCount + 1
    
    blackRatio = blackCount/(blackCount + colorCount)
    colorRatio = colorCount/(blackCount + colorCount)
    blackCount = 0
    colorCount = 0
    if (colorRatio >= 0.8):
        # print("Black Ratio: ", blackRatio)
        # print("Color Ratio: ", colorRatio)
        bottom = j
        break

for j in range(height):
    if (j >= bottom):
        for i in range(width):
            if pixel_map[i,(height - (j+1))] == (0,0,0):
                blackCount = blackCount + 1
            else:
                colorCount = colorCount + 1
        
        blackRatio = blackCount/(blackCount + colorCount)
        colorRatio = colorCount/(blackCount + colorCount)
        #print("Black Ratio: ", blackRatio)
        #print("Color Ratio: ", colorRatio)
        blackCount = 0
        colorCount = 0
        if (colorRatio <= 0.75):
            top = j
            break

for j in range(height):
    if (j >= top):
        for i in range(width):
            if pixel_map[i,(height - (j+1))] == (0,0,0):
                blackCount = blackCount + 1
            else:
                colorCount = colorCount + 1
        
        blackRatio = blackCount/(blackCount + colorCount)
        colorRatio = colorCount/(blackCount + colorCount)
        # print("Black Ratio: ", blackRatio)
        # print("Color Ratio: ", colorRatio)
        blackCount = 0
        colorCount = 0
        if (colorRatio >= 0.97):
            bottleTop = j
            break

for i in range(width):
    pixel_map[i,(height - (bottom+1))] = (0,0,255)  
    pixel_map[i,(height - (top+1))] = (255,0,0)
    pixel_map[i,(height - (bottleTop+1))] = (0,255,0)    

im.show()

im = Image.open(path1)

pixel_map = im.load()
width, height = im.size

''' Draw the top and bottom lines for both the thresholded image and the original image '''

for i in range(width):
    pixel_map[i,(height - (bottom+1))] = (0,0,255)  
    pixel_map[i,(height - (top+1))] = (255,0,0)
    pixel_map[i,(height - (bottleTop+1))] = (0,255,0)  

''' Use the various pixel values to calculate the height of the bottle and the liquid in terms of pixels and then conver it into ml'''  

pixelHeight = top - bottom
bottleHeight = bottleTop - bottom
print("Height of Liquid: ", pixelHeight)
print("Height of Bottle: ", bottleHeight)

heightRatio = 17.5/bottleHeight
fluidHeight = pixelHeight * heightRatio
fluidVolume = (389.2 * fluidHeight) - 224.41

print("Fluid Volume: ", fluidVolume, "ml")

im.show()