from flask import Flask

from flask import Blueprint, request, render_template
from flask import flash, redirect, url_for
from flask import current_app as current
from flask import g
from module import dbModule

import time
import serial
import requests

app = Flask(__name__)

count = 0

PORT = 'COM4'
BaudRate = 9600

## serial port setting
ser = serial.Serial(
    port = PORT,
    baudrate = BaudRate,
)

##send serial data to Arduino
def serialWrite(trans):
    ser.write(trans)
    time.sleep(0.5)

## main page route
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', result = None, resultData = None, resultUPDATE = None)

## red page route
@app.route('/red', methods=['GET'])
def red():
    global count

    # connect Database
    dbClass = dbModule.Database()

    # Insert count, Color To database
    insertQuery = "INSERT INTO inseo.color VALUES({}, '{}');".format(count , "RED")

    # Send query to Database
    dbClass.executeAll(insertQuery)
    dbClass.commit()
    
    # inquire database
    selectQuery = "SELECT * FROM color WHERE userColor = '{}' AND no = {};".format("RED", count)
    result = dbClass.executeAll(selectQuery)
    print(result)

    # result null check
    if not result:
        print("NULL")
        return render_template('red.html', result = None, resultData = None, resultUPDATE = None)

        count = count + 1

    #not null -> send data to arduino
    else:
        red = "255"
        Trans = "R" + red
        Trans = Trans.encode('utf-8')

        serialWrite(Trans)


    return render_template('red.html', result = None, resultData = None, resultUPDATE = None)

@app.route('/blue' , methods=['GET'])
def blue():
    global count
    dbClass = dbModule.Database()
    insertQuery = "INSERT INTO inseo.color VALUES({}, '{}');".format(count , "BLUE")
    dbClass.executeAll(insertQuery)
    dbClass.commit()

    selectQuery = "SELECT * FROM color WHERE userColor = '{}' AND no = {};".format("BLUE", count)
    result = dbClass.executeAll(selectQuery)

    if not result:
        print("NULL")
        return render_template('blue.html', result = None, resultData = None, resultUPDATE = None)

    else:
        blue = "255"
        Trans = "B" + blue
        Trans = Trans.encode('utf-8')
        serialWrite(Trans)
    

    count = count + 1
    return render_template('blue.html', result = None, resultData = None, resultUPDATE = None)

@app.route('/green', methods=['GET'])
def green():
    global count
    dbClass = dbModule.Database()
    insertQuery = "INSERT INTO inseo.color VALUES({}, '{}');".format(count , "GREEN")

    dbClass.executeAll(insertQuery)
    dbClass.commit()

    selectQuery = "SELECT * FROM color WHERE userColor = '{}' AND no = {};".format("GREEN", count);
    result = dbClass.executeAll(selectQuery)

    if not result:
            return render_template('green.html', result = None, resultData = None, resultUPDATE = None)

    else:
        green = "123"

        Trans = "G" + green
        Trans = Trans.encode("utf-8")

        serialWrite(Trans)
    count = count + 1
    return render_template('green.html', result = None, resultData = None, resultUPDATE = None)

@app.route('/white', methods=['GET'])
def white():
    global count
    dbClass = dbModule.Database()
    insertQuery = "INSERT INTO inseo.color VALUES({}, '{}');".format(count , "WHITE")

    dbClass.executeAll(insertQuery)
    dbClass.commit()

    selectQuery = "SELECT * FROM color WHERE userColor = '{}' AND no = {};".format("WHITE", count)
    result = dbClass.executeAll(selectQuery)

    if not result:
        print("NULL")
        return render_template('white.html', result = None, resultData = None, resultUPDATE = None)

    else:
        white = "000"

        Trans = "W" + white
        Trans = Trans.encode("utf-8")

        serialWrite(Trans)

    count = count + 1
    return render_template('white.html', result = None, resultData = None, resultUPDATE = None)

if __name__ == '__main__':
    app.run(debug=True)
