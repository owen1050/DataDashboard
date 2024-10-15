from databaseQuerys import databaseQuerys


db = databaseQuerys()
for i in range(10):
	db.addTimestampEvent(i,i,i)