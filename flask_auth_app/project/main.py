from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import db
#################################################################################
#DHT SERVER
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from flask import send_file, make_response, request
#################################################################################

main = Blueprint('main', __name__)

#app = Flask(__name__)

#################################################################################
#SQL LITE
import sqlite3
import threading 
conn=sqlite3.connect('sensorsData.db',check_same_thread=False)
#conn=sqlite3.connect('../sensorsData.db')
curs=conn.cursor()

lock = threading.Lock()
#################################################################################
import serial
#################################################################################
#FUNCTIONS
def getLastData():
	try:
		lock.acquire()
		for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
			time = str(row[0])
			temp = row[1]
			hum = row[2]
		return time, temp, hum
	finally:
	        lock.release()
		#conn.close()


def getHistData (numSamples):
	try:
		lock.acquire()
		curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
		data = curs.fetchall()
		dates = []
		temps = []
		hums = []
		for row in reversed(data):
			dates.append(row[0])
			temps.append(row[1])
			hums.append(row[2])
		return dates, temps, hums
	finally:
		lock.release()
		#conn.close()
def maxRowsTable():
	try:
		lock.acquire()
		for row in curs.execute("select COUNT(temp) from  DHT_data"):
			maxNumberRows=row[0]
		return maxNumberRows
	finally:
		lock.release()
		#conn.close()
#initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
	numSamples = 100
	
#################################################################################
#RUTAS DHT server

# main route 
#@main.route("/")
#def index():
#	time, temp, hum = getLastData()
#	templateData = {
#	  'time'		: time,
#      'temp'		: temp,
#      'hum'			: hum,
#      'numSamples'	: numSamples
#	}
#	return render_template('profile.html', **templateData)


@main.route('/profile', methods=['POST'])
def my_form_post():
    global numSamples 
    numSamples = int (request.form['numSamples'])
    if (numSamples>0):
        numMaxSamples = maxRowsTable()
        if (numSamples > numMaxSamples):
            numSamples = (numMaxSamples-1)

        time, temp, hum = getLastData()
        
        templateData = {
        'name'        :current_user.name,
        'time'		: time,
        'temp'		: temp,
        'hum'			: hum,
        'numSamples'	: numSamples
        }
        return render_template('profile.html', **templateData)
    
    arduino = serial.Serial('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0', 9600)
    comando='H'
    arduino.write(comando.encode())
    arduino.close() #Finalizamos la comunicacion     
    if (request.form['riego_manual']=='riego_manual'):
        print('RIEGO MANUAL')
        comando='H'
        arduino.write(comando.encode())
        arduino.close() #Finalizamos la comunicacion
    if (request.form['ventilar']=='ventilar'):
        print('VENTILAR')
        comando='H'
        arduino.write(comando.encode())
        arduino.close() #Finalizamos la comunicacion  

@main.route('/plot/temp')
def plot_temp():
	times, temps, hums = getHistData(numSamples)
	ys = temps
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature [°C]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@main.route('/plot/hum')
def plot_hum():
	times, temps, hums = getHistData(numSamples)
	ys = hums
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Humidity [%]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response




#################################################################################


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    time, temp, hum = getLastData()
    templateData = {
       'name'        :current_user.name,
       'time'	     : time,
       'temp'	     : temp,
       'hum'	     : hum,
       'numSamples'  : numSamples
	}
	#name=current_user.name
    return render_template('profile.html',**templateData)
