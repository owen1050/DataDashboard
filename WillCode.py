# format for ID system (XXX) line #, (XXX) device number, (0 or 1) in or out, (HALT / Reset = 1, default 0)
import random
import time
from collections import OrderedDict

class RandDataGen():
    i = 0 
    timeStamps = {}
    serialString = ""
    sorted_timeStamps = {}
    average_time = {}
    line_balancing_efficiency = {}

    def segmentedInput(self, segments):
        segments = self.serialString.split('x')
        lineID = segments[0]
        stationID = segments[1]
        inNOut = segments[2]
        haltNSave = segments[3]
        return lineID, stationID, inNOut,haltNSave
        print("Line ID:", lineID)
        print("Station ID:", stationID)
        print("In/Out:", inNOut)
        print("Halt/Save:", haltNSave)

    def addTimeStamp(self, tree, line_id, station_id, in_out):

        timeNow = time.time()

        if line_id not in tree:
            tree[line_id] = {}
        if station_id not in tree[line_id]:
            tree[line_id][station_id] = {}
        if in_out not in tree[line_id][station_id]:
            tree[line_id][station_id][in_out] = []
        
        tree[line_id][station_id][in_out].append(timeNow)

    def sort_nested_dict(self, d):
        # Recursively sort the dictionary by keys
        if isinstance(d, dict):
            return OrderedDict(
                sorted((k, self.sort_nested_dict(v)) for k, v in d.items())
            )
        return d

    def calculate_average_time(self, timeStamps):
        # Create a new tree to store the average times
        average_time_tree = {}
        
        for line_id, stations in self.timeStamps.items():
            if line_id not in average_time_tree:
                average_time_tree[line_id] = {}
            
            for station_id, in_outs in stations.items():
                if station_id not in average_time_tree[line_id]:
                    average_time_tree[line_id][station_id] = {}
                
                for in_out, self.timeStamps in in_outs.items():
                    if len(self.timeStamps) > 1:
                        max_value = max(self.timeStamps)
                        min_value = min(self.timeStamps)
                        length = len(self.timeStamps)
                        average = (max_value - min_value) / length
                        average_time_tree[line_id][station_id][in_out] = average
                    else:
                        average_time_tree[line_id][station_id][in_out] = None
        
        return average_time_tree

    def calculate_line_balancing_efficiency(self, average_time_tree):
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

    def genRandData(self, loopDur_ = 1000):
        loopDur = loopDur_
        for i in range (loopDur):
            randomLine = str(random.randint(1,5))
            randomStation = str(random.randint(1,5))
            self.serialString = randomLine+"x"+randomStation+"x0x0"
            lineID, stationID, inNOut, haltNSave = self.segmentedInput(self.serialString)
            self.addTimeStamp(self.timeStamps, lineID, stationID, inNOut)
            #print(self.timeStamps)

        self.sorted_timeStamps = self.sort_nested_dict(self.timeStamps) # sorted_timestamp
        self.average_time = self.calculate_average_time(self.sorted_timeStamps)
        self.line_balancing_efficiency = self.calculate_line_balancing_efficiency(self.average_time)
        print("Average Time Tree:", self.average_time)
        print("Line Balancing Efficiency Tree:", self.line_balancing_efficiency)