from flask import Flask
from flask import request
from flask import send_file
from threading import Thread

import json, time, requests


app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def main():
	return app.send_static_file('main.html')

@app.route('/api/upcheck')
def upCheck():
	return str(1)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)