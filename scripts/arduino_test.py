#!/usr/bin/python3

#Arduino test script for trying out automated testing

import serial
import time
import datetime
import os

results = []

if os.path.exists("arduino_test_log.md"):
	pass
else:
	with open("arduino_test_log.md", "w") as file:
		file.write("=== ARDUINO TEST LOG ===\n")

def test_arduino_connection():
#Function to check if we connect to the Arduino successfully
	try:
		with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
			time.sleep(2)
			return True
	except Exception:
		return False

def test_arduino_data():
	try:
		with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
			time.sleep(2)
			command = "1"
		        #Write command to Arduino - .encode is for converting string to byte 
			arduino.write(command.encode())
			time.sleep(0.5)	
			#Readline() reads from the serial port what is sent back from the Arduino
			response = arduino.readline().decode('utf-8').strip()
			print(f"Received: {response}")
			time.sleep(0.5)
			if "LED ON" in response:
				return True
			return False #If we get here, the response is wrong
	except Exception:
		return False

def print_test_summary(results):
	#Code to create a test summary and print this into the output
	print("=== TEST SUMMARY ===")
	passes = 0
	fails = 0
	for result in results:
		if result["passed"]:
			print(f"✅, {result['test']} : {result['message']}")
			passes = passes + 1
		else:
			print(f"❌, {result['test']} : {result['message']}")
			fails = fails + 1
	no_tests = passes + fails
	print(f"Tests run: {no_tests}")
	print(f"Passed: {passes}")
	print(f"Failed: {fails}")

def log_results_to_file(results, filename):
	#Add results to a log file for test summary
	with open(filename, "a") as file:
		#Write timestamp
		ts = str(datetime.datetime.now())
		file.write(f"\n=== Test Run: {ts} ===\n")

		#Loop through the results and write each one
		for result in results:
			if result["passed"]:
				file.write(f"✅, {result['test']} : {result['message']}")
			else:
				file.write(f"❌, {result['test']} : {result['message']}")

		# Write summary stats
		passes = sum(1 for r in results if r["passed"])
		fails = len(results) - passes
		file.write(f"Tests: {len(results)}, Passed: {passes}, Failed: {fails}\n")
		file.write("---\n\n")  # Separator between run

check = test_arduino_connection()
if check:
	#After each test, append result
	results.append({
        	"test": "Connection Test",
        	"passed": True,
        	"message": "Arduino connected successfully"
	})

	#print("Test Success!")
else:
	results.append({
		"test": "Connection Test",
		"passed": False,
		"message": "Arduino not connected"
	})
	#print("Test Failed!")

check = test_arduino_data()
if check:
        #After each test, append result
	results.append({
        	"test": "Command Send, LED ON",
        	"passed": True,
        	"message": "Arduino LED ON"
	})

	#print("Data Success!")
else:
	results.append({
		"test": "Command Send, LED ON",
		"passed": False,
		"message": "Arduino LED OFF"
        })
	#print("Data Failed!")

print_test_summary(results)

log_results_to_file(results, "arduino_test_log.md")
