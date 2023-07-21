import saccademodel 
import csv
import numpy as np
import matplotlib.pyplot as plt
import time

from detectors import blink_detection, saccade_detection, fixation_detection
from gazeplotter import *



def main():
    # frame rate in fps
    frame_rate = float(input("Enter frame rate of eye tracker (HoloLens default is 30fps): "))

    # time interval in seconds
    time_interval = float(input("Enter desired interval in seconds: "))

    # time interval in frames
    frame_interval = frame_rate * time_interval

    frame_stamps = [0]

    errors = []

    # dictionary - key = name of AOI, value = list of hit frames per frame interval (len(values) = len(frame_stamps)), sort of like a hash map
    target_hits = {}

    x_points = []

    y_points = []

    time_stamps_ms = []


    with open('machinesample20230719130750.csv', newline = '\n') as csvfile:
        data = csv.DictReader(csvfile, delimiter = ',')
        frame_count = 0;
    
        for row in data:
            # create frame timestamps for aoi graph
            if frame_count % frame_interval == 0 and frame_count != 0:
                frame_stamps = np.append(frame_stamps, frame_count / frame_rate);
        
            # update dictionary when a hit is detected
            if row['hit_name'] != "" and row['hit_name'] != None:
                # create new key in dictionary when AOI is initially found
                if target_hits.get(row["hit_name"]) == None:
                    target_hits[row["hit_name"]] = []
                # add 0s for intervals with no hits
                for i in range(0, len(frame_stamps) - len(target_hits[row["hit_name"]])):
                        target_hits[row["hit_name"]].append(0)
                target_hits[row["hit_name"]][len(frame_stamps)-1] += 1 

            
            
            if row['enabled'] == "True" and row['valid'] == "True":
                # add points for saccade analysis
                # to do: figure out if this is actually the appropriate way to find 2d gaze position
                x_points = np.append(x_points, float(row['gaze_origin_z']) + float(row['gaze_direction_z']))
                y_points = np.append(y_points, float(row['gaze_origin_y']) + float(row['gaze_direction_y']))
            else:
                x_points = np.append(x_points, 0.0)
                y_points = np.append(y_points, 0.0)

            time_stamps_ms = np.append(time_stamps_ms, frame_count / frame_rate * 1000.0)
            frame_count += 1
    
    # scale points to fit
    x_min = min(x_points)
    for i, pt in enumerate(x_points):
        if pt != 0.0:
            x_points[i] -= x_min
    y_min = min(y_points)
    for i, pt in enumerate(y_points):
        if pt != 0.0:
            y_points[i] -= y_min

    Ssac, Esac = saccade_detection(x_points, y_points, time_stamps_ms)
    Sfix, Efix = fixation_detection(x_points, y_points, time_stamps_ms)
    Sblk, Eblk = blink_detection(x_points, y_points, time_stamps_ms)

    plt.figure(1)
    fixation_starts = np.array([inner[0] for inner in Efix])
    fixation_durations = np.array([inner[2] for inner in Efix])
    saccade_starts = np.array([inner[0] for inner in Esac])
    saccade_durations = np.array([inner[2] for inner in Esac])
    blink_starts = np.array([inner[0] for inner in Eblk])
    blink_durations = np.array([inner[2] for inner in Eblk])
    plt.scatter(fixation_starts, fixation_durations, label = "Fixations")
    plt.scatter(saccade_starts, saccade_durations, label = "Saccades")
    plt.scatter(blink_starts, blink_durations, label = "Blinks")
    plt.xlabel("Action Start Time (ms)")
    plt.ylabel("Action Duration (ms)")
    plt.legend()
    plt.show()

    draw_fixations(Efix, (int(max(x_points)), int(max(y_points))))

    draw_scanpath(Efix, Esac, (int(max(x_points)), int(max(y_points))))

    draw_raw(x_points, y_points, (int(max(x_points)), int(max(y_points))))

    for data in target_hits.items():
        # add 0s for intervals with no hits
        for i in range(0, len(frame_stamps) - len(data[1])):
            data[1].append(0)
        plt.figure(0)
        plt.plot(frame_stamps, data[1], label = data[0])
    
        plt.legend(fontsize = 12)




    plt.xlabel("Time (seconds)", fontsize = 12)
    plt.ylabel("Fixation Frames in " + str(time_interval) + " Second Interval", fontsize = 12)
    plt.show()

    
  
if __name__ == "__main__":
	main()
