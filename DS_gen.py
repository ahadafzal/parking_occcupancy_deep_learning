import numpy as np
import cv2
from drawing_utils import draw_contours


img = cv2.imread("cwing1.jpg")
coordinates = []
per_cor = []
click_count = 0
ids = 0

def mouse_callback(event, x, y, flags, params):
        global click_count,coordinates,ids,per_cor
        if event == cv2.EVENT_LBUTTONDOWN:
            coordinates.append((x, y))
            click_count += 1

            if click_count >= 4:
                handle_done()

            elif click_count > 1:
                handle_click_progress()

        cv2.imshow("img", img)


def handle_done():
        global click_count,coordinates,ids,per_cor
        cv2.line(img,
                     coordinates[2],
                     coordinates[3],
                     (0, 0, 255),
                     1)
        cv2.line(img,
                     coordinates[3],
                     coordinates[0],
                     (0, 0, 255),
                     1)

        click_count = 0

        # coordinates = np.array(coordinates)
        

        # output.write("-\n          id: " + str(self.ids) + "\n          coordinates: [" +
        #                   "[" + str(self.coordinates[0][0]) + "," + str(self.coordinates[0][1]) + "]," +
        #                   "[" + str(self.coordinates[1][0]) + "," + str(self.coordinates[1][1]) + "]," +
        #                   "[" + str(self.coordinates[2][0]) + "," + str(self.coordinates[2][1]) + "]," +
        #                   "[" + str(self.coordinates[3][0]) + "," + str(self.coordinates[3][1]) + "]]\n")

        draw_contours(img, np.array(coordinates), str(ids + 1),(255, 255, 255))
        per_cor.append(coordinates.copy())
        for i in range(0, 4):
            coordinates.pop()

        ids += 1



def handle_click_progress():
        global click_count,coordinates,ids,per_cor
        cv2.line(img, coordinates[-2], coordinates[-1], (255, 0, 0), 1)

cv2.namedWindow("img", cv2.WINDOW_GUI_EXPANDED)
cv2.setMouseCallback("img", mouse_callback)

while True:
        cv2.imshow("img", img)
        key = cv2.waitKey(1)


        if key & 0xFF == ord('q'):
                break


print(per_cor)
coordinates = np.array(per_cor)
i = 0
c = 25
while(i<len(coordinates)):
        rect = cv2.boundingRect(coordinates[i])
        new_coordinates = coordinates[i].copy()
        new_coordinates[:, 0] = coordinates[i][:, 0] - rect[0]
        new_coordinates[:, 1] = coordinates[i][:, 1] - rect[1]

        frame = cv2.imread("cwing1.jpg")
        cv2.imwrite("dataset/free/free"+str(c)+".jpg",frame[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])])
        i+=1
        c+=1




        
