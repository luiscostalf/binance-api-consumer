
from flask import Flask
from flask import request
import mainProcess
import time
import subprocess
import threading
import json
import os
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
@app.route("/start")
def start():
    quantity = request.args.get('x', default = 0, type = int)
    print quantity
    price = float(request.args.get('y', default = '*', type = str))
    print price
    symbol = request.args.get('z', default = '*', type = str)
    print symbol
    mode = request.args.get('a', default = '*', type = str)
    print mode
    min_ganho = request.args.get('up', default = '*', type = str)
    print min_ganho
    aux = mainProcess.mainProcess(quantity,price,symbol,mode,min_ganho)
    t = threading.Thread(target=aux.bot)
    t.start()
    return "Hello World!"
    
@app.route("/check")
def check():
    log = request.args.get('x', default = '*', type = str)
    f = (str(log) + 'lifeLOG.txt', 'r')
    obj = json.load(f.read())
    return obj

@app.route("/kill")
def kill():
    log = request.args.get('pid', default = '*', type = str)
    os.kill(log)
    return json



if __name__ == "__main__":
    app.run()