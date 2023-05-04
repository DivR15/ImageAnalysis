# Fill-E Analysis and GUI System

Image analysis for fluid detection and volume estimation of Benchmark ULTRA reagent bottles. Users will interact with analysis functionality via a GUI touchscreen.

## Table of contents
* [General Info](#general-info)
* [Features](#features)
* [Setup and Basic Use](#setup)
* [Dependencies](#dependencies)
* [Scope and Status](#scope-and-status)

## General Info
This is a collection of all related software for the Fill-E system for use in the analysis of reagent bottles in Benchmark ULTRA systems by Roche Diagnostics. 

## Features
- GUI to interact with analysis functionality
- Storage of analysis data
- Login system

For analysis of Big and Small Bottles:
- Gamma Correction: makes the liquid look darker
- Pixel Intensity Averaging: takes an average of all the pixel intensities in a row
- Thresholding: draws a line for the bottom of the bottle, top of the bottle and at the fluid level

## Setup and Basic Use
Once the repository is downloaded, there are two main components to the code inside the `Final_Code` folder: the analysis code via `FinalAnalysisCode.py` in the `Analysis Code` folder, and `mergeFinal.py`, which includes the system peripherals (and is the program that is used by the system).

### `Analysis Code`
Here, the analysis code can be tested indepdently from the GUI for accuracy testing of fluid level estimation or editing of `FinalAnalysisCode.py`. The folder contains the latter, as well as several images to perform tests on. Before using any software within the repository, ensure the proper [Dependencies](#dependencies) are downloaded and applied.

Firstly, the record system of each image is

```TestX_XXBY_YYS.jpg```

where `X_XX` denotes the volume of the big bottle in liters, and `Y_YY` the volume of the small bottle -- the underscore represents a decimal point; for example,

```Test2_5B1_25S.jpg```

means that the image contains big bottles filled to 2.5 L, and small bottles filled to 1.25 L.

To analyze a test image, open the source code for `FinalAnalysisCode.py`. Below the package imports, there is this snippet of code:

```py
# Read File and Gamma Conversion.

img = cv.imread("##########") # Add name and directory of image to be analyzed here
```

Replace the string of pound signs with the filename of the image to be tested, including its file extensions; e.g.,

```py
# Read File and Gamma Conversion.

img = cv.imread("Test2_5B1_25S.jpg") # Analyze 2.5 L big bottles; 1.25 L small bottles
```

Run the code to have the chosen image analyzed.

### `mergeFinal.py`

This is the main file that the system runs, and combines the analysis code along with the GUI so that once the program is opened, technicians need only interact with the GUI in order to access the system's functionality. Note that `mergeFinal.py` requires `my3.kv` to function. Also note that the system itself runs on an identical but differently named `merge.py`. Please see the provided manual for further information about the use of the system.

## Dependencies

### Libraries:
- [Numpy](https://github.com/numpy/numpy)
- [OpenCV](https://github.com/abidrahmank/OpenCV2-Python-Tutorials)
- [Os](https://docs.python.org/3/library/os.html)
- [Kivy](https://github.com/kivy/kivy)
- [Pandas](https://github.com/pandas-dev/pandas)
- [CSV](https://docs.python.org/3/library/csv.html)
- [PiCamera](https://github.com/waveform80/picamera)
- [Matplotlib](https://github.com/matplotlib/matplotlib)
- [Datetime](https://docs.python.org/3/library/datetime.html)
- [Time](https://docs.python.org/3/library/time.html)
- [Pyhubctl](https://github.com/DuraTech-Industries/pyhubctl)

### Hardware:
Please see the Software Design Document for more detail on hardware.
- Raspberry Pi 3
- Raspberry Pi-compatible tablet
- LED strip (RGB, with 3 pin JST-SM connectors and separated +5V/GND wires)
- Raspberry Pi Camera (12 MP)
	- 6 mm focal lens

## Scope and Status
After much testing, the system is ready to be implemented. Integration between the analysis code, the GUI code, and the system peripherals is done, promising a useful design that will serve technicians with much alleviated time and effort. After the basics of the system are determined, the benefits of the system will become apparent.

Currently, the repository is designed to analyze four bottles -- specifically those within a provided simulation cart. The code is made with scalability in mind, and the system may be modified to analyze more bottles (or less!), with those interested in seeing the strengths and limits of the fluid estimation through the `Analysis Code` folder.
