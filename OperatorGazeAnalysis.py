import saccademodel 
import csv

# frame rate in fps
frame_rate = float(input("Enter frame rate of eye tracker (HoloLens default is 30fps): "))

# time interval in seconds
time_interval = float(input("Enter the interval at which saccade duration is calculated: "))

frame_interval = frame_rate * time_interval

input_eye_points = []

with open('machinesample_BIG.csv', newline = '\n') as csvfile:
    data = csv.DictReader(csvfile, delimiter = ',')
    frame_count = 0;
    for row in data:
        non_nans = 0
        if row['enabled'] != 'enabled' and eval(row['enabled']) and eval(row['valid']):
            input_eye_points.append([float(row['gaze_origin_x']) + float(row['gaze_direction_x']), float(row['gaze_origin_y']) + float(row['gaze_direction_y'])])
            non_nans = 1
        else:
            input_eye_points.append([None, None])

        if frame_count % frame_interval == 0 and frame_count != 0 and non_nans:
            results = saccademodel.fit(input_eye_points)

            print("info at frame: ", frame_count)
            if "saccade_points" in results.keys():
                print('saccade duration: ', len(results["saccade_points"]) / frame_rate)
            print('error: ', results["mean_squared_error"])
            input_eye_points.clear()

        frame_count += 1
  

