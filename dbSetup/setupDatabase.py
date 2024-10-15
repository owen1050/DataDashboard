import sqlite3

con = sqlite3.connect("testDB.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS timestamps(lineID INTEGER,   stationID integer, state integer, timeOfEvent timestamp )")

cur.execute("CREATE TABLE IF NOT EXISTS averageStationTimes(lineID integer, stationID integer, averageTimeSec real, updatedAt timestamp, updateCount integer)")

cur.execute("CREATE TABLE IF NOT EXISTS lineEffeciencies(lineID integer,  lineEffeciency real,  updatedAt timestamp )")

cur.execute("CREATE TABLE IF NOT EXISTS lineNames(lineID integer, lineName text)")

cur.execute("CREATE TABLE IF NOT EXISTS stationNames(stationID integer, stationName text)")

con.commit()