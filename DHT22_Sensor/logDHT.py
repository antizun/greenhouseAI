import time
import sqlite3
import Adafruit_DHT
import serial
arduino = serial.Serial('/dev/ttyACM0/',9600)
dbname='sensorsData.db'
sampleFreq = 1*5 # time in seconds ==> Sample each 1 min
# get data from DHT sensor
def getDHTdata():	
	DHT22Sensor = Adafruit_DHT.DHT22
	DHTpin = 16
	#hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
	hum=22.1
	temp=33.3
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
	return temp, hum
# log sensor data on database
def logData (temp, hum):
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum))
	conn.commit()
	conn.close()
# main function
def main():
	while True:
		temp, hum = getDHTdata()
		logData (temp, hum)
		time.sleep(sampleFreq)
		print(temp)
		print(hum)
# ------------ Execute program 
main()
