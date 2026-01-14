#!/usr/bin/python3

#Temperature and Humidity logging script - records timestamped temperature readings

import csv
import datetime
import os

if os.path.exists("weather_log.csv"):
        #If file exists - do nothing
        pass
else:
        # Open file in write mode
        with open("weather_log.csv", "w") as file:
                writer = csv.writer(file)

                #Write Header Row
                writer.writerow(["timestamp", "temperature_c", "humidity_percent"])

                print("File created and headers added!")

def log_reading(temp, humid):
        # Open file in write mode
        with open("weather_log.csv", "a") as file:
                writer = csv.writer(file)
                #Current time
                dt = str(datetime.datetime.now())
                # Write temp and humid data entry
                writer.writerow([dt, temp, humid])

                print("Data logged successfully!")

input_temp = float(input("Enter the temperature: "))
input_humid = float(input("Enter the humidity: "))

log_reading(input_temp, input_humid)
