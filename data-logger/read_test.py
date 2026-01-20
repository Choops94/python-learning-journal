#!/usr/bin/python3

#Script for reading data from CSV file

import csv
import os

if os.path.exists("weather_log2.csv"):
	# Open file in read mode
	with open("weather_log2.csv", "r") as file:
		reader = csv.reader(file)
		next(reader)
		for row in reader:
			print(type(row[1])) #Print each row of the file
else:
	pass



