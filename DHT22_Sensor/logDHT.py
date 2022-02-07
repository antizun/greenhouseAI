import time
import sqlite3
#import Adafruit_DHT
import serial
#arduino = serial.Serial('/dev/ttyACM0/',9600)
dbname='sensorsData.db'
sampleFreq = 0.2 # time in seconds ==> Sample each 1 min
# get data from DHT sensor

temp=1.1
hum=1.1
hgr=1.1 

def getDHTdata():	

	arduino=serial.Serial("/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0", 9600, timeout=1)
	time.sleep(0.1) #wait for serial to open
	if arduino.isOpen():
		print("{} connected!".format(arduino.port))
		try:

			cmd='t'
			#cmd=input("Enter command : ")
			arduino.write(cmd.encode())
			time.sleep(1) #wait for arduino to answer
			#while arduino.inWaiting()==0: pass
			if  arduino.inWaiting()>0: 
				answer=arduino.readline()
				temp=answer.decode("utf-8")
				arduino.flushInput() #remove data after reading

				answer=arduino.readline()
				hum=answer.decode("utf-8")
				arduino.flushInput() #remove data after reading

				answer=arduino.readline()
				hgr=answer.decode("utf-8")
				arduino.flushInput() #remove data after reading

				arduino.close()

		except KeyboardInterrupt:
			print("KeyboardInterrupt has been caught.")

    
	return temp, hum, hgr 
	#hum=22.1
	#temp=33.3
	# if hum is not None and temp is not None and hgr is not None:
	# 	hum = round(hum)
	# 	temp = round(temp, 1)
	# 	hgr = round(hgr)

# log sensor data on database
def logData (temp2, hum2, hgr2):
	
	print("temperatura:"+str(temp2))
	print("humedad:"+str(hum2))
	print("hgr:"+str(hgr2))
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
