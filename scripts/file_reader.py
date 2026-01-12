#!/usr/bin/python3

#Simple file reader script

#with open("./fruits.txt", "r") as file:
#	content = file.read()
#	print(content)

#Line by line read

with open("./fruits.txt", "r") as file:
	for line in file:
		print(line.strip())

