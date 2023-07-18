import saccademodel 
import csv
import numpy as np
import matplotlib.pyplot as plt
import time

from pygaze import *

# frame rate in fps
frame_rate = float(input("Enter frame rate of eye tracker (HoloLens default is 30fps): "))

# time interval in seconds
time_interval = float(input("Enter the interval at which saccade duration is calculated: "))

frame_interval = frame_rate * time_interval

input_eye_points = []

saccade_durations = []

frame_stamps = [0]

errors = []

target_hits = {}


with open('machinesample20230718112820.csv', newline = '\n') as csvfile:
    data = csv.DictReader(csvfile, delimiter = ',')
    frame_count = 0;
    
    for row in data:
        if frame_count % frame_interval == 0 and frame_count != 0:
            frame_stamps = np.append(frame_stamps, frame_count / frame_rate);
        frame_count += 1

        if row['hit_name'] != "" and row['hit_name'] != None:
            if target_hits.get(row["hit_name"]) == None:
                target_hits[row["hit_name"]] = []
            # add 0s for intervals with no hits
            for i in range(0, len(frame_stamps) - len(target_hits[row["hit_name"]])):
                    target_hits[row["hit_name"]].append(0)
            target_hits[row["hit_name"]][len(frame_stamps)-1] += 1

        

        '''
        non_nans = 0
        if row['enabled'] != 'enabled' and row['enabled'] == 'TRUE' and row['valid'] == 'TRUE':
            input_eye_points.append([float(row['gaze_origin_x']) + float(row['gaze_direction_x']), float(row['gaze_origin_y']) + float(row['gaze_direction_y'])])
            non_nans = 1
        else:
            input_eye_points.append([None, None])
        if frame_count % frame_interval == 0 and frame_count != 0:
            if non_nans:
                results = saccademodel.fit(input_eye_points)
                print("info at frame: ", frame_count)
                if "saccade_points" in results.keys():
                    print('saccade duration: ', len(results["saccade_points"]) / frame_rate)
                    saccade_durations = np.append(saccade_durations, len(results["saccade_points"]) / frame_rate)
                    frame_stamps = np.append(frame_stamps, frame_count);
                print('error: ', results["mean_squared_error"])
                errors = np.append(errors, results["mean_squared_error"]);
                
            input_eye_points.clear()


        frame_count += 1
        if frame_count > 200000:
            break
        ''' 


for data in target_hits.items():
    for i in range(0, len(frame_stamps) - len(data[1])):
        data[1].append(0)
    if "Controller" in data[0]:
        plt.plot(frame_stamps, data[1], label = data[0], color = "blue")
    elif "Display" in data[0]:
        plt.plot(frame_stamps, data[1], label = data[0], color = "red")
    else:
        plt.plot(frame_stamps, data[1], label = data[0])
    
    plt.legend()




plt.xlabel("Seconds")
plt.ylabel("Fixations in " + str(time_interval) + " Second Interval")
plt.show()
  

