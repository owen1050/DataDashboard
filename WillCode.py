# format for ID system (XXX) line #, (XXX) device number, (0 or 1) in or out, (HALT / Reset = 1, default 0)
import random
import time
from collections import OrderedDict

i = 0 
loopDur = 1000


timeStamps = {}

def segmentedInput(segments):
    segments = serialString.split('x')
    lineID = segments[0]
    stationID = segments[1]
    inNOut = segments[2]
    haltNSave = segments[3]
    return lineID, stationID, inNOut,haltNSave
    print("Line ID:", lineID)
    print("Station ID:", stationID)
    print("In/Out:", inNOut)
    print("Halt/Save:", haltNSave)

def addTimeStamp(tree, line_id, station_id, in_out):

    timeNow = time.time()

    if line_id not in tree:
        tree[line_id] = {}
    if station_id not in tree[line_id]:
        tree[line_id][station_id] = {}
    if in_out not in tree[line_id][station_id]:
        tree[line_id][station_id][in_out] = []
    
    tree[line_id][station_id][in_out].append(timeNow)

def sort_nested_dict(d):
    # Recursively sort the dictionary by keys
    if isinstance(d, dict):
        return OrderedDict(
            sorted((k, sort_nested_dict(v)) for k, v in d.items())
        )
    return d

def calculate_average_time(timeStamps):
    # Create a new tree to store the average times
    average_time_tree = {}
    
    for line_id, stations in timeStamps.items():
        if line_id not in average_time_tree:
            average_time_tree[line_id] = {}
        
        for station_id, in_outs in stations.items():
            if station_id not in average_time_tree[line_id]:
                average_time_tree[line_id][station_id] = {}
            
            for in_out, timestamps in in_outs.items():
                if len(timestamps) > 1:
                    max_value = max(timestamps)
                    min_value = min(timestamps)
                    length = len(timestamps)
                    average = (max_value - min_value) / length
                    average_time_tree[line_id][station_id][in_out] = average
                else:
                    average_time_tree[line_id][station_id][in_out] = None
    
    return average_time_tree

def calculate_line_balancing_efficiency(average_time_tree):
    line_efficiency_tree = {}
    
    for line_id, stations in average_time_tree.items():
        total_station_time = 0
        max_station_time = 0
        station_count = 0

        for station_id, in_outs in stations.items():
            for in_out, average_time in in_outs.items():
                if average_time is not None:
                    total_station_time += average_time
                    max_station_time = max(max_station_time, average_time)
                    station_count += 1

        # Calculate the line balancing efficiency
        if station_count > 0 and max_station_time > 0:
            line_efficiency = (total_station_time / (station_count * max_station_time)) * 100
        else:
            line_efficiency = None
        
        line_efficiency_tree[line_id] = line_efficiency
    
    return line_efficiency_tree

for i in range (loopDur):
    randomLine = str(random.randint(1,5))
    randomStation = str(random.randint(1,5))
    serialString = randomLine+"x"+randomStation+"x0x0"
    lineID, stationID, inNOut, haltNSave = segmentedInput(serialString)
    addTimeStamp(timeStamps, lineID, stationID, inNOut)
    print(timeStamps)

sorted_timeStamps = sort_nested_dict(timeStamps) # sorted_timestamp
average_time = calculate_average_time(sorted_timeStamps)
line_balancing_efficiency = calculate_line_balancing_efficiency(average_time)
print("Average Time Tree:", average_time)
print("Line Balancing Efficiency Tree:", line_balancing_efficiency)