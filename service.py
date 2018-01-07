from flask import Flask
from flask import request
import mainProcess
import time
import subprocess
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
@app.route("/start")
def start():
    quantity = request.args.get('x', default = 0, type = int)
    print quantity
    price = request.args.get('y', default = '*', type = str)
    print price
    symbol = request.args.get('z', default = '*', type = str)
    print symbol
    mode = request.args.get('a', default = '*', type = str)
    print mode
    min_ganho = request.args.get('up', default = '*', type = str)
    print min_ganho
    mainProcess.mainProcess(quantity,price,symbol,mode,min_ganho)
    return "Hello World!"
    



if __name__ == "__main__":
    app.run()