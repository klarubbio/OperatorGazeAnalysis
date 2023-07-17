import saccademodel 
import csv
import numpy as np
import matplotlib.pyplot as plt
import time

# frame rate in fps
frame_rate = float(input("Enter frame rate of eye tracker (HoloLens default is 30fps): "))

# time interval in seconds
time_interval = float(input("Enter the interval at which saccade duration is calculated: "))

frame_interval = frame_rate * time_interval

input_eye_points = []

saccade_durations = []

frame_stamps = []

errors = []


with open('machinesample_BIG.csv', newline = '\n') as csvfile:
    data = csv.DictReader(csvfile, delimiter = ',')
    frame_count = 0;
    
    for row in data:
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

plt.plot(frame_stamps, saccade_durations)
plt.xlabel("Frame")
plt.ylabel("Saccade Duration (frames per interval)")
plt.show()
  

