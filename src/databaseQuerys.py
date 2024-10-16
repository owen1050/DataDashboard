import sqlite3
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse


class databaseQuerys:

	con = -1

	def __init__(self):
		self.con = sqlite3.connect("realDB.db", check_same_thread=False)

	def addTimestampEvent(self, lineID, stationID,  state):
		cur = self.con.cursor()
		try:
			res = cur.execute("select max(ROWID) as greatestID from timestamps")
			ret = res.fetchone()
			maxID = int(ret[0])

			s = f"INSERT INTO timestamps VALUES ({maxID + 1}, '{lineID}', '{stationID}', {state},'{datetime.now()}')"
			res = cur.execute(s)

			self.con.commit()

			return 0
		except Exception as e:
			print("error in addTimestampEvent", e)
			return -1

	def getAllStations(self):

		cur = self.con.cursor()
		try:
			allLines = cur.execute("select DISTINCT lineID from timestamps ORDER BY lineID")
			allLinesRequest = allLines.fetchall()
			lineNums = {}
			for line in allLinesRequest:
				allStation = cur.execute(f"select DISTINCT stationID from timestamps where lineID ='{line[0]}' ORDER BY stationID")
				allStationReq = allStation.fetchall()
				stations = []
				for station in allStationReq:
					stations.append(station[0])
				lineNums[line[0]] = stations
			print(lineNums)
			self.con.commit()

			return lineNums
		except Exception as e:
			print("error in getAllStations", e)
			return -1

	def calcAvgTimeForAllStations(self):
		stations = self.getAllStations()
		avgTimes = {}
		for line in stations:
			oneStationAvgTimes = {}
			for station in stations[line]:
				avgTime = self.calcAvgTimeForStation(line, station)
				oneStationAvgTimes[station] = avgTime
			avgTimes[line] = oneStationAvgTimes

		return avgTimes

	def calcAvgTimeForStation(self, lineID, stationID):
		#get all line/station timesttatmps
		#calc avg time

		cur = self.con.cursor()

		allStamps = cur.execute(f"select lineID, stationID, state, timeOfEvent from timestamps WHERE lineID = '{lineID}' and stationID = '{stationID}' order by timeOfEvent")
		allStampsReq = allStamps.fetchall()
		self.con.commit()

		data = []
		for timestamp in allStampsReq:
			state = timestamp[2]
			time = parse(timestamp[3])
			data.append([state, time])

		timeDeltas = []
		prevState = 0
		prevTime = 0
		seen0 = False
		for d in data:
			if(seen0 == False and d[0] == 0):
				seen0 = True
				prevTime = d[1]
			else:
				if(seen0 == True):
					if(prevState == 0 and d[0] == 1):

						td = d[1] - prevTime
						timeDeltas.append(td)
						prevState = 0
					else:
						prevTime = d[1]
						prevState = 0
		totalTime = timedelta(seconds = 0)
		for td in timeDeltas:
			totalTime = totalTime + td

		avgTime = (totalTime/len(timeDeltas)).total_seconds()



		return avgTime

	
	