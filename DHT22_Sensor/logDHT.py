import time
import sqlite3
#import Adafruit_DHT
import serial
#arduino = serial.Serial('/dev/ttyACM0/',9600)
dbname='sensorsData.db'
sampleFreq = 0.2 # time in seconds ==> Sample each 1 min
# get data from DHT sensor


def getDHTdata():	
    

	ser = serial.Serial("/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0", 9600, timeout=1)
	# try:
	while True:
		cmd = "t"
		comandoBytes = cmd.encode()
		ser.write(comandoBytes)
		time.sleep(2)
		read = ser.readline()
		temp=read.decode()
		if len(temp)!=0:
			break
	while True:
		cmd = "h"
		comandoBytes = cmd.encode()
		ser.write(comandoBytes)
		time.sleep(2)
		read = ser.readline()
		hum=read.decode()
		if len(hum)!=0:
			break
	while True:
		cmd = "g"
		comandoBytes = cmd.encode()
		ser.write(comandoBytes)
		time.sleep(2)
		read = ser.readline()
		hgr=read.decode()
		if len(hgr)!=0:
			break
    
	print(temp)
	print(hum)
	print(hgr)

	# except KeyboardInterrupt:
	# 	print("\nInterrupcion por teclado")
	# except ValueError as ve:
	# 	print(ve)
	# 	print("Otra interrupcion")
	# finally:
	ser.close()


    
	return temp, hum, hgr 
	#hum=22.1
	#temp=33.3
	# if hum is not None and temp is not None and hgr is not None:
	# 	hum = round(hum)
	# 	temp = round(temp, 1)
	# 	hgr = round(hgr)

# log sensor data on database
def logData (temp2, hum2, hgr2):
	
	print("-->")
	#print("temperatura:"+str(temp2))
	#print("humedad:"+str(hum2))
	#print("hgr:"+str(hgr2))
	#conn=sqlite3.connect(dbname)
	#curs=conn.cursor()
	#curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum,hgr))
	#conn.commit()
	#conn.close()
# main function
def main():
	while True:
		temp2, hum2, hgr2 = getDHTdata()
		logData (temp2, hum2, hgr2)
		time.sleep(sampleFreq)
		#print(temp)
		#print(hum)
# ------------ Execute program 
main()
