#!/usr/bin/python3

#Even/Odd Filter

#My attempt
numbers = range(1,21)

for number in numbers:
	result1 = number % 2
	if result1 > 0:
		result2 = "odd"
	else:
		result2 = "even"
	print(f"{number} is", result2)

#Imporved solution
for number in range(1, 21):
    if number % 2 == 0:
        print(f"{number} is even")
    else:
        print(f"{number} is odd")

#Checks the remainder directly
#Efficient variable use
#More concise
