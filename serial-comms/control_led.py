#!/usr/bin/python3
# Basic script for turning LED ON and OFF on Arduino over serial
import serial
import time

#Function to send and recieve data - assuming serial port is open!
def send_receive(arduino, command):
	#Write command to Arduino - .encode is for converting string to byte 
	# (could leave as .encode() as utf-8 is default)
	arduino.write(command.encode('utf-8'))
	time.sleep(0.5)

	#Readline() reads from the serial port what is sent back from the Arduino
	response = arduino.readline().decode('utf-8').strip()
	print(f"Received: {response}")
	time.sleep(0.5)

# Open serial port
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
	time.sleep(2) #Wait for connection to stabilize

	print("Arduino Ready for Command...")

	while True:
		#Ask for command input
		command = input("Enter 1 (ON) or 0 (OFF):")
		#Check if the input is 'quit'
		if command == "quit":
			break
		elif command != "1" and command != "0":
			print("Error on input - please enter a valid command")
			continue
		else:
			#Send and receive
			send_receive(arduino, command)
