import serial

arduino = serial.Serial('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0', 9600)
#arduino.open()
print("Starting!")

while True:
      comando = input('Introduce un comando: ') #Input
      #arduino.write(comando.encode()) #Mandar un comando hacia Arduino
      arduino.write(comando.encode())
      if comando == 'H':
            print('LED ENCENDIDO')
      elif comando == 'L':
            print('LED APAGADO')

arduino.close() #Finalizamos la comunicacion
