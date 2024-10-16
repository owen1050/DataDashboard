from flask import Flask
from flask import request
from flask import send_file
from threading import Thread
from RandomNumGenerator import RandDataGen
from databaseQuerys import databaseQuerys

db = databaseQuerys()
import json, time, requests


app = Flask(__name__, static_folder='static', static_url_path='')
randData = RandDataGen()

@app.route('/')
def main():
	return app.send_static_file('main.html')

@app.route('/api/upcheck')
def upCheck():
	return str(1)

@app.route('/api/getAverageTimes')
def getAverageTimes():
	return (json.dumps(db.calcAvgTimeForAllStations()))

@app.route('/api/getEfficiency')
def getEfficiency():
	return (json.dumps(randData.line_balancing_efficiency))

@app.route('/api/getPartCounts')
def getPartCounts():
	return (json.dumps(randData.partCounts))

@app.route('/api/regenData')
def regenData():
	randData.genRandData()
	return str(1)

if __name__ == '__main__':
	randData.genRandData(10000)
	app.run(host="0.0.0.0", port=5000)