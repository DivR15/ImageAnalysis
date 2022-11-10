import cv2
from matplotlib import pyplot as plt
import imutils
from PIL import Image
import os
import numpy

path1 = "" # Path of Original Image
im = cv2.imread(path1)

''' Apply Thresholds and subtract two images to highlight the liquid inside the bottles'''

ret1, img1 = cv2.threshold(im, 100, 255, cv2.THRESH_BINARY)
cv2.imshow('Image1', img1)
cv2.waitKey(0)
ret2, img2 = cv2.threshold(im, 195, 255, cv2.THRESH_BINARY)
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
''' Using the ratios, determine the top and bottom lines '''

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
        #print("Black Ratio: ", blackRatio)
        #print("Color Ratio: ", colorRatio)
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
        if (colorRatio <= 0.58):
            top = j
            break


''' Draw the top and bottom lines for both the thresholded image and the original image '''

for i in range(width):
    pixel_map[i,(height - (bottom+1))] = (0,0,255)  
    pixel_map[i,(height - (top+1))] = (255,0,0)    

im.show()

im = Image.open(path1)

pixel_map = im.load()
width, height = im.size

for i in range(width):
    pixel_map[i,(height - (bottom+1))] = (0,0,255)  
    pixel_map[i,(height - (top+1))] = (255,0,0)    

print("Height of Liquid: ", (top - bottom))

im.show()
