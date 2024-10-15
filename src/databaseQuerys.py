import sqlite3, openpyxl
from datetime import datetime
from datetime import timedelta


class databaseQuerys:

	con = -1

	def __init__(self):
		self.con = sqlite3.connect("realDB.db", check_same_thread=False)
		
	def doesUserExist(self, id):
		cur = self.con.cursor()
		try:
			res = cur.execute("SELECT * FROM users where id = " + str(id))
			ret = res.fetchone()
			if(ret == None):
				return 0
			return 1
		except Exception as e:
			print("error in doesUserExist", e)
			return -1

	def addSignInEvent(self, id, action,  daysAgo, hours, categoryId = -1,):
		cur = self.con.cursor()
		try:
			res = cur.execute("UPDATE users SET checkedIn = 1 where id = " + str(id))
			ret = res.fetchone()
			s = f"INSERT INTO events VALUES ({id},'{datetime.now() - timedelta(days = int(daysAgo), hours = float(hours))}', '{action}', {int(categoryId)}, {1})"
			res = cur.execute(s)

			self.con.commit()

			self.checkUserOutMinusTime(id, action, daysAgo, hours, categoryId)

			return 0
		except Exception as e:
			print("error in checkUserIn", e)
			return -1
		

	def checkUserOutMinusTime(self, id, action, daysAgo, hours, categoryId = -1,):
		cur = self.con.cursor()
		try:
			res = cur.execute("UPDATE users SET checkedIn = 0 where id = " + str(id))
			ret = res.fetchone()

			s = f"INSERT INTO events VALUES ({id},'{datetime.now() - timedelta(days = int(daysAgo))}', '{action}', {int(categoryId)}, {0})"
			res = cur.execute(s)

			self.con.commit()
			return 0
		except Exception as e:
			print("error in checkUserOut", e)
			return -1

	def updateCategoryValues(self, id, hours, bV, bJV, bP, busV, busJV, busPar, name, weight):
		if(self.doesCategoryIDExist(id)):
			cur = self.con.cursor()
			try:
				s = f"UPDATE categories SET hours='{hours}',"\
					f"buildVarsityPer='{bV}', "\
					f"buildJVPer='{bJV}', "\
					f"buildParPer='{bP}', "\
					f"busVarsityPer='{busV}', "\
					f"busJVPer='{busJV}', "\
					f"busParPer='{busPar}', "\
					f"name='{name}', "\
					f"weight='{weight}'"\
					f"WHERE id = '{id}'"
					
				res = cur.execute(s)
				ret = res.fetchone()
				self.con.commit()
				return 0
			except Exception as e:
				print("error in setHoursForCategory", e)
				return -1
	