# Python Serial Communication - Quick Reference

## What We Built Today
Created Python scripts to communicate with Arduino over USB serial connection - reading data FROM Arduino and sending commands TO Arduino to control hardware (LED).

---

## What is Serial Communication?

### Core Concepts
- **Serial Port** = Hardware interface for sending data one bit at a time (sequentially)
- **Bidirectional** = Can read AND write simultaneously (unlike files where you choose mode)
- **Baud Rate** = Speed of communication in bits per second (both devices must agree!)
  - Common rates: 9600, 115200
- **Buffer** = Temporary storage for incoming/outgoing data

### Serial vs Files
```python
# Files: Choose read OR write mode
with open("file.txt", "r") as f:    # Read only
with open("file.txt", "w") as f:    # Write only

# Serial: Read AND write on same connection
with serial.Serial('/dev/ttyUSB0', 9600) as port:
    port.write(data)    # Send
    port.readline()     # Receive
```

---

## PySerial Library

### Installation
```bash
pip install pyserial --break-system-packages    # Some systems
pip install pyserial                             # Or just this
pip3 install pyserial                            # Or this
pip3 install --user pyserial                     # If permission errors
```

### Import Convention
```python
import serial    # Import as 'serial' even though package is 'pyserial'
```

### Finding Your Device
```bash
# Linux - Arduino usually appears as:
ls /dev/ttyUSB*    # USB-to-serial adapters
ls /dev/ttyACM*    # Arduino Uno/Mega (native USB)

# Common outputs:
# /dev/ttyUSB0
# /dev/ttyACM0
```

---

## Opening Serial Ports

### Basic Connection
```python
import serial

# Open serial port
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
# ... use port ...
ser.close()    # Don't forget to close!
```

### Using 'with' (Recommended)
```python
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    # Use arduino here
    pass
# Automatically closed when block ends
```

### Connection Parameters
- **Port:** `/dev/ttyUSB0` (Linux), `COM3` (Windows), `/dev/cu.usbserial` (Mac)
- **Baud rate:** Must match Arduino's `Serial.begin()` value
- **Timeout:** Seconds to wait for data (prevents infinite blocking)

### Why time.sleep(2) After Opening?
```python
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    time.sleep(2)    # Arduino resets when serial connection opens!
    # Now Arduino is ready
```

**Important:** Arduinos reset when you open the serial port. The 2-second delay allows the Arduino to boot up and start its `loop()`.

---

## Reading Data FROM Arduino

### Basic Reading
```python
import serial
import time

with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    time.sleep(2)
    
    # Read one line
    line = arduino.readline()    # Returns bytes: b'Hello\r\n'
```

### Converting Bytes to Strings
```python
# Raw bytes (what you receive)
line = arduino.readline()    # b'Hello from Arduino!\r\n'

# Decode to string and clean up
text = line.decode('utf-8').strip()    # 'Hello from Arduino!'
```

**Key Methods:**
- `.decode('utf-8')` = Convert bytes → string
- `.strip()` = Remove `\r\n` (carriage return + newline)

### Reading Multiple Lines
```python
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    time.sleep(2)
    
    for i in range(10):    # Read 10 messages
        line = arduino.readline().decode('utf-8').strip()
        print(f"Received: {line}")
        time.sleep(0.5)
```

### Complete Read Example
```python
#!/usr/bin/python3
import serial
import time

with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    time.sleep(2)
    print("Reading from Arduino...")
    
    for i in range(10):
        line = arduino.readline().decode('utf-8').strip()
        print(f"Received: {line}")
        time.sleep(0.5)
```

---

## Writing Data TO Arduino

### Basic Writing
```python
# Send data as bytes
arduino.write(b'1')                    # Method 1: bytes literal
arduino.write('1'.encode())            # Method 2: encode string
arduino.write('1'.encode('utf-8'))     # Method 3: explicit encoding
```

### Write and Read Response
```python
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    time.sleep(2)
    
    # Send command
    arduino.write(b'1')
    time.sleep(0.5)    # Give Arduino time to process
    
    # Read response
    response = arduino.readline().decode('utf-8').strip()
    print(f"Arduino says: {response}")
```

