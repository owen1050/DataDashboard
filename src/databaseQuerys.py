import sqlite3, openpyxl
from datetime import datetime
from datetime import timedelta


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
		

	
	