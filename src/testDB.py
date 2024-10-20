from databaseQuerys import databaseQuerys


db = databaseQuerys()
lb = db.getAllStationsAvgOverTime(1,20,600, 3600*2.1)

for b in lb:
    print(b)
    for s in lb[b]:
        print("\t", s[1])