### Interactive Control Loop
```python
#!/usr/bin/python3
import serial
import time

with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    time.sleep(2)
    print("Arduino Ready!")
    
    while True:
        command = input("Enter command (or 'quit'): ")
        
        if command == "quit":
            break
        
        # Send to Arduino
        arduino.write(command.encode())
        time.sleep(0.5)
        
        # Read response
        response = arduino.readline().decode('utf-8').strip()
        print(f"Response: {response}")
```

---

## Arduino Side (C++ Sketches)

### Basic Send Sketch
```cpp
void setup() {
  Serial.begin(9600);    // Must match Python baud rate!
}

void loop() {
  Serial.println("Hello from Arduino!");
  delay(1000);    // Wait 1 second
}
```

### Basic Receive Sketch (LED Control)
```cpp
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  if (Serial.available() > 0) {    // Check if data waiting
    char command = Serial.read();   // Read one byte
    
    if (command == '1') {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("LED ON");
    }
    else if (command == '0') {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("LED OFF");
    }
  }
}
```

### Key Arduino Functions
- `Serial.begin(9600)` - Initialize serial at baud rate
- `Serial.available()` - Returns number of bytes waiting to be read
- `Serial.read()` - Read one byte (returns char)
- `Serial.println()` - Send line with newline
- `Serial.print()` - Send without newline

---

## Common Patterns

### Send Command, Get Response Function
```python
def send_receive(arduino, command):
    """Send command to Arduino and return response"""
    arduino.write(command.encode())
    time.sleep(0.5)
    response = arduino.readline().decode('utf-8').strip()
    return response

# Usage:
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    time.sleep(2)
    reply = send_receive(arduino, "1")
    print(reply)
```

### Input Validation Pattern
```python
while True:
    command = input("Enter 1 (ON) or 0 (OFF): ")
    
    if command == "quit":
        break
    
    # Validate before sending
    if command not in ["1", "0"]:
        print("Error: Invalid command. Use 1, 0, or quit")
        continue    # Skip to next iteration
    
    # Send valid command
    send_receive(arduino, command)
```

### Continuous Reading Until Keyword
```python
while True:
    line = arduino.readline().decode('utf-8').strip()
    print(line)
    
    if "DONE" in line:    # Stop when Arduino sends DONE
        break
```

---

## Data Types & Conversion

### The Byte Problem
```python
# Arduino sends bytes over serial
received = arduino.readline()    # b'Hello\r\n'
print(received)                  # Shows: b'Hello\r\n'

# Convert to clean string
text = received.decode('utf-8').strip()    # 'Hello'
print(text)                                # Shows: Hello
```

### Encoding & Decoding
```python
# String → Bytes (for sending)
message = "Hello"
bytes_data = message.encode('utf-8')    # b'Hello'
arduino.write(bytes_data)

# Bytes → String (for receiving)
bytes_data = arduino.readline()         # b'Hello\r\n'
message = bytes_data.decode('utf-8')    # 'Hello\r\n'
clean = message.strip()                 # 'Hello'
```

### Why UTF-8?
- UTF-8 = Universal character encoding standard

- Handles ASCII (English) and international characters
- Default encoding for most systems

---

## Input Validation

### Checking Valid Commands
```python
# Method 1: Multiple conditions with 'and'
if command != "1" and command != "0":
    print("Invalid!")

# Method 2: Using 'not in' with list (cleaner!)
if command not in ["1", "0"]:
    print("Invalid!")

# Method 3: Using 'not in' with string
if command not in "10":
    print("Invalid!")
```

### Validation Before Sending
```python
valid_commands = ["1", "0", "ON", "OFF"]

while True:
    cmd = input("Command: ")
    
    if cmd == "quit":
        break
    
    if cmd not in valid_commands:
        print(f"Error: '{cmd}' not recognized")
        print(f"Valid: {', '.join(valid_commands)}")
        continue    # Ask again without sending anything
    
    arduino.write(cmd.encode())
```

---

## Best Practices

