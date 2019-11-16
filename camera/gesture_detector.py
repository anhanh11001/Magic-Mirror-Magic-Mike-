import cv2
from picamera import PiCamera
import numpy as np

class GestureDetector:
    
    def __init__(self):
        self.lower = np.array([0, 69, 60], dtype="uint8")  # 0 , 48, 80
        self.upper = np.array([205, 155, 213], dtype="uint8")  # 20,255,255
        self.center_flag = False
        self.box = ((90,60),(230,180)) # (250,160),(410,320)
        self.face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')
        self.camera = PiCamera()
        self.camera.resolution = (320, 240)
        self.camera.framerate = 30
        self.status = 0 # 0-NOTHING 1-LEFT 2-RIGHT
        
    def handle_image(self):
        # Get RGB image from PiCamera
        img = np.empty((240, 320, 3), dtype=np.uint8)
        self.camera.capture(img, 'bgr')
        # Remove the face by replacing it with white square
        #img = self.remove_face(img)
        # Detect hand by skin detection
        skin = self.get_hand(img)
        cv2.imshow("Img", skin)
        # Find the greatest contour (hand):
        contours, _ = cv2.findContours(skin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_max, area = get_max_contour(contours)
        # Draw the center box
        center_x, center_y = self.get_hand_center_point(contour_max, area)
        if center_x is not None:
            # Set up swiping left right to the app.
            if not self.center_flag:
                if self.box[1][0] > center_x > self.box[0][0] and self.box[0][1] < center_y < self.box[1][1]:
                    self.center_flag = True
            else:
                if center_x > self.box[1][0]:
                    self.status = 2
                    self.center_flag = False
                elif center_x < self.box[0][0]:
                    self.status = 1
                    self.center_flag = False
                    
    def get_hand(self, img):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        skin_region = cv2.inRange(img_hsv, self.lower, self.upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        skin_region = cv2.erode(skin_region, kernel, iterations=2)
        skin_region = cv2.dilate(skin_region, kernel, iterations=2)
        skin_region = cv2.GaussianBlur(skin_region, (3, 3), 0)
        return skin_region

    def get_hand_center_point(self, contour, contour_area):
        if contour is None or contour_area < 10000:
            return None, None

        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        first_point = box[1]
        second_point = box[3]
        center_x = int((second_point[0] - first_point[0]) / 2) + first_point[0]
        center_y = int((second_point[1] - first_point[1]) / 2) + first_point[1]

        return center_x, center_y
    
    def remove_face(self, img):
        extended_range = 20

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(img_gray, 1.1, 5)
        for face in faces:
            cv2.rectangle(img,
                          (face[0] - extended_range, face[1] - extended_range),
                          (face[0] + face[2] + extended_range, face[1] + face[3] + extended_range),
                          (255, 255, 255), cv2.FILLED)
        return img
        

# Helper functions
def get_max_contour(contours):
    cont_max_area = 0
    cont_max_ind = -1
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if area > cont_max_area:
            cont_max_area = area
            cont_max_ind = i
    if cont_max_ind == -1:
        return None, cont_max_area
    else:
        return contours[cont_max_ind], cont_max_area