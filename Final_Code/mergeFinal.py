from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd
import  os
import numpy as np
import cv2 as cv
import csv
from datetime import date
import time
import pandas as pd
#from tabulate import tabulate
import  matplotlib . pyplot  as  plt
from kivy.core.window import Window
Window.size = (850, 530)
from picamera import PiCamera 
from time import sleep
from pyhubctl import  PyHubCtl, Configuration

# class to call the popup function
class PopupWindow(Widget):
    def btn(self):
        popFun ()


# class to build GUI for a popup window
class P(FloatLayout):
    pass


# function that displays the Error message
def popFun():
    show = P()
    window = Popup(title="Error", content=show,
                   size_hint=(None, None), size=(300, 300))
    window.open()


# class to accept user info and validate it
class loginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def validate(self):

        # validating if the email already exists
        if self.email.text not in users['Email'].unique():
            popFun ()
        else:

            # switching the current screen to display validation result
            sm.current = 'logdata'

            # reset TextInput widget
            self.email.text = ""
            self.pwd.text = ""


# class to accept sign up info
class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def signupbtn(self):

        # creating a DataFrame of the info
        user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text]],
                            columns=['Name', 'Email', 'Password'])
        if self.email.text != "":
            if self.email.text not in users['Email'].unique():
                # if email does not exist already then append to the csv file
                # change current screen to log in the user now
                user.to_csv('login.csv', mode='a', header=False, index=False)
                sm.current = 'login'
                self.name2.text = ""
                self.email.text = ""
                self.pwd.text = ""
        else:
            # if values are empty or invalid show pop up
            popFun ()


# class to display validation result
class logDataWindow(Screen):
    pass

