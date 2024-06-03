from ultralytics import YOLO
import numpy as np
import cv2
from ultralytics import YOLO
import keyboard

vehicles_detected_n = []
vehicles_detected_s = []
vehicles_detected_e = []
vehicles_detected_w = []

model = YOLO('yolov8n.pt')

def truefn(ret_n,ret_s,ret_e,ret_w):
    if ret_n == False or ret_s == False or ret_w == False or ret_e == False:
        return False
    else:
        return True
# def updatearray(detection):
def vehicle_detection(cap_n,cap_s,cap_e,cap_w):
    ret_n = True
    ret_s = True
    ret_e = True
    ret_w = True
    while truefn(ret_n,ret_s,ret_e,ret_w):
        ret_n, frame_n = cap_n.read()
        ret_s, frame_s = cap_s.read()
        ret_e, frame_e = cap_e.read()
        ret_w, frame_w = cap_w.read()
        if truefn(ret_n,ret_s,ret_e,ret_w):
            detections_n = model.track(frame_n,persist=True)
            detections_s = model.track(frame_s,persist=True)
            detections_e = model.track(frame_e,persist=True)
            detections_w = model.track(frame_w,persist=True)

            plotted_n = detections_n[0].plot()
            plotted_s = detections_s[0].plot()
            plotted_e = detections_e[0].plot()
            plotted_w = detections_w[0].plot()

            updatearray(detections_n)
            updatearray(detections_s)
            updatearray(detections_e)
            updatearray(detections_w)


            if cv2.waitKey(10) and keyboard.is_pressed('q'):
                break


north = ''
south = ''
east = ''
west = ''

cap_n = cv2.VideoCapture(north)
cap_s = cv2.VideoCapture(south)
cap_e = cv2.VideoCapture(east)
cap_w = cv2.VideoCapture(west)

