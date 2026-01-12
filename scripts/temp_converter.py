#!/usr/bin/python3

#Temperature converter script -  celsius to farenheit
#Attempt 1
def temp_conv(temp):
	return (temp * 9/5) + 32 

#result = temp_conv(0)
#print(f"0 celsuis is {result} farenheit")
#
#result = temp_conv(25)
#print(f"25 celsuis is {result} farenheit")
#
#result = temp_conv(100)
#print(f"100 celsuis is {result} farenheit")

temps = [0, 25, 100]
for t in temps:
	result = temp_conv(t)
	print(f"{t} celsuis is {result} farenheit")

