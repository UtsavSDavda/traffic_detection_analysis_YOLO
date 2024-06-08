# traffic_detection_analysis_YOLO
Detect traffic from CCCTV camera footage and automate decision making of traffic signals. 

**How to run the code**

1. Create a virtual environment with pip or conda.

2. Install every necessary library imported in detection.py

3. Add the footage videos you want to do the detections in the paths provided in the code.

4.Run the code.

**How does this work**

4 footages of traffic are used to decide what should the traffic signal do. Hence, we add video file paths for 4 streams.

These videos are captured by CV2. 

Enabled threading as I want to do detections simultaneously in the future. All 4 capture objects will pass through a method TRACK_VEHICLES. It is ther method that tracks vehicles like bicycle,car,motorcycle,truck and bus. This method also saves the object IDs and their corresponding detected class in an object called CLASSLIST.

The CLASSLIST object is appended to a global variable OVERALLUNIQUEID. This object stores the CLASSLIST of all the threads. 4 in this case. We can display it just to get some rough idea of vehicles detected from all 4 sides before processing the data.

After saving the detected objects' corresponding classes, we display the footage with the tracking.

Next step: decision making of traffic signals. Once I get the idea what amount and type of vehicles I get on all 4 lanes, I use this information in an algorithm that will decide which lane should be GREEN and which should be RED.

**How traffic signal algorithm works**

I am using a weighted score to help the traffic signals' decision as to what type of vehicles should be given a priority.

Each lane has a LANE_SCORE. This LANE_SCORE is made as maximum of 2 values: CAR_SCORE and TIME_SCORE.

TIME_SCORE of each lane is the total time sum of all the vehicles waited at the lane while the light is RED. Once it is green, some vehicles will pass through and some will remain at the lane itself when it turns RED again. This time, the TIME_SCORE of the remaining vehicles is counted to calculate the LANE_SCORE for the next time frame for which decisions will have to be made.

CAR_SCORE is simply a score that is counted by noticing the amount of vehicles in lane weighted with the type of vehicles.

Maximum of CAR_SCORE and TIME_SCORE is used as the LANE_SCORE for each lane.

The lane with highest LAN_SCORE will be allowed to pass through with a GREEN SIGNAL, meanwhile the other lanes will have a RED signal and their TIME_SCORE will keep increasing while they are RED.

The descision to color a signal GREEN or RED for the next 10 seconds will be taken at a time. Every once in 5 times, the lane that last turned GREEN earliest will be flagged GREEN. This method ensures that no lane is RED at all times.  


 


