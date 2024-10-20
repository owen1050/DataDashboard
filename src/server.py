from flask import Flask
from flask import request
from databaseQuerys import databaseQuerys
import json

db = databaseQuerys()

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def main():
	return app.send_static_file('main.html')

@app.route('/graphpage')
def graphPage():
	return app.send_static_file('graphPage.html')

@app.route('/api/upcheck')
def upCheck():
	return str(1)

@app.route('/api/getAverageTimes')
def getAverageTimes():
	t = db.calcAvgTimeForAllStations()
	return (json.dumps(t))

@app.route('/api/getEfficiency')
def getEfficiency():
	return (json.dumps(db.getAllLineEffeciencies()))


@app.route('/api/getPartCounts')
def getPartCounts():
	return (json.dumps(db.calcPartCount()))

@app.route('/api/getAllStationsAvgOverTime')
def getAllStationsAvgOverTime():
	lineID = int(request.args.get('lineID'))
	intervalInSeconds = int(request.args.get('intervalInSeconds'))
	totalTIme = int(request.args.get('totalTIme'))
	startSecondsAgo = int(request.args.get('startSecondsAgo'))
	#print("server.pygetAllStationsAvgOverTime:", lineID, intervalInSeconds, totalTIme, startSecondsAgo)

	return (json.dumps(db.getAllStationsAvgOverTime(lineID, intervalInSeconds, totalTIme, startSecondsAgo)))

if __name__ == '__main__':
	randData.genRandData(10000)
	app.run(host="0.0.0.0", port=5000)