# class for analysis
class analysisWindow(Screen):
    ultraid = ObjectProperty(None)
    def dataanalysis(self):
        #LIGHTS ON
        phc = PyHubCtl()
        phc.run(Configuration(action="1", ports="2"))
        camera = PiCamera() 
        sleep(2)
        camera.capture('/home/pi/Desktop/Image Analysis/image.jpg')
        # Read File and Gamma Conversion.

        img = cv.imread("image.jpg")
        # cv.imshow("1", img)
        # cv.waitKey(0)
        #LIGHTS OFF
        phc = PyHubCtl()
        phc.run(Configuration(action="0", ports="2"))
        phc.run(Configuration(action="0", ports="2"))
        
        
        height, width = img.shape[:2]
        print("height: ", height)
        print("width: ", width)

        img = img[30:430, 130:690]
        #cv.imshow("2", img)
        #cv.waitKey(0)

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

        # cv.imshow("", nat_2)
        # cv.waitKey(0)

        def gammaCorrection(src, gamma):
            invGamma  =  1  /  gamma

            table = [((i / 255) ** invGamma) * 255 for i in range(256)]
            table = np.array(table, np.uint8)

            return cv.LUT(src, table)

        gamma = 0.70  # change the value here to get different result
        adjusted  =  gammaCorrection ( nat_2 , gamma = gamma )
        # cv.imshow("", adjusted)
        # cv.waitKey(0)
        cv.imwrite("Threshold.jpg", adjusted)

        imGray = cv.cvtColor(adjusted, cv.COLOR_BGR2GRAY)
        # cv.imshow("", imGray)
        # cv.waitKey(0)

        height, width = imGray.shape[:2]

        print("Height: ", height)
        print("Width: ", width)

        # Find ratio of width of the bottles and draw the vertical lines identifying each bottle.

        for  i  in  range ( width ):
            color = 0
            color = color + imGray[int(height / 2), i]
            if color >= 20:
                b1Start = i
                break

        bigBRatio = int(width / 3.60)
        smallBRatio = int(width / 6.50)
        # b1Start = int(width/20)
        b1End = b2Start = b1Start + bigBRatio
        b2End = b3Start = b1End + smallBRatio
        b3End = b4Start = b3Start + smallBRatio

        for  i  in  range ( width ):
            color = 0
            color = color + imGray[int(height / 2), width - i - 1]
            if color >= 20:
                b4End = i
        # b4End = b4Start + bigBRatio

        for  i  in  range ( height ):
            imGray[i, b1Start] = 255
            imGray[i, b1End] = 255
            imGray[i, b2End] = 255
            imGray[i, b3End] = 255
            imGray[i, b4End] = 255

        a = height / 4.85
        """ for i in range(width):
            imGray[int(a), i] = 255 """

        # cv.imshow("", imGray)
        # cv.waitKey(0)

        # Identify the clips and draw lines

        def clips(imGray, width, height, start, end):
            a = height / 4.85
            for  i  in  range ( width ):
                if (i > start) and (i < end):
                    for  b  in  range ( start  +  1 , end ):
                        color = 0
                        color = color + imGray[int(a), b]
                        if (color > 6):
                            first = b - 2
                            break

                    for  b  in  range ( start  +  1 , end ):
                        color = 0
                        if (b > first + 5):
                            color = color + imGray[int(a), b]
                            # print("color: ", color)
                            if (color < 6):
                                second = b + 2
                                # print("B: ", b)
                                break

            # print("START: ", start)
            # print("END: ", end)
            # print("FIRST: ", first)
            # print("SECOND: ", second)
            for  b  in  range ( height ):
                imGray[b, first] = 255
                imGray[b, second] = 255

            return first, second

        def reagentDetection(img, first, second, height):
            h = int(height / 5.85)
            pixelavg = [0, 0, 0]
            count = 0

            for w in range(first + 10, second - 10):
                pixelavg = pixelavg + img[h, w]
                img[h, w] = [0, 0, 0]
                count += 1
            pixelavg = pixelavg / count

            b, g, r = pixelavg
            print("r: ", int(r), "g: ", int(g), "b: ", int(b))

            if (r >= 35) and (r <= 65) and (g >= 90) and (g <= 140) and (b >= 50) and (b <= 85):
                reagentNo = 4
                reagent = "Reaction Buffer"
            elif (r >= 0) and (r <= 20) and (g >= 65) and (g <= 100) and (b >= 30) and (b <= 60):
                reagentNo = 5
                reagent = "Ultra CC1"
            elif (r >= 60) and (r <= 130) and (g >= 20) and (g <= 55) and (b >= 10) and (b <= 40):
                reagentNo = 6
                reagent = "Ultra CC2"
            elif (r >= 5) and (r <= 35) and (g >= 20) and (g <= 80) and (b >= 10) and (b <= 45):
                reagentNo = 7
                reagent = "Option"
            else:
                reagentNo = "Error"
                reagent = "Error"

            # cv.imshow("nat", img)
            # cv.waitKey(0)

            return reagentNo, reagent

        # DEFINE FUNCTION: If the bottle width is corresponding to the big bottle, run the fluid detection for big bottle. Save the values in a dictionary and draw the lines.

        def bigBottleDetection(imGray, height, start, end, first, second):
            for j in range(10, height):
                pixelCount = 0
                pixelInt1 = 0
                for i in range(start + 1, end):
                    pixelInt1 = pixelInt1 + imGray[height - (j + 1), i]
                    pixelCount = pixelCount + 1

                avgInt = pixelInt1 / pixelCount
                # print("avgInt: ", avgInt)
                # print("avgInt0 = ", avgInt0)

                if (avgInt >= 15):
                    bottom = j - 5

                    break

            pixelInt1 = 0
            pixelCount = 0
            pixelCount2 = 0
            pixelInt2 = 0

            for j in range(height):
                if (j >= bottom + 55):
                    pixelCount = 0
                    pixelInt1 = 0
                    pixelCount2 = 0
                    pixelInt2 = 0
                    for i in range(start + 1, end):
                        if (i < first) or (i > second):
                            if (imGray[height - (j + 1), i] >= 20) and (imGray[height - (j + 1), i] <= 120):
                                pixelInt1 = pixelInt1 + imGray[height - (j + 1), i]
                                pixelCount = pixelCount + 1
                            if (imGray[height - ((j + 5) + 1), i] >= 20) and (imGray[height - ((j + 5) + 1), i] <= 120):
                                pixelInt2 = pixelInt2 + imGray[height - ((j + 5) + 1), i]
                                pixelCount2 = pixelCount2 + 1

                    if (pixelCount != 0) and (pixelCount2 != 0):
                        avgInt1 = pixelInt1 / pixelCount
                        avgInt2 = pixelInt2 / pixelCount2

                    diff = abs(avgInt2 - avgInt1)
                    # print("Diff: ", diff)
                    if (diff >= 3):
                        if j > 250:
                            top = j + 5
                        else:
                            top = j + 10
                        break

            pixelInt1 = 0
            pixelCount = 0
            avgInt0 = 0

            for j in range(height):
                if (j >= top):
                    pixelCount = 0
                    pixelInt1 = 0
                    for i in range(start + 1, end):
                        if (i < first - 5) or (i > second + 5):
                            pixelInt1 = pixelInt1 + imGray[height - (j + 1), i]
                            pixelCount = pixelCount + 1

                    avgInt = pixelInt1 / pixelCount
                    # print("avgInt: ", avgInt)
                    # print("avgInt0 = ", avgInt0)

                    if (avgInt <= 10):
                        bottleTop = j - 30
                        avgInt0 = 0
                        break
                    else:
                        avgInt0 = avgInt

            for i in range(start + 1, end):
                imGray[height - (bottom + 1), i] = 255
                imGray[height - (top + 1), i] = 255
                imGray[height - (bottleTop + 1), i] = 0

            pixelHeight = top - bottom
            bottleHeight = bottleTop - bottom
            print("Height of Liquid: ", pixelHeight)
            print("Height of Bottle: ", bottleHeight)

            heightRatio = 17 / bottleHeight
            fluidHeight = pixelHeight * heightRatio
            fluidVolume = int((368.96 * fluidHeight) - 209.68)

            print("Fluid Volume: ", fluidVolume, "ml")
            print("Fluid Height: ", fluidHeight)
            print("width: ", width)
            print("Height: ", height)

            if fluidVolume <= 1200:
                fluidVolume = "Unable to analyze. Volume might be too low or too high"

            return fluidVolume

        # DEFINE FUNCTION:Repeat the same for the small bottle with the small bottle code.

        def smallBottleDetection(imGray, height, start, end, first, second):
            avgInt0 = 0
            for j in range(height):
                pixelCount = 0
                pixelInt1 = 0
                for i in range(start + 1, end):
                    if (imGray[height - (j + 1), i] < 255):
                        pixelInt1 = pixelInt1 + imGray[height - (j + 1), i]
                        pixelCount = pixelCount + 1

                avgInt = pixelInt1 / pixelCount
                # print("avgInt: ", avgInt)
                # print("avgInt0 = ", avgInt0)

                if (avgInt >= 25):
                    bottom = j - 5
                    # print("Bottom: ", bottom)
                    avgInt0 = 0
                    break
                else:
                    avgInt0 = avgInt

            pixelInt1 = 0
            pixelCount = 0
            pixelCount2 = 0
            pixelInt2 = 0

            for j in range(height):
                if (j >= bottom + 65):
                    pixelCount = 0
                    pixelInt1 = 0
                    pixelInt2 = 0
                    pixelCount2 = 0
                    for i in range(start + 1, end):
                        if (i < first) or (i > second):
                            if (imGray[height - (j + 1), i] >= 20) and (imGray[height - (j + 1), i] <= 120):
                                pixelInt1 = pixelInt1 + imGray[height - (j + 1), i]
                                pixelCount = pixelCount + 1
                            if (imGray[height - ((j + 10) + 1), i] >= 20) and (
                                    imGray[height - ((j + 10) + 1), i] <= 120):
                                pixelInt2 = pixelInt2 + imGray[height - ((j + 5) + 1), i]
                                pixelCount2 = pixelCount2 + 1

                    if (pixelCount != 0) and (pixelCount2 != 0):
                        avgInt1 = pixelInt1 / pixelCount
                        avgInt2 = pixelInt2 / pixelCount2

                    diff = abs(avgInt2 - avgInt1)
                    # print("Diff: ", diff)
                    if (diff >= 2.2):
                        if j < 100:
                            top = j
                        else:
                            top = j + 10
                        break

            pixelInt1 = 0
            pixelCount = 0
            avgInt0 = 0

            for j in range(height):
                if (j >= top + 15):
                    pixelCount = 0
                    pixelInt1 = 0
                    for i in range(start + 1, end):
                        if (i < first) or (i > second):
                            pixelInt1 = pixelInt1 + imGray[height - (j + 1), i]
                            pixelCount = pixelCount + 1

                    avgInt = pixelInt1 / pixelCount
                    # print("avgInt: ", avgInt)
                    # print("avgInt0 = ", avgInt0)

                    if (avgInt <= 10):
                        bottleTop = j - 25
                        avgInt0 = 0
                        break
                    else:
                        avgInt0 = avgInt

            for i in range(start + 1, end):
                imGray[height - (bottom + 1), i] = 255
                imGray[height - (top + 1), i] = 255
                imGray[height - (bottleTop + 1), i] = 0

            pixelHeight = top - bottom
            bottleHeight = bottleTop - bottom
            print("Height of Liquid: ", pixelHeight)
            print("Height of Bottle: ", bottleHeight)

            heightRatio = 18 / bottleHeight
            fluidHeight = pixelHeight * heightRatio
            fluidVolume = int((176.48 * fluidHeight) - 84.63)

            print("Fluid Volume: ", fluidVolume, "ml")
            print("Fluid Height: ", fluidHeight)

            if fluidVolume <= 650:
                fluidVolume = "Unable to analyze. Volume might be too low or too high"

            return fluidVolume

        # Based on width of each bottle, run the big or small fluid detction function.

        try:
            clip1S, clip1E = clips(imGray, width, height, b1Start, b1End)
            reagentNo1, reagent1 = reagentDetection(img, clip1S, clip1E, height)
            bottle1 = bigBottleDetection(imGray, height, b1Start, b1End, clip1S, clip1E)
            if type(bottle1) != str:
                toFill1 = 4800 - int(bottle1)
                if toFill1 < 0:
                    toFill1 = "No Need to Fill"

            else:
                toFill1 = "Upto 4800 ml"

        except (IndexError, UnboundLocalError) as error:
            clip1S, clip1E = clips(imGray, width, height, b1Start, b1End)
            reagentNo1, reagent1 = reagentDetection(img, clip1S, clip1E, height)
            bottle1 = "Unable to analyze. Volume might be too low or too high"
            toFill1 = "Upto 4800 ml"

            # cv.imshow("Final", imGray)
            # cv.waitKey(0)

        try:
            clip2S, clip2E = clips(imGray, width, height, b2Start, b2End)
            bottle2 = smallBottleDetection(imGray, height, b2Start, b2End, clip2S, clip2E)
            reagentNo2, reagent2 = reagentDetection(img, clip2S, clip2E, height)
            if type(bottle2) != str:
                toFill2 = 2400 - int(bottle2)
                if toFill2 < 0:
                    toFill2 = "No Need to Fill"
            else:
                toFill2 = "Upto 2400 ml"

        except (IndexError, UnboundLocalError) as error:
            clip2S, clip2E = clips(imGray, width, height, b2Start, b2End)
            reagentNo2, reagent2 = reagentDetection(img, clip2S, clip2E, height)
            bottle2 = "Unable to analyze. Volume might be too low or too high"
            toFill2 = "Upto 2400 ml"

        # cv.imshow("Final", imGray)
        # cv.waitKey(0)

        try:
            clip3S, clip3E = clips(imGray, width, height, b3Start, b3End)
            bottle3 = smallBottleDetection(imGray, height, b3Start, b3End, clip3S, clip3E)
            reagentNo3, reagent3 = reagentDetection(img, clip3S, clip3E, height)
            if type(bottle3) != str:
                toFill3 = 2400 - int(bottle3)
                if toFill3 < 0:
                    toFill3 = "No Need to Fill"
            else:
                toFill3 = "Upto 2400 ml"

        except (IndexError, UnboundLocalError) as error:
            clip3S, clip3E = clips(imGray, width, height, b3Start, b3End)
            reagentNo3, reagent3 = reagentDetection(img, clip3S, clip3E, height)
            bottle3 = "Unable to analyze. Volume might be too low or too high"
            toFill3 = "Upto 2400 ml"

        # cv.imshow("Final", imGray)
        # cv.waitKey(0)

        try:
            clip4S, clip4E = clips(imGray, width, height, b4Start, b4End)
            bottle4 = bigBottleDetection(imGray, height, b4Start, b4End, clip4S, clip4E)
            reagentNo4, reagent4 = reagentDetection(img, clip4S, clip4E, height)
            if type(bottle4) != str:
                toFill4 = 4800 - int(bottle4)
                if toFill4 < 0:
                    toFill4 = "No Need to Fill"
            else:
                toFill4 = "Upto 4800 ml"

        except (IndexError, UnboundLocalError) as error:
            clip4S, clip4E = clips(imGray, width, height, b4Start, b4End)
            reagentNo4, reagent4 = reagentDetection(img, clip4S, clip4E, height)
            bottle4 = "Unable to analyze. Volume might be too low or too high"
            toFill4 = "Upto 4800 ml"
        # cv.imshow("Final", imGray)
        # cv.waitKey(0)

        # Display the final picture with all the lines.

        #cv.imshow("Final", imGray)
        #cv.waitKey(0)

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
        df.to_csv("ULTRABulkReagents_Data.csv", mode="a", index=False, header=True)
        table1 = [["Number", "Reagent", "Value", "Fill"], [reagentNo1, reagent1, bottle1, toFill1],
                  [reagentNo2, reagent2, bottle2, toFill2], [reagentNo3, reagent3, bottle3, toFill3],
                  [reagentNo4, reagent4, bottle4, toFill4]]
        #print(tabulate(table1, headers='firstrow', tablefmt='fancy_grid'))

        title_text = 'Fluid Volume Data'
        footer_text = str(day) + "_" + str(time) + "_data"
        fig_background_color = 'black'
        fig_border = 'white'

        data = [['Measured (mL)', 'To be filled (mL)'],
                [reagent1, bottle1, toFill1],
                [reagent2, bottle2, toFill2],
                [reagent3, bottle3, toFill3],
                [reagent4, bottle4, toFill4],
                ]

        column_headers = data.pop(0)
        row_headers = [x.pop(0) for x in data]

        cell_text = []
        for row in data:
            cell_text.append([str(x) for x in row])

        # Create the figure. Setting a small pad on tight_layout
        # seems to better regulate white space. Sometimes experimenting
        # with an explicit figsize here can produce better outcome.
        plt.figure(linewidth=1,
                   edgecolor=fig_border,
                   facecolor=fig_background_color,
                   # tight_layout={'pad':2},
                   figsize=(10, 4)
                   )

        # Get some lists of color specs for row and column headers
        rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
        ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))

        # Add a table at the bottom of the axes
        the_table = plt.table(cellText=cell_text,
                              rowLabels=row_headers,
                              rowColours=rcolors,
                              rowLoc='right',
                              colColours=ccolors,
                              colLabels=column_headers,
                              loc='center')

        # Scaling is the only influence we have over top and bottom cell padding.
        # Make the rows taller (i.e., make cell y scale larger).
        the_table.scale(1, 1.5)
        # Hide axes
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        # Hide axes border
        plt.box(on=None)
        # Add title
        plt.suptitle(title_text)
        # Add footer
        plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=6, weight='light')
        # Force the figure to update, so backends center objects correctly within the figure.
        # Without plt.draw() here, the title will center on the axes and not the figure.
        plt.draw()
        # Create image. plt.savefig ignores figure edge and face colors, so map them.
        fig = plt.gcf()
        plt.savefig("data",
                    # bbox='tight',
                    edgecolor=fig.get_edgecolor(),
                    facecolor=fig.get_facecolor(),
                    dpi=150
                    )
        plt.savefig(str(day) + "_" + str(time_) + "_data",
                    # bbox='tight',
                    edgecolor=fig.get_edgecolor(),
                    facecolor=fig.get_facecolor(),
                    dpi=150
                    )

        #plt.show()
        #LIGHTS ON
        phc.run(Configuration(action="1", ports="2"))
        cv.destroyAllWindows()

    pass

# class for post processing options
class postpWindow(Screen):
    pass

# class for managing screens
class dataWindow(Screen):
    pass

# class for managing screens
class windowManager(ScreenManager):
    pass


# kv file
kv = Builder.load_file('my3.kv')
sm = windowManager()

# reading all the data stored
users = pd.read_csv('login.csv')

# adding screens
sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))
sm.add_widget(analysisWindow(name='analysis'))
sm.add_widget(dataWindow(name='data'))
sm.add_widget(postpWindow(name='postp'))




# class that builds gui
class loginMain(App):
    def build(self):
        return sm


# driver function
if __name__ == "__main__":
    loginMain().run()
    pass


kv = Builder.load_file("my3.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
