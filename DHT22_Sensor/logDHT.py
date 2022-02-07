import time
import sqlite3
#import Adafruit_DHT
import serial
#arduino = serial.Serial('/dev/ttyACM0/',9600)
dbname='sensorsData.db'
sampleFreq = 0.2 # time in seconds ==> Sample each 1 min
# get data from DHT sensor
temp=0.0
hum=0.0
hgr=0.0

def getDHTdata():	
	#DHT22Sensor = Adafruit_DHT.DHT22
	DHTpin = 16
	#hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)

	with serial.Serial("/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0", 9600, timeout=1) as arduino:
		time.sleep(0.1) #wait for serial to open
		if arduino.isOpen():
			print("{} connected!".format(arduino.port))
			try:

				_temp='t'
				#cmd=input("Enter command : ")
				arduino.write(_temp.encode())
				time.sleep(5) #wait for arduino to answer
				while arduino.inWaiting()==0: pass
				if  arduino.inWaiting()>0: 
					answer=arduino.readline()
					#print(answer)
					temp=answer.decode("utf-8")
					arduino.flushInput() #remove data after reading
					answer=arduino.readline()
					#print(answer)
					hum=answer.decode("utf-8")
					arduino.flushInput() #remove data after reading
					answer=arduino.readline()
					#print(answer)
					hgr=answer.decode("utf-8")
					arduino.flushInput() #remove data after reading

			except KeyboardInterrupt:
				print("KeyboardInterrupt has been caught.")



	#hum=22.1
	#temp=33.3
	# if hum is not None and temp is not None and hgr is not None:
	# 	hum = round(hum)
	# 	temp = round(temp, 1)
	# 	hgr = round(hgr)
	return temp, hum, hgr
# log sensor data on database
def logData (temp, hum, hgr):
	
	print("temperatura:"+str(temp))
	print("humedad:"+str(hum))
	print("hgr:"+str(hgr))
	#conn=sqlite3.connect(dbname)
	#curs=conn.cursor()
	#curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum,hgr))
	#conn.commit()
	#conn.close()
# main function
def main():
	while True:
		temp, hum, hgr = getDHTdata()
		logData (temp, hum, hgr)
		time.sleep(sampleFreq)
		#print(temp)
		#print(hum)
# ------------ Execute program 
main()
