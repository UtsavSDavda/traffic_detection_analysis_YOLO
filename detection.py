from ultralytics import YOLO
import numpy as np
import cv2
from ultralytics import YOLO
import threading

overalluniqueid = list()

model = YOLO('yolov8n.pt')

file_path1 = "video/video/cctv052x2004080516x01638.avi"
file_path2 = "video/video/cctv052x2004080516x01639.avi"
file_path3 = "video/video/cctv052x2004080516x01641.avi"
file_path4 = "video/video/cctv052x2004080516x01643.avi"

cap1 = cv2.VideoCapture(file_path1)
cap2 = cv2.VideoCapture(file_path2)
cap3 = cv2.VideoCapture(file_path3)
cap4 = cv2.VideoCapture(file_path4)


def add_yolo_counts(yolo_counts):
    final = yolo_counts[0] + (8*yolo_counts[1]) + (5*yolo_counts[2]) + (9*(yolo_counts[3]+yolo_counts[4]))
    return final
def addcountclass(y,yolo_counts):
    if y == 1:
        yolo_counts[0] += 1
    elif y == 2:
        yolo_counts[1] += 1
    elif y == 3:
        yolo_counts[2] += 1
    elif y == 5:
        yolo_counts[3] += 1
    else:
        yolo_counts[4] += 1

    return yolo_counts
#18599

def getnumber(vehicle):
    yolo_classes = [(1,"bicycle"),(2,"car"),(3,"motorcycle"),(5,"bus"),(7,"truck")]
    yolo_counts = [0,0,0,0,0]
    for i in range(len(vehicle)):
        x = list(vehicle[i].keys())[0]
        y = list(vehicle[i].values())[0]
        if y in [1,2,3,5,7]:
            yolo_counts = addcountclass(y,yolo_counts)
    final = add_yolo_counts(yolo_counts)
    return final

def windowname(idname):
    if idname == 1:
        return 'North'
    elif idname == 2:
        return 'South'
    elif idname == 3:
        return 'East'
    else:
        return 'West'
def track_vehicles(path,cap,threadn):
    unique_id = set()
    classlist = []
    print(path)
    success = True
    while success:
        success, frame = cap.read()
        if success:
            results = model.track(frame,persist=True)
            for result1 in results:
                box = result1.numpy().boxes
                for bx in box:
                    x = len(unique_id)
                    unique_id.add(int((bx.id)[0]))
                    y = len(unique_id)
                    if y > x:
                        classlist.append({int((bx.id)[0]):int((bx.cls)[0])})


            frame2 = results[0].plot()
            cv2.imshow(windowname(threadn),frame2)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    print("classlist" + str(classlist))
    print("list of ids" + str(unique_id))
    overalluniqueid.append({ threadn : classlist})
    cap.release()

thread_1 = threading.Thread(target=track_vehicles(file_path1,cap1,1),daemon=True)
thread_2 = threading.Thread(target=track_vehicles(file_path2,cap2,2),daemon=True)
thread_3 = threading.Thread(target=track_vehicles(file_path3,cap3,3),daemon=True)
thread_4 = threading.Thread(target=track_vehicles(file_path4,cap4,4),daemon=True)

thread_1.start()
thread_2.start()
thread_3.start()
thread_4.start()

thread_1.join()
thread_2.join()
thread_3.join()
thread_4.join()

print(overalluniqueid)

vehicle_north = overalluniqueid[0].get(1)
vehicle_south = overalluniqueid[1].get(2)
vehicle_east = overalluniqueid[2].get(3)
vehicle_west = overalluniqueid[3].get(4)

waitscoren = getnumber(vehicle_north)
waitscores = getnumber(vehicle_south)
waitscoree = getnumber(vehicle_east)
waitscorew = getnumber(vehicle_west)


print(vehicle_north)
print(vehicle_south)
print(vehicle_east)
print(vehicle_west)

print(waitscoren)
print(waitscores)
print(waitscoree)
print(waitscorew)


cv2.destroyAllWindows()

