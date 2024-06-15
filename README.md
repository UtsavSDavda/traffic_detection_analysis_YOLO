# traffic_detection_analysis_YOLO
Detect traffic from CCCTV camera footage and automate decision making of traffic signals. This code helps capture traffic images and after detecting various vehicles from 4 footages in 4 directions, decides which signal to be GREEN for how much amount of time.

**How to run the code**

1. Create a virtual environment with pip or conda.

2. Install every necessary library imported in detection.py

3. Add the footage videos you want to do the detections in the paths provided in the code. (Add file paths for all 4 videos as this code is for 4 direction traffic)

4. Run the code.

**How does this work**

4 footages of traffic are used to decide what should the traffic signal do. Hence, we add video file paths for 4 streams.

These videos are captured by CV2. 

Enabled threading as I want to do detections simultaneously in the future. All 4 capture objects will pass through a method TRACK_VEHICLES. It is ther method that tracks vehicles like bicycle,car,motorcycle,truck and bus. This method also saves the object IDs and their corresponding detected class in an object called CLASSLIST.

The CLASSLIST object is appended to a global variable OVERALLUNIQUEID. This object stores the CLASSLIST of all the threads. 4 in this case. We can display it just to get some rough idea of vehicles detected from all 4 sides before processing the data.

After saving the detected objects' corresponding classes, we display the footage with the tracking for each frame of each video.

Next step: decision making of traffic signals. Once I get the idea what amount and type of vehicles I get on all 4 lanes, I use this information in an algorithm that will decide which lane should be GREEN and which should be RED.

**How traffic signal algorithm works**

Based on the type of vehicles and amount of vehicles of each side, a SCORE is determined of each side.

There are 4 sides : NORTH, SOUTH , EAST and WEST.

The SCORE comprises of nothing but the summation of each vehicle in the lane which is multiplied with the WEIGHT_SCORE  alloted for each vehicle.

This is done because lanes with vehicles like buses will have a smaller VEHICLE COUNT, but that does not mean they get a low priority. Thus, weights are alloted to the vehicles of a high SIZE and PRIORITY as well. 

For instance, I have set the weights as:

1 for bicycle, 8 for cars, 5 for motorcycles, 9 for buses and 9 for trucks.

After this weighted multiplication of each vehicle, we add the results as the SCORE of each lane.

SCORE = SUM(vehicle_weight_score*vehicle) + WAITING_SCORE,

where WAITING SCORE = 10* (Number of vehicles waiting in RED Light)

The variable WAITING_SCORE is applicable ONLY if the lane is in RED light while the score of the iteration is being calculated.

The SCORE of opposite lanes will be added for decision making, because if we turn signal GREEN for a side, it is GREEN for the opposite side as well beccause vehicles from both sides can move ahead without blocking each other. 

If NORTH side has a GREEN signal, vehicles from the NORTH will move to the SOUTH and vehicles from the SOUTH can move towards the NORTH as well because their lane will not have any vehicles ahead. But vehicles from the EAST side can not move during this time. 

For every 10 seconds, decision is taken by traffic signal to choose which signal to turn GREEN. It will iterate the process of 10 seconds until the Traffic is CLEAR. 
 
If a side is on RED during these 10 seconds, the SCORE of the side will increase by 10 X (number of vehicles waiting during this time).

I have added this so that a side that keeps waiting for a lot of time, especially if it has a higher number of vehicles will get a priority.

