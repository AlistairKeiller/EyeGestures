import cv2
import dlib
import math
import time
import queue
import pickle
import random
import numpy as np
from typing import Callable, Tuple
from eyeGestures.gazeestimator import GazeTracker
from eyeGestures.calibration import Calibration


class EyeGestures:

    def __init__(self,height,width):
        self.width  = width
        self.height = height

        self.gaze = GazeTracker(width,height)
        self.calibrated = False

        self.calibration = Calibration(self.height, self.width, 60)
        pass

    def __onCalibrated(self):
        self.gaze.fit()
        self.calibrated = True

    def calibrate(self,image):
        if(not self.calibrated and not self.calibration.inProgress()):
            self.calibration.start(self.__onCalibrated)

        point = self.calibration.getTrainingPoint()
        self.gaze.calibrate(point,image)
        
        if len(self.gaze.getCalibration()[0]) > 10:
            self.gaze.fit()
            self.calibrated = True

        return point 

    def getFeatures(self,image):
        return self.gaze.getFeatures(image)

    def getHeadDirection(self):
        return self.gaze.getHeadDirection()

    def isCalibrated(self):
        return self.calibrated and not self.calibration.inProgress()

    def estimate(self,image):
        return self.gaze.estimate(image)
