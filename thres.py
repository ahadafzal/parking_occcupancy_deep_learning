import cv2 as open_cv
import numpy as np
import logging
from drawing_utils import draw_contours
from colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE,COLOR_RED
from firebase import firebase


class Thresholder:
    
    def __init__(self, image, coordinates):
        self.coordinates_data = coordinates
        self.contours = []
        self.bounds = []
        self.image = open_cv.imread(image)
        self.mask = []
        self.threshold = []
        # self.fire = firebase.FirebaseApplication("https://newone-9aa60.firebaseio.com/")
    
    def generate_threshold(self):
        coordinates_data = self.coordinates_data
        logging.debug("coordinates data: %s", coordinates_data)
        print(coordinates_data)
        for p in coordinates_data:
            print("gjh hhj ",coordinates_data)
            coordinates = self._coordinates(p)
            logging.debug("coordinates: %s", coordinates)

            rect = open_cv.boundingRect(coordinates)
            logging.debug("rect: %s", rect)

            new_coordinates = coordinates.copy()
            new_coordinates[:, 0] = coordinates[:, 0] - rect[0]
            new_coordinates[:, 1] = coordinates[:, 1] - rect[1]
            logging.debug("new_coordinates: %s", new_coordinates)

            self.contours.append(coordinates)
            self.bounds.append(rect)

            mask = open_cv.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=open_cv.LINE_8)

            mask = mask == 255
            self.mask.append(mask)
            blurred = open_cv.GaussianBlur(self.image, (5, 5), 3)
            grayed = open_cv.cvtColor(blurred, open_cv.COLOR_BGR2GRAY)
            
            # print("sfasdf________________________________________________")
            # open_cv.imshow("some",grayed)

        for index, c in enumerate(coordinates_data):
            threshold = self.__apply(grayed, index, c)
            self.threshold.append(threshold)
            

        return self.threshold




    def __apply(self, grayed, index, p):
        coordinates = self._coordinates(p)
        logging.debug("points: %s", coordinates)

        rect = self.bounds[index]
        logging.debug("rect: %s", rect)

        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian = open_cv.Laplacian(roi_gray, open_cv.CV_64F)
        logging.debug("laplacian: %s", laplacian)

        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        threshold = np.mean(np.abs(laplacian * self.mask[index]))
        return threshold

    @staticmethod
    def _coordinates(p):
        return np.array(p["coordinates"])