#!/usr/bin/python3

#Temperature logging script - records timestamped temperature readings

import csv
import datetime
import os

if os.path.exists("temperature_log.csv"):
	#If file exists - do nothing
	pass
else:
	# Open file in write mode
        with open("temperature_log.csv", "w") as file:
                writer = csv.writer(file)

                #Write Header Row
                writer.writerow(["timestamp", "temperature_c"])

                print("File created and headers added!")

def log_temperature(temp):
	# Open file in write mode
	with open("temperature_log.csv", "a") as file:
		writer = csv.writer(file)
		#Current time
		dt = str(datetime.datetime.now())
		# Write one data entry
		writer.writerow([dt, temp])

		print("Data logged successfully!")

input_temp = float(input("Enter the temperature"))

log_temperature(input_temp)