### Always Use 'with' Statement
```python
# ✅ GOOD - Automatic cleanup
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    arduino.write(b'data')

# ❌ BAD - Must remember to close
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
arduino.write(b'data')
arduino.close()    # Easy to forget!
```

### Set Appropriate Timeouts
```python
# Timeout too short - might miss slow data
serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)

# Timeout too long - program hangs waiting
serial.Serial('/dev/ttyUSB0', 9600, timeout=10)

# Balanced - works for most cases
serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
```

### Wait After Opening Connection
```python
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    time.sleep(2)    # CRITICAL - Arduino resets on connection!
    # Now safe to communicate
```

### Clear Receive Buffer (Advanced)
```python
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    time.sleep(2)
    arduino.reset_input_buffer()    # Clear any startup messages
    # Now read fresh data
```

### Pass Serial Port to Functions
```python
# ✅ GOOD - Function receives port as parameter
def send_command(arduino, cmd):
    arduino.write(cmd.encode())

with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    send_command(arduino, "1")

# ❌ BAD - Function assumes global 'arduino' exists
def send_command(cmd):
    arduino.write(cmd.encode())    # Where does arduino come from?
```

---

## Troubleshooting

### "PortNotOpenError: Attempting to use a port that is not open"
**Problem:** Trying to use serial port outside `with` block or after closing
**Solution:** Ensure all serial operations are inside the `with` block

```python
# ❌ WRONG
with serial.Serial('/dev/ttyUSB0', 9600) as arduino:
    pass

arduino.write(b'1')    # Error! Port closed after 'with' block

# ✅ CORRECT
with serial.Serial('/dev/ttyUSB0', 9600) as arduino:
    arduino.write(b'1')    # Inside 'with' block
```

### "SerialException: [Errno 16] Device or resource busy"
**Problem:** Another program is using the serial port
**Common causes:**
- Arduino IDE Serial Monitor is open
- Another Python script is running
- Previous script didn't close port properly

**Solution:** Close all other programs using the port

### "SerialException: [Errno 2] No such file or directory: '/dev/ttyUSB0'"
**Problem:** Device not found
**Solutions:**
1. Check device is plugged in
2. Run `ls /dev/ttyUSB*` or `ls /dev/ttyACM*` to find actual device name
3. Check USB cable is data cable (not power-only)
4. On Linux: Add user to `dialout` group: `sudo usermod -a -G dialout $USER`

### "UnicodeDecodeError"
**Problem:** Received data isn't valid UTF-8 text
**Solution:** Arduino might be sending binary data or garbage during startup

```python
try:
    text = arduino.readline().decode('utf-8').strip()
except UnicodeDecodeError:
    print("Received invalid data (Arduino still booting?)")
```

### No Data Received (Empty Strings)
**Problem:** `readline()` returns empty or `b''`
**Possible causes:**
1. Arduino not sending data
2. Timeout too short
3. Baud rate mismatch
4. Reading before Arduino boots (forgot `time.sleep(2)`)

**Debug:**
```python
line = arduino.readline()
print(f"Raw: {line}")    # See what you actually got
print(f"Length: {len(line)}")
```

### Wrong Baud Rate Symptoms
- Receiving garbage characters: `ÃŸÂ§â‚¬Ã†`
- Empty reads
- Partial messages
**Solution:** Ensure Python baud rate matches Arduino's `Serial.begin()` value exactly

---

## Common Mistakes to Avoid

### Forgetting to Decode Bytes
```python
# ❌ WRONG
line = arduino.readline()
print(line)    # Shows: b'Hello\r\n'

# ✅ CORRECT
line = arduino.readline().decode('utf-8').strip()
print(line)    # Shows: Hello
```

### Using 'or' Instead of 'and' in Validation
```python
# ❌ WRONG - This doesn't work as expected!
if command != "1" or command != "0":
    # This is ALWAYS true!

# ✅ CORRECT
if command != "1" and command != "0":
    print("Invalid")

# ✅ BETTER
if command not in ["1", "0"]:
    print("Invalid")
```

