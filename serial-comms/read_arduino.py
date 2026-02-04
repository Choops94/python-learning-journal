#!/usr/bin/python3
import serial
import time

# Open serial port
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    time.sleep(2)  # Wait for connection to stabilize
    
    print("Reading from Arduino...")
    for i in range(10):  # Read 10 messages
        line = arduino.readline().decode('utf-8').strip()
        print(f"Received: {line}")
        time.sleep(0.5)
