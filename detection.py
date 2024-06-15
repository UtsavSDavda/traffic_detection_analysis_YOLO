from ultralytics import YOLO
import numpy as np
import cv2
from ultralytics import YOLO
import keyboard
import threading
import queue

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



def vehicle_counter(count):
    addtn = 0
    for i in range(len(count)):
        addtn = addtn + count[i]
    return addtn

def add_yolo_counts(yolo_counts):
    final = 0
    for i in range(len(yolo_counts)):
        final+= yolo_counts[i]
    return final
def addcountclass(y,yolo_counts):
    if y == 1:
        yolo_counts.append(1)
    elif y == 2:
        yolo_counts.append(8)
    elif y == 3:
        yolo_counts.append(5)
    elif y == 5:
        yolo_counts.append(9)
    else:
        yolo_counts.append(9)

    return yolo_counts

def getnumber(vehicle):
    yolo_classes = [(1,"bicycle"),(2,"car"),(3,"motorcycle"),(5,"bus"),(7,"truck")]
    yolo_counts = []
    for i in range(len(vehicle)):
        x = list(vehicle[i].keys())[0]
        y = list(vehicle[i].values())[0]
        if y in [1,2,3,5,7]:
            yolo_counts = addcountclass(y,yolo_counts)
    final = add_yolo_counts(yolo_counts)
    return (final, yolo_counts)

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
    overalluniqueid.append({ threadn : classlist})
    cap.release()

def remove_vehicles(count1,count2):
    if len(count1) > 5:
        count1 = count1[5:]
    else:
        count1 = []
    if len(count2) > 5:
        count2 = count2[5:]
    else:
        count2 = []
    return count1, count2
def decide_signal(vehicle_north, vehicle_south, vehicle_east, vehicle_west):
    waitscoren, ncount = getnumber(vehicle_north)
    waitscores, scount = getnumber(vehicle_south)
    waitscoree, ecount = getnumber(vehicle_east)
    waitscorew, wcount = getnumber(vehicle_west)

    signals = []
    open_direction = 'None'
    traffic_null = 0
    iterations = 0
    while traffic_null < 1:
        iterations+=1
        waitscoren = add_yolo_counts(ncount)
        waitscores = add_yolo_counts(scount)
        waitscoree = add_yolo_counts(ecount)
        waitscorew = add_yolo_counts(wcount)
        print("ITERATION "+str(iterations))
        print("\n")
        print("SCORE NORTH  ::::  "+str(waitscoren)+"  VEHICLES ::::  "+str(len(ncount)))
        print("SCORE SOUTH  ::::  "+str(waitscores)+"  VEHICLES ::::  "+str(len(scount)))
        print("SCORE EAST   ::::  "+str(waitscoree)+"  VEHICLES ::::  "+str(len(ecount)))
        print("SCORE SOUTH  ::::  "+str(waitscorew)+"  VEHICLES ::::  "+str(len(wcount)))
        vertical_score = waitscoren + waitscores
        horizontal_score = waitscoree + waitscorew
        if vertical_score > horizontal_score:
            open_direction = 'North-South'
            signals.append('North-South for seconds '+str((iterations-1)*10)+"-"+str(iterations*10))
            ncount, scount = remove_vehicles(ncount,scount)
            horizontal_score += (10 * (len(ecount) + len(wcount)))
            print("SIGNAL GREEN for the direction North-South for seconds "+str((iterations-1)*10)+"-"+str(iterations*10))

        elif horizontal_score > vertical_score:
            open_direction = 'East-West'
            signals.append('East-West for seconds '+str((iterations-1)*10)+"-"+str(iterations*10))
            ecount, wcount = remove_vehicles(ecount, wcount)
            vertical_score+= (10*(len(ncount) + len(scount)))
            print("SIGNAL GREEN for the direction East-West for seconds "+str((iterations-1)*10)+"-"+str(iterations*10))
        elif vertical_score > 0:
            if (ncount + scount) >= (ecount + wcount):
                open_direction = 'North-South'
                signals.append('North-South for seconds '+str((iterations-1)*10)+"-"+str(iterations*10))
                ncount, scount = remove_vehicles(ncount, scount)
                horizontal_score += (10 * (len(ecount) + len(wcount)))
                print("SIGNAL GREEN for the direction North-South for seconds "+str((iterations-1)*10)+"-"+str(iterations*10))
            else:
                open_direction = 'East-West'
                signals.append('East-West for seconds '+str((iterations-1)*10)+"-"+str(iterations*10))
                ecount, wcount = remove_vehicles(ecount, wcount)
                vertical_score += (10 * (len(ncount) + len(scount)))
                print("SIGNAL GREEN for the direction East-West for seconds "+str((iterations-1)*10)+"-"+str(iterations*10))
        else:
            print("Congratulations! Traffic at the signal has come down to ZERO. Waiting for the next set.")
            traffic_null+=1


    return signals

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

vehicle_north = overalluniqueid[0].get(1)
vehicle_south = overalluniqueid[1].get(2)
vehicle_east = overalluniqueid[2].get(3)
vehicle_west = overalluniqueid[3].get(4)

cv2.destroyAllWindows()

signals = decide_signal(vehicle_north, vehicle_south, vehicle_east, vehicle_west)
print("GREEN SIGNAL LOGS :::::\n")
for signal in signals:
    print(signal)