### Not Waiting for Arduino to Boot
```python
# ❌ WRONG - Arduino still resetting!
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    arduino.write(b'1')    # Lost! Arduino not ready yet

# ✅ CORRECT
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    time.sleep(2)          # Wait for Arduino to boot
    arduino.write(b'1')    # Now it works
```

### Forgetting to Import time
```python
# ❌ WRONG
import serial
time.sleep(2)    # NameError: name 'time' is not defined

# ✅ CORRECT
import serial
import time
time.sleep(2)
```

### Trying to Read/Write After 'with' Block
```python
# ❌ WRONG
def send_data(command):
    arduino.write(command.encode())    # 'arduino' doesn't exist here!

with serial.Serial('/dev/ttyUSB0', 9600) as arduino:
    send_data("1")

# ✅ CORRECT - Pass port as parameter
def send_data(arduino, command):
    arduino.write(command.encode())

with serial.Serial('/dev/ttyUSB0', 9600) as arduino:
    send_data(arduino, "1")
```

---

## Arduino IDE Basics

### Uploading Sketches
1. **Open Arduino IDE**
2. **Write or paste sketch code**
3. **Select board:** Tools → Board → Arduino Uno (or your model)
4. **Select port:** Tools → Port → `/dev/ttyUSB0` (or your device)
5. **Click Upload** (right arrow icon)
6. **Wait for "Done uploading"**

### Viewing Serial Output from Arduino
- Tools → Serial Monitor (or Ctrl+Shift+M)
- Set baud rate to match sketch (e.g., 9600)
- **IMPORTANT:** Close Serial Monitor before running Python scripts!

### Common Upload Errors
- **"Port busy"** - Close Serial Monitor or Python scripts
- **"Port not found"** - Check USB connection and port selection
- **"Wrong board"** - Select correct board type in Tools → Board

---

## Complete Working Examples

### Example 1: Read Temperature Data
**Arduino Sketch:**
```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  int temp = analogRead(A0);  // Read sensor
  Serial.print("Temperature: ");
  Serial.println(temp);
  delay(1000);
}
```

**Python Script:**
```python
#!/usr/bin/python3
import serial
import time

with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    time.sleep(2)
    print("Reading temperature data...")
    
    while True:
        line = arduino.readline().decode('utf-8').strip()
        if line:    # If not empty
            print(line)
```

### Example 2: LED Control with Validation
**Arduino Sketch:**
```cpp
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    
    if (cmd == '1') {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("LED ON");
    }
    else if (cmd == '0') {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("LED OFF");
    }
    else {
      Serial.println("Unknown command");
    }
  }
}
```

**Python Script:**
```python
#!/usr/bin/python3
import serial
import time

def send_command(arduino, command):
    """Send command and return response"""
    arduino.write(command.encode())
    time.sleep(0.5)
    response = arduino.readline().decode('utf-8').strip()
    return response

with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    time.sleep(2)
    print("LED Controller Ready")
    print("Commands: 1=ON, 0=OFF, quit=Exit")
    
    while True:
        cmd = input("\nEnter command: ")
        
        if cmd == "quit":
            print("Exiting...")
            break
        
        if cmd not in ["1", "0"]:
            print("Error: Invalid command (use 1 or 0)")
            continue
        
        response = send_command(arduino, cmd)
        print(f"Arduino: {response}")
```

---

## Quick Command Reference

### Python Serial Commands
```python
import serial
import time

# Open port
ser = serial.Serial(port, baudrate, timeout=seconds)

# Read operations
ser.read()              # Read 1 byte
ser.read(10)            # Read 10 bytes
ser.readline()          # Read until \n
ser.read_all()          # Read everything in buffer

# Write operations
ser.write(b'data')      # Write bytes
ser.write('text'.encode())  # Write string as bytes

# Buffer management
ser.reset_input_buffer()    # Clear receive buffer
ser.reset_output_buffer()   # Clear send buffer
ser.in_waiting              # Number of bytes waiting to read

# Status
ser.is_open             # True if port open
ser.close()             # Close port manually
```

### Arduino Serial Commands
```cpp
// Setup
Serial.begin(9600);           // Initialize at 9600 baud

// Checking for data
Serial.available()            // Returns number of bytes waiting

// Reading
Serial.read()                 // Read one byte (returns int/char)
Serial.readString()           // Read until timeout (returns String)

// Writing
Serial.print(data)            // Send without newline
Serial.println(data)          // Send with newline
Serial.write(byte)            // Send raw byte
```

---

## Next Steps for Learning

### Beginner Level (What You've Learned)
✅ Basic serial connection setup
✅ Reading data from Arduino
✅ Sending commands to Arduino  
✅ Input validation
✅ LED control

### Intermediate Level (Next Steps)
- Reading sensor data (temperature, distance, light)
- Sending multiple values in one message
- Parsing comma-separated values (CSV over serial)
- Logging sensor data to files
- Real-time plotting of sensor data

### Advanced Level (Future Topics)
- Binary data transmission (struct module)
- Custom communication protocols
- Error checking (checksums)
- Multi-threaded serial reading
- Serial communication with non-Arduino devices
- Modbus, I2C, SPI protocols

---

## Real-World Applications

### Home Automation
- Control lights, fans, motors via Python scripts
- Read temperature/humidity sensors
- Trigger actions based on sensor data

### Data Acquisition
- Log environmental data (temp, pressure, light)
- Monitor equipment status
- Record measurements for analysis

### Robotics
- Send movement commands to robot
- Receive sensor feedback
- Implement control loops

### Lab Equipment
- Control power supplies, function generators
- Automate measurement sequences
- Interface custom hardware

### 3D Printing
- Send G-code commands
- Monitor print progress
- Custom printer control interfaces

---

## Key Takeaways

1. **Serial is bidirectional** - read and write simultaneously once open
2. **Baud rates must match** - Python and Arduino must agree on speed
3. **Bytes vs strings matter** - use `.encode()` to send, `.decode()` to receive
4. **Arduino resets on connection** - always `time.sleep(2)` after opening
5. **Always use 'with' statement** - ensures port closes properly
6. **Validate input in Python** - before sending to hardware
7. **One program at a time** - serial port can't be shared
8. **UTF-8 is standard** - for encoding/decoding text
9. **readline() waits for newline** - Arduino should use `println()` not `print()`
10. **Timeout prevents hanging** - set reasonable timeout value

---

## Resources

### Python Documentation
- **PySerial Docs:** https://pyserial.readthedocs.io/
- **Serial Module API:** https://pyserial.readthedocs.io/en/latest/pyserial_api.html

### Arduino Resources
- **Arduino Language Reference:** https://www.arduino.cc/reference/en/
- **Serial Reference:** https://www.arduino.cc/reference/en/language/functions/communication/serial/
- **Built-in Examples:** File → Examples → 04.Communication

### Learning Platforms
- **Arduino Project Hub:** https://create.arduino.cc/projecthub
- **PySerial Examples:** https://github.com/pyserial/pyserial/tree/master/examples

---

## Quick Troubleshooting Checklist

When something doesn't work:

- [ ] Is Arduino plugged in?
- [ ] Is correct port selected? (`ls /dev/ttyUSB*`)
- [ ] Is Arduino IDE Serial Monitor closed?
- [ ] Do baud rates match? (Python and Arduino `Serial.begin()`)
- [ ] Did you wait 2 seconds after opening port? (`time.sleep(2)`)
- [ ] Are you decoding received bytes? (`.decode('utf-8')`)
- [ ] Are you encoding sent strings? (`.encode()`)
- [ ] Is code inside the `with` block?
- [ ] Did you import both `serial` and `time`?
- [ ] Is Arduino sketch uploaded successfully?

---

## Scripts Created Today

1. **read_arduino.py** - Read data FROM Arduino
   - Demonstrates receiving serial data
   - Shows byte to string conversion
   - Uses loop to read multiple messages

2. **control_led.py** - Send commands TO Arduino
   - Interactive LED control
   - Input validation
   - Function for send/receive pattern
   - Continuous loop with quit option

Both committed to git repository: `serial-comms/`
