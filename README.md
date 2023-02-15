# Fill-E Analysis and GUI System

Image analysis for fluid detection and volume estimation of Benchmark ULTRA reagent bottles. Users will interact with analysis functionality via a GUI touchscreen.

## Table of contents
* [General Info](#general-info)
* [Features](#features)
* [Setup](#setup)
* [Screenshots and Figures](#screenshots-and-figures)
* [Dependencies](#dependencies)
* [Scope and Status](#scope-and-status)

## General Info
This is a collection of all related software for the Fill-E system for use in the analysis of reagent bottles in Benchmark ULTRA systems by Roche Diagnostics. 

## Features
- GUI to interact with analysis functionality
- Temporary and permanent storage of analysis data
- Login system

For images of Big and Small Bottles:
- Gamma Correction: makes the liquid look darker
- Pixel Intensity Averaging: takes an average of all the pixel intensities in a row
- Thresholding: draws a line for the bottom of the bottle, top of the bottle and at the fluid level

## Setup
The code is currently in progress and will have additional hardware dependencies. As such, the only file that will have any tractable use on a computer would be the image analysis.

For the image analysis,

- Download required packages (see [Dependencies](#dependencies))
- Install repository and unzip
- Run the program to view analysis of example images

## Screenshots and Figures
To be updated
## Dependencies
Libraries:
- Numpy
- OpenCV
- Image
- Os
- kivy

Hardware:
- Raspberry Pi 3
- Raspberry Pi-compatible tablet
- LED strip (RGB, with 3 pin JST-SM connectors and separated +5V/GND wires)
- Raspberry Pi Camera (12 MP)
	- 6 mm focal lens

## Scope and Status
Currently, the repository deals with the analysis of a given picture which is in a file. In the final rendition of the system, the camera will provide the software with the image which will be overwritten with every analysis.

Additionally, the repo has a GUI which will allow the user to use the program and interact with its main functions, on top of having other functionalities, such as analysis result storage and a login system. 

The system will, at its greatest scope, include several hardware dependencies which will be reflected in the software content (see [Dependencies](#dependencies))
