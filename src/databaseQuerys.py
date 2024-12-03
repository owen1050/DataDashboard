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
		
	def addTimestampEventAT(self, lineID, stationID,  state, time):
		cur = self.con.cursor()
		try:
			res = cur.execute("select max(ROWID) as greatestID from timestamps")
			ret = res.fetchone()
			maxID = int(ret[0])

			s = f"INSERT INTO timestamps VALUES ({maxID + 1}, '{lineID}', '{stationID}', {state},'{time}')"
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

	def calcPartCount(self):
		stations = self.getAllStations()
		partCounts = {}
		for line in stations:
			minPartCount = 999999
			for station in stations[line]:
				pc = self.calcPartCountForStation(line, station)
				if(pc < minPartCount):
					minPartCount = pc
			partCounts[line] = minPartCount

		return partCounts

	def calcPartCountForStation(self, lineID, stationID):
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
		return len(timeDeltas)

	def calcAvgTimeForStation(self, lineID, stationID):
		#get all line/station timesttatmps
		#calc avg time

		cur = self.con.cursor()

		allStamps = cur.execute(f"select lineID, stationID, state, timeOfEvent from timestamps WHERE lineID = '{lineID}' and stationID = '{stationID}' order by timeOfEvent")
		allStampsReq = allStamps.fetchall()
		self.con.commit()

		return self.rawTimestampsToAverageTime(allStampsReq)

		

	def getAllLineEffeciencies(self):
		avgTimes = self.calcAvgTimeForAllStations()
		effecienceis = {}

		for line in avgTimes:
			minT = 999999999
			maxT = 0
			#print(line, avgTimes[line])
			for station in avgTimes[line]:
				time = avgTimes[line][station]
				if(time > maxT):
					maxT = time

				if(time < minT):
					minT = time

			effecienceis[line] = 100*minT/(maxT+0.000001)
		return effecienceis
	
	def getAverageTimeForStationInIntervals(self, lineID, stationID, intervalInSeconds, totalTime, startSecondsAgo):
		now = datetime.now()
		startTime = now - timedelta(seconds = (startSecondsAgo))
		numTimeIntervals = int(totalTime/intervalInSeconds)
		if(numTimeIntervals > 500):
			return "Error: Too many datapoints"
		else:
			intervals = []
			for iN in range(numTimeIntervals):
				start = startTime + timedelta(seconds = intervalInSeconds * iN )
				end =  startTime + timedelta(seconds = intervalInSeconds * (iN+1))
				#print("start, end:", start, end)
				intervals.append([start, end])
		
		cur = self.con.cursor()
		ret = []
		for interval in intervals:
			r = f"select lineID, stationID, state, timeOfEvent from timestamps where timeOfEvent between '{interval[0]}' and '{interval[1]}' and lineID = '{lineID}' and stationID = '{stationID}' and state = 1 order by timeOfEvent"
			allStamps = cur.execute(r)
			allStampsReq = allStamps.fetchall()

			self.con.commit()

			ret.append([str(interval[0]), self.rawTimestampsToAverageTime(allStampsReq)])

		return ret
	

	def getAllStationsAvgOverTime(self, lineID, intervalInSeconds, totalTIme, startSecondsAgo):
		stations = self.getAllStations()[lineID]
		cycleTimeOverTimeByStation = {}
		for station in stations:
			times = self.getAverageTimeForStationInIntervals(lineID, station, intervalInSeconds, totalTIme, startSecondsAgo)
			cycleTimeOverTimeByStation[station] = times

		return cycleTimeOverTimeByStation

	def rawTimestampsToAverageTime(self, allStampsReq):
		#print(allStampsReq)
		data = []
		for timestamp in allStampsReq:
			state = timestamp[2]
			time = parse(timestamp[3])
			if(state == 1):
				data.append([state, time])
		print(data)
		timeDeltas = []
		prevState = 0
		prevTime = 0
		first = True
		totalTime = timedelta(seconds = 0)
		for d in data:
			if(first):
				first = False
				prevTime = d[1]
			else:
				td = d[1] - prevTime
				prevTime = d[1]
				if(td.total_seconds() < 60*60*8):
					timeDeltas.append(td)
					totalTime = totalTime + td

		
		try:
			avgTime = (totalTime/len(timeDeltas)).total_seconds()
			return avgTime
		except:
			return 0
		

	