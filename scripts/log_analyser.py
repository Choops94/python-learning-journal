#!/usr/bin/python3

#Analyses the fake system.log file

count = 0

with open("./system.log", "r") as file:
	for line in file:
		if "ERROR" in line:
			count = count + 1
			print(line.strip())
print(f"There are {count} error lines")

