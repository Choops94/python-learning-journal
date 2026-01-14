#!/usr/bin/python3

#Temperature and Humidity continuous logging script - records timestamped temperature readings

import csv
import datetime
import os

if os.path.exists("weather_log2.csv"):
        #If file exists - do nothing
        pass
else:
        # Open file in write mode
        with open("weather_log2.csv", "w") as file:
                writer = csv.writer(file)

                #Write Header Row
                writer.writerow(["timestamp", "temperature_c", "humidity_percent"])

                print("File created and headers added!")

def log_reading(temp, humid):
        # Open file in write mode
        with open("weather_log2.csv", "a") as file:
                writer = csv.writer(file)
                #Current time
                dt = str(datetime.datetime.now())
                # Write temp and humid data entry
                writer.writerow([dt, temp, humid])

                print("Data logged successfully!")

while True:
	#Input the temp and humid
	input_temp = input("Enter the temperature: ")

	#Check if the input is 'quit'
	if input_temp == "quit":
		break
	else:
		#input humidity
		input_humid = input("Enter the humidity: ")

		#Check if input is 'quit'
		if input_humid == "quit":
			break
		else:

		#Convert to float
		it = float(input_temp)
		ih = float(input_humid)

		log_reading(it, ih)
