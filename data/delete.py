import numpy as np
import cv2

coordinates = np.array([[391,212],[388,182],[489,189],[497,215]])

rect = cv2.boundingRect(coordinates)
new_coordinates = coordinates.copy()
new_coordinates[:, 0] = coordinates[:, 0] - rect[0]
new_coordinates[:, 1] = coordinates[:, 1] - rect[1]
print(coordinates)
print("\n\n")
print(new_coordinates)
print("\n\n")
print(rect)

img2 =  np.zeros((rect[3], rect[2]), dtype=np.uint8)
cv2.imwrite("np.jpg",img2)
img2 = cv2.imread("np.jpg")

global mask
status = [False]
l_c = 1.0
frame = cv2.imread("newo.jpg")
img = frame.copy()
mask = cv2.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=cv2.LINE_8)

while True:
    cv2.imshow("frame",img)
    cv2.rectangle(img,(rect[0],rect[1]),(rect[2],rect[3]),color=(0,0,255),thickness=2)
    cv2.circle(img,tuple(coordinates[0]),radius=1,color=(0,0,255),thickness=2)
    cv2.circle(img,tuple(coordinates[1]),radius=1,color=(0,0,255),thickness=2)
    cv2.circle(img,tuple(coordinates[2]),radius=1,color=(0,0,255),thickness=2)
    cv2.circle(img,tuple(coordinates[3]),radius=1,color=(0,0,255),thickness=2)

    cv2.circle(img,tuple(new_coordinates[0]),radius=1,color=(0,0,255),thickness=2)
    cv2.circle(img,tuple(new_coordinates[1]),radius=1,color=(0,255,0),thickness=2)
    cv2.circle(img,tuple(new_coordinates[2]),radius=1,color=(255,0,0),thickness=2)
    cv2.circle(img,tuple(new_coordinates[3]),radius=1,color=(0,0,0),thickness=2)
    cv2.drawContours(
                img,
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=cv2.LINE_8)

    mask = cv2.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=cv2.LINE_8)
    
    mask = mask == 255
    blurred = cv2.GaussianBlur(frame.copy(), (5, 5), 3)
    grayed = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)


    roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
    laplacian = cv2.Laplacian(roi_gray, cv2.CV_64F)
    # print(laplacian.shape,mask.shape)
    status = np.mean(np.abs(laplacian * mask)) < l_c
    print(np.mean(np.abs(laplacian * mask)))

    



    cv2.imshow("after mask", np.abs(laplacian * mask))
    cv2.imshow("OG_image",frame[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])])
    cv2.imshow("laplacian",laplacian)
    cv2.imshow("blurred",blurred)
    cv2.imshow("gray",grayed)
    cv2.imshow('frame2',img2)


    cv2.drawContours(
                img2,
                [new_coordinates],
                contourIdx=-1,
                color=(0,45,45),
                thickness=-1,
                lineType=cv2.LINE_8)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
print("mask:")
print(mask)
print("status: ",status)



##############
#captuer
#############

# import cv2

# cap = cv2.VideoCapture("rtsp:///192.168.0.100:8080/video/h264")
# ret,frame = cap.read()
# # cv2.("live.jpg",frame)

# while True:
#     ret,frame = cap.read()

#     cv2.imshow("nd",frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cv2.destroyAllWindows()
# cap.release()

##############
# live rtsp
###########
# import cv2 as cv
# vcap = cv.VideoCapture("rtsp://192.168.0.100:8080/video/h264")
# while(1):
#     ret, frame = vcap.read()
#     cv.imshow('VIDEO', frame)
#     cv.waitKey(1) & 0xFF == ord('q')        

# #rtsp://admin:admin123@149.129.132.29:554/cam/realmonitor?channel=0&subtype=0