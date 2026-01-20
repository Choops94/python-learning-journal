#!/usr/bin/python3

#Script for reading and plotting data

import csv
import os
import matplotlib.pyplot as plt

timestamps = []
temperatures = []
humidity = []

if os.path.exists("weather_log2.csv"):
	#Open file in read mode
	with open("weather_log2.csv", "r") as file:
		reader = csv.reader(file)
		next(reader) #Skip header row
		for row in reader:
			timestamps.append(row[0])
			temperatures.append(float(row[1]))
			humidity.append(float(row[2]))
else:
	pass

print(f"Read {len(temperatures)} data points")
print(f"First temperature: {temperatures[0]}")

#Calculate averages and max
avg_temp = sum(temperatures) / len(temperatures)
avg_hum = sum(humidity) / len(humidity)
max_temp = max(temperatures)
max_hum = max(humidity)
min_temp = min(temperatures)

print(f"Average temperature: {avg_temp:.1f}°C")
print(f"Average humidity: {avg_hum:.1f}°C")
print(f"Max temperature: {max_temp:.1f}°C")
print(f"Max humidity: {max_hum:.1f}°C")
print(f"Min temperature: {min_temp:.1f}C")

#Plot using matplotlib
#plt.plot(range(len(temperatures)), temperatures)
#plt.xlabel('Reading Number')
#plt.ylabel('Temperature (°C)')
#plt.title('Temperature')
#plt.show()

#Subplotting
# Create figure with 2 subplots (2 rows, 1 column)
plt.figure(figsize=(10, 8))  # figsize makes it bigger

# First subplot (top)
plt.subplot(3, 1, 1)  # (rows, cols, position)
plt.plot(range(len(temperatures)), temperatures)
plt.ylabel('Temperature (°C)')
plt.title('Temperature Over Time')
plt.axhline(y=avg_temp, color='r', linestyle='--', label='Average')
plt.legend()

# Second subplot (bottom)
plt.subplot(3, 1, 2)
plt.plot(range(len(humidity)), humidity)
plt.xlabel('Reading Number')
plt.ylabel('Humidity (%)')
plt.title('Humidity Over Time')
plt.axhline(y=avg_hum, color='r', linestyle='--', label='Average')
plt.legend()

# Third subplot
plt.subplot(3, 1, 3)
plt.scatter(temperatures, humidity)
plt.xlabel('Temperature (°C)')
plt.ylabel('Humidity (%)')
plt.title('Temp vs Humidity')

plt.tight_layout()  # Prevents labels from overlapping
plt.show()
