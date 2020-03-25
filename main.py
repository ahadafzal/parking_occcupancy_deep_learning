import argparse
import yaml
from coordinates_generator import CoordinatesGenerator
from motion_detector import MotionDetector
from colors import *
import logging
from firebase import firebase
from thres import Thresholder

global fire
fire = firebase.FirebaseApplication("https://newone-9aa60.firebaseio.com/")
geos = [19.0215936,72.8685476]
location_id = "col-1"
# fire.put("/location")


def main():
    global fire
    logging.basicConfig(level=logging.INFO)

    args = parse_args()

    image_file = args.image_file
    data_file = args.data_file
    start_frame = args.start_frame

    if image_file is not None:
        with open(data_file, "w+") as points:
            generator = CoordinatesGenerator(image_file, points, COLOR_RED)
            generator.generate()
            

            
        # insert new entry in firebase

        with open(data_file,"r") as data:
            dic = yaml.load(data)
            c_points = []
            status = []
            for l in dic:
                print(l["coordinates"])
                p = ''
                for j in range(4):
                    for k in range(2):
                        p += str(l["coordinates"][j][k])
                        p += ","
                    p += " "
                p += p[:p.find(" ")-1]
                c_points.append([p])
                status.append(False)

            datum = {
                "geo_points" : [19.0215936,72.8685476],
                "loc_id" : "col-1",
                "slot_details" : {
                    "coords" : c_points,
                    "status" : status
                },
                "system_state" : "active"
                }
            print(datum)
            fire.put("/location","test_loc",datum)




    with open(data_file, "r") as data:
        points = yaml.load(data)
        thresholder = Thresholder(image_file,points)
        thresholds = thresholder.generate_threshold()
        print("thresdfsal", thresholds)
        detector = MotionDetector(args.video_file, points, int(start_frame),thresholds)
        detector.detect_motion()


def parse_args():
    parser = argparse.ArgumentParser(description='Generates Coordinates File')

    parser.add_argument("--image",
                        dest="image_file",
                        required=False,
                        help="Image file to generate coordinates on")

    parser.add_argument("--video",
                        dest="video_file",
                        required=True,
                        help="Video file to detect motion on")

    parser.add_argument("--data",
                        dest="data_file",
                        required=True,
                        help="Data file to be used with OpenCV")

    parser.add_argument("--start-frame",
                        dest="start_frame",
                        required=False,
                        default=1,
                        help="Starting frame on the video")

    return parser.parse_args()


if __name__ == '__main__':
    main()
