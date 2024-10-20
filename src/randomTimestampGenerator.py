from random import random
from databaseQuerys import databaseQuerys

from datetime import datetime
from datetime import timedelta

db = databaseQuerys()

timestepBack = 600
timesToStepBack = 30
datapointsToCreate = 10
spacing = 10
avgTime = 10
oneStepVariance = 10
oneSessionVariance = 1
lines = [11,12,13,14,15]
stations = [1,2,3,4,5,6,7,8,10]

startTime = datetime.now()

for stepBack in range(timesToStepBack):
    
    thisStepRandomDiff = (random() - 0.5) * oneStepVariance + avgTime
    thisStepStartTime = startTime - timedelta(seconds = stepBack * timestepBack) + timedelta(seconds=thisStepRandomDiff)
    for datapoint in range(datapointsToCreate):
        for line in lines:
            for station in stations:
                thisStationStartTime = thisStepStartTime + timedelta(seconds=spacing * datapoint)
                thisStationRandomDiff =  (random() - 0.5) * oneSessionVariance

                db.addTimestampEventAT(line, station, 0, thisStationStartTime)
                db.addTimestampEventAT(line, station, 1, thisStationStartTime + timedelta(seconds=thisStationRandomDiff))



