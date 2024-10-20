from random import random
from databaseQuerys import databaseQuerys

from datetime import datetime
from datetime import timedelta

db = databaseQuerys()

timestepBack = 600
timesToStepBack = 25
datapointsToCreate = 20
spacing = 10
avgTime = 10
oneStepVariance = 6
oneSessionVariance = 1
lines = [6,7]
stations = [1,2]

startTime = datetime.now()

for stepBack in range(timestepBack):
    
    thisStepRandomDiff = (random() - 0.5) * oneStepVariance
    thisStepStartTime = startTime - timedelta(seconds = stepBack * timestepBack) + timedelta(seconds=thisStepRandomDiff)
    for datapoint in range(datapointsToCreate):
        for line in lines:
            for station in stations:
                thisStationRandomDiff =  (random() - 0.5) * oneSessionVariance
                db.addTimestampEventAT(line, station, 0, thisStepStartTime)
                db.addTimestampEventAT(line, station, 1, thisStepStartTime + timedelta(seconds=thisStationRandomDiff))



