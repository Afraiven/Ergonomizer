import cv2
import win10toast
import time
import sys
import os
import json


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except (ValueError, Exception):
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def mid_point(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


class BlinkDetector:
    def __init__(self, is_polish=True):

        if is_polish:
            self.text = "MRUGNIECIE"
            self.size = 1.5
        else:
            self.text = "BLINK"
            self.size = 3

        self.go = True

        self.right_eye_ver_line = None
        self.cap = cv2.VideoCapture(0)
        self.toaster = win10toast.ToastNotifier()
        file = open(resource_path(r'.\img\settings.json'))
        values = json.load(file)
        file.close()
        self.calibration_value = values['wsk']
        self.diagonal_value = values['dgn']

        self.left_eye_blink = False
        self.right_eye_blink = False

        self.left_eye_horizontal = 999
        self.right_eye_horizontal = 999

        self.blink_count = 0
        self.distance_count = 0

        self.detector = None
        self.predictor = None

        self.left_eye_left_point = None
        self.left_eye_right_point = None
        self.left_eye_center_top = None
        self.left_eye_center_bottom = None
        self.right_eye_left_point = None
        self.right_eye_right_point = None
        self.right_eye_center_top = None
        self.right_eye_center_bottom = None
        self.left_eye_hor_line = None
        self.left_eye_ver_line = None
        self.right_eye_hor_line = None
        self.landmarks = None

        self.ret, self.frame = self.cap.read()

        self.toast_shown = -999

    def check_if_not_too_close(self):
        if self.diagonal_value == 15:
            too_close = 220
        elif self.diagonal_value == 17:
            too_close = 180
        elif self.diagonal_value == 19:
            too_close = 160
        elif self.diagonal_value == 21:
            too_close = 160
        elif self.diagonal_value == 22:
            too_close = 140
        else:
            too_close = 125

        try:
            if self.landmarks.part(15).x - self.landmarks.part(1).x > too_close and\
                    self.toast_shown + 3 < time.perf_counter():
                self.distance_count += 1
                self.toast_shown = time.perf_counter()
                self.toaster.show_toast("Engonomizer", 'Jesteś za blisko ekranu !', duration=3, threaded=True)
        except (ValueError, Exception):
            pass

    def check_if_blinks(self):
        try:
            if self.left_eye_center_bottom[1] - self.left_eye_center_top[1] < self.left_eye_horizontal /\
                    self.calibration_value or \
                    self.right_eye_center_bottom[1] - self.right_eye_center_top[1] < self.right_eye_horizontal /\
                    self.calibration_value:
                self.left_eye_blink = True
            else:
                if self.left_eye_blink:
                    self.blink_count += 1
                    cv2.putText(
                        self.frame,
                        self.text,
                        (self.left_eye_center_bottom[0]-100, self.left_eye_center_bottom[1]-100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        self.size,
                        (0, 0, 255, 255),
                        3)
                    print(self.blink_count)
                    print(time.perf_counter()/60)
                elif self.right_eye_blink:
                    self.blink_count += 1
                    cv2.putText(
                        self.frame,
                        "BLINK",
                        (self.left_eye_center_bottom[0]-100, self.left_eye_center_bottom[1]-100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        3,
                        (0, 0, 255, 255),
                        3)
                    print(self.blink_count)
                    print(time.perf_counter()/60)
                self.right_eye_blink = False
                self.left_eye_blink = False

        except (ValueError, Exception):
            pass

    def working(self):
        if self.go:
            self.ret, self.frame = self.cap.read()
            self.frame = cv2.flip(self.frame, 1)
            try:
                faces = self.detector(self.frame)
                for face in faces:
                    self.landmarks = self.predictor(self.frame, face)

                    self.left_eye_left_point = (self.landmarks.part(36).x, self.landmarks.part(36).y)
                    self.left_eye_right_point = (self.landmarks.part(39).x, self.landmarks.part(39).y)

                    self.left_eye_center_top = mid_point(self.landmarks.part(37), self.landmarks.part(38))
                    self.left_eye_center_bottom = mid_point(self.landmarks.part(41), self.landmarks.part(40))

                    self.left_eye_horizontal = self.landmarks.part(39).x - self.landmarks.part(36).x
                    self.left_eye_hor_line = cv2.line(self.frame, self.left_eye_left_point, self.left_eye_right_point,
                                                      (0, 0, 255), 1)
                    self.left_eye_ver_line = cv2.line(self.frame, self.left_eye_center_top, self.left_eye_center_bottom,
                                                      (0, 0, 255), 1)

                    self.right_eye_left_point = (self.landmarks.part(42).x, self.landmarks.part(42).y)
                    self.right_eye_right_point = (self.landmarks.part(45).x, self.landmarks.part(45).y)

                    self.right_eye_center_top = mid_point(self.landmarks.part(43), self.landmarks.part(44))
                    self.right_eye_center_bottom = mid_point(self.landmarks.part(47), self.landmarks.part(46))

                    self.right_eye_horizontal = self.landmarks.part(45).x - self.landmarks.part(42).x
                    self.right_eye_hor_line = cv2.line(self.frame, self.right_eye_left_point,
                                                       self.right_eye_right_point, (0, 0, 255), 1)
                    self.right_eye_ver_line = cv2.line(self.frame, self.right_eye_center_top,
                                                       self.right_eye_center_bottom, (0, 0, 255), 1)
            except (ValueError, Exception):
                pass

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
