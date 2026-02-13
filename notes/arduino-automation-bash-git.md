# Python Test Automation Workflow - Quick Reference

## What We Built Today
Created a **complete automated testing workflow** that integrates hardware sensors, Python test scripts, Bash orchestration, and Git version control - a real-world example of continuous integration for IoT devices.

---

## Project Architecture

### The Complete Workflow
```
Arduino (DHT11 Sensor)
    ↓ USB Serial
Python Test Script (test_dht_temp_hum.py)
    ↓ Runs tests, validates data
Log Files (CSV + Markdown)
    ↓ Test results stored
Bash Script (run_dht_tests.sh)
    ↓ Orchestrates everything
Git Repository
    ↓ Version controlled history
```

### File Structure
```
arduino-automation/
├── scripts/
│   ├── test_dht_temp_hum.py    # Python test script
│   └── run_dht_tests.sh         # Bash orchestration
├── logs/
│   ├── dht_data.csv             # Time-series sensor data
│   └── dht_temp_hum_log.md      # Test summaries
└── notes/
    └── (documentation)
```

---

## Arduino Integration

### Sensor Setup (DHT11)
- **Hardware:** KY-015 Temperature & Humidity Sensor
- **Connections:**
  - Signal → Digital Pin 2
  - +V → 5V
  - GND → GND

### Arduino Sketch Design Principles

**Output Format for Automation:**
```cpp
// BAD - Hard to parse
Serial.println("Temperature: 22.5°C  Humidity: 68%");

// GOOD - Easy to parse
Serial.println("TEMP:22.5,HUM:68.0");

// GOOD - Error handling
Serial.println("ERROR:Failed to read sensor");
```

**Key Pattern:**
```cpp
void loop() {
  delay(2000);  // Sample rate
  
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  if (isnan(h) || isnan(t)) {
    Serial.println("ERROR:Failed to read sensor");
    return;
  }
  
  // Structured output
  Serial.print("TEMP:");
  Serial.print(t);
  Serial.print(",HUM:");
  Serial.println(h);
}
```

**Why This Format?**
- Easy to parse with `.split()`
- Distinguishable from debug messages
- Handles errors explicitly
- No spaces (simpler parsing)

---

## Python Test Architecture

### Core Design Principle: Separation of Concerns

**Test functions** = Execute tests and return raw data
**Main code** = Decide what to do with results (print, log, analyze)

### Test Function Pattern

**Simple Test (Connection Check):**
```python
def test_arduino_connection():
    """Test if Arduino connects successfully"""
    try:
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
            time.sleep(2)  # Wait for Arduino reset
            return {"test_name": "Arduino Connection", "passed": True}
    except Exception:
        return {"test_name": "Arduino Connection", "passed": False}
```

**Complex Test (Data Validation):**
```python
def test_dht_sensor_readings():
    """Test DHT sensor data is valid"""
    fail_num_t = 0
    fail_num_h = 0
    temp = []
    humid = []
    
    try:
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
            time.sleep(2)
            
            # Read multiple samples
            for num in range(1, 4):
                output = arduino.readline().decode().strip()
                
                # Handle different message types
                if output.startswith("TEMP:"):
                    # Parse valid data
                    parts = output.split("TEMP:")[1].split(",HUM:")
                    temp.append(float(parts[0]))
                    humid.append(float(parts[1]))
                    
                    # Validate ranges
                    if temp[-1] < 0 or temp[-1] > 50.0:
                        fail_num_t += 1
                    if humid[-1] < 20.0 or humid[-1] > 90.0:
                        fail_num_h += 1
                        
                elif output.startswith("ERROR:"):
                    # Count errors
                    fail_num_t += 1
                    fail_num_h += 1
                    temp.append("Error")
                    humid.append("Error")
                    continue
                    
                else:
                    # Skip garbage/header
                    temp.append("Error")
                    humid.append("Error")
                    continue
            
            # Return structured result
            return {
                "test_name": "DHT Sensor Readings",
                "passed": fail_num_t == 0 and fail_num_h == 0,
                "temp_failures": fail_num_t,
                "hum_failures": fail_num_h,
                "samples": [
                    {"temp": temp[0], "hum": humid[0]},
                    {"temp": temp[1], "hum": humid[1]},
                    {"temp": temp[2], "hum": humid[2]}
                ]
            }
    except Exception:
        return {
            "test_name": "DHT Sensor Readings",
            "passed": False,
            "temp_failures": 3,
            "hum_failures": 3,
            "samples": []
        }
```

---

## Parsing Serial Data

### The Challenge
Arduino outputs: `"TEMP:22.5,HUM:68.0"`
Need to extract: `temp = 22.5`, `humidity = 68.0`

### Parsing Approaches

**Method 1: Split on keywords**
```python
line = "TEMP:22.5,HUM:68.0"
parts = line.split("TEMP:")  # ['', '22.5,HUM:68.0']
data = parts[1].split(",HUM:")  # ['22.5', '68.0']
temp = float(data[0])
humidity = float(data[1])
```

**Method 2: Split on comma first**
```python
line = "TEMP:22.5,HUM:68.0"
parts = line.split(",")  # ['TEMP:22.5', 'HUM:68.0']
temp = float(parts[0].split(":")[1])
humidity = float(parts[1].split(":")[1])
```

**Both work!** Choose what makes sense to you.

### Defensive Parsing Pattern
```python
output = arduino.readline().decode().strip()

if output.startswith("TEMP:"):
    # Parse as valid data
    pass
elif output.startswith("ERROR:"):
    # Handle sensor error
    pass
else:
    # Skip unknown/garbage
    continue
```

**Why this is robust:**
- Handles Arduino startup messages
- Distinguishes errors from data
- Won't crash on unexpected input
- Silently skips garbage

---

## Data Logging Strategies

### Two Log Types, Two Purposes

**CSV Log - Time-Series Data:**
```python
def log_to_csv(result_dict):
    """Log sensor samples to CSV with timestamp"""
    csv_path = "path/to/dht_data.csv"
    
    # Create with headers if new
    if not os.path.exists(csv_path):
        with open(csv_path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "temp_c", "humid_percent"])
    
    # Append samples
    with open(csv_path, "a") as file:  # APPEND mode
        writer = csv.writer(file)
        timestamp = str(datetime.datetime.now())
        
        # Only log valid samples
        for sample in result_dict["samples"]:
            if sample["temp"] != "Error" and sample["hum"] != "Error":
                writer.writerow([timestamp, sample["temp"], sample["hum"]])
```

**Markdown Log - Test Summaries:**
```python
def log_summary(results_list):
    """Log test summary to markdown file"""
    with open(log_path, "a") as file:
        timestamp = str(datetime.datetime.now())
        file.write(f"\n=== Test Run: {timestamp} ===\n")
        
        for result in results_list:
            status = "✅" if result["passed"] else "❌"
            file.write(f"{status} {result['test_name']}: ")
            file.write(f"{'PASS' if result['passed'] else 'FAIL'}\n")
            
            # Add details for sensor tests
            if "temp_failures" in result:
                file.write(f"  Temp failures: {result['temp_failures']}/3\n")
                file.write(f"  Humidity failures: {result['hum_failures']}/3\n")
        
        file.write("---\n")
```

### CSV Design Decisions

**Option A - Wide format (all samples in one row):**
```csv
timestamp, temp1, temp2, temp3, hum1, hum2, hum3
2026-02-13 10:00:00, 22.5, 22.3, 22.4, 68.0, 68.5, 68.2
```

**Option B - Long format (one sample per row):**
```csv
timestamp, temp_c, humid_percent
2026-02-13 10:00:00, 22.5, 68.0
2026-02-13 10:00:00, 22.3, 68.5
2026-02-13 10:00:00, 22.4, 68.2
```

**We chose Option B because:**
- Easier to plot (one column per variable)
- Easier to filter and analyze
- Standard format for time-series data
- Works with pandas, matplotlib seamlessly

---

## Bash Orchestration Script

### Purpose
Automate the entire workflow: run tests → log results → commit to Git

### Complete Script Pattern
```bash
#!/bin/bash

# Script header with description
echo "=== DHT Sensor Test Automation ==="
echo "Starting test run at $(date)"
echo ""

# Run the Python test script
python3 /path/to/test_dht_temp_hum.py

# Check if tests succeeded
if [ $? -eq 0 ]; then
    echo ""
    echo "Tests completed successfully!"
    echo "Committing results to Git..."
    
    # Navigate to repo
    cd /path/to/repo
    
    # Stage log files
    git add arduino-automation/logs/dht_temp_hum_log.md
    git add arduino-automation/logs/dht_data.csv
    
    # Commit with timestamp
    git commit -m "Automated DHT sensor test - $(date '+%Y-%m-%d %H:%M:%S')"
    
    echo "Results committed to Git!"
else
    echo ""
    echo "Tests failed! Check the output above."
    exit 1
fi
```

### Key Bash Concepts

**Exit Status Check:**
```bash
python3 script.py
if [ $? -eq 0 ]; then  # $? = exit status of last command
    echo "Success!"
else
    echo "Failed!"
    exit 1
fi
```

**Command Substitution:**
```bash
echo "Time: $(date)"  # Runs date command, inserts output
git commit -m "Test - $(date '+%Y-%m-%d %H:%M:%S')"
```

**Making Scripts Executable:**
```bash
chmod +x run_dht_tests.sh
./run_dht_tests.sh  # Run it
```

---

## Main Execution Pattern

### Structure
```python
if __name__ == "__main__":
    # Initialize results storage
    results = []
    
    # Run all tests
    results.append(test_arduino_connection())
    results.append(test_dht_sensor_readings())
    
    # Log data (only sensor test has samples)
    log_to_csv(results[1])
    
    # Log summary (all tests)
    log_summary(results)
    
    # User feedback
    print("Tests complete! Check logs/")
```

### Why This Pattern?
- Tests are independent (can add/remove easily)
- All results stored in one list
- Clear separation: test → log → report
- Easy to extend with more tests

---

## Common Pitfalls & Solutions

### Issue 1: Arduino Startup Messages
**Problem:** Arduino prints header in `setup()`, Python tries to parse it as data
**Solution:** Defensive parsing with `if output.startswith("TEMP:")`

### Issue 2: Empty List Indexing
```python
# WRONG
temp = []
temp[0] = 22.5  # IndexError!

# RIGHT
temp = []
temp.append(22.5)  # Works!
```

### Issue 3: File Mode Confusion
```python
# WRONG - Overwrites file every time
with open("log.csv", "w") as file:
    writer.writerow([new_data])

# RIGHT - Appends to existing file
with open("log.csv", "a") as file:
    writer.writerow([new_data])
```

### Issue 4: Timestamp Placement
```python
# LESS USEFUL - Same timestamp for all samples
timestamp = str(datetime.datetime.now())
for sample in samples:
    write(timestamp, sample)

# ACCEPTABLE FOR TEST RUNS - All samples from one test
# (They were collected in same 6-second window)
```

### Issue 5: Path Expansion
```python
# WRONG - Tilde doesn't expand in Python strings
path = "~/folder/file.txt"

# RIGHT - Use expanduser
path = os.path.expanduser("~/folder/file.txt")

# OR - Use absolute path
path = "/home/username/folder/file.txt"
```

---

## Testing Best Practices

### Test Design Principles

**1. Independence**
Each test should work on its own (no shared state)

**2. Repeatability**
Same input = same output every time

**3. Fast Execution**
Quick tests = run them often
(3 samples @ 2s each = 6s total is reasonable)

**4. Clear Pass/Fail**
No ambiguity about test results

**5. Informative Failures**
When test fails, provide diagnostic info

### Validation Strategy

**For DHT11 Sensor:**
- Temperature range: 0-50°C
- Humidity range: 20-90%
- All samples must pass (stable sensor, slow rate)

**Decision Tree:**
```
Read sample
  ↓
Starts with "TEMP:"? → Yes → Parse and validate ranges
  ↓ No
Starts with "ERROR:"? → Yes → Count as failure
  ↓ No
Unknown/garbage → Skip silently
```

### Error Handling Philosophy

**In Test Functions:**
```python
try:
    # Test logic
    return result_dict
except Exception:
    # Return failure, don't crash
    return {"passed": False, ...}
```

**Never let tests crash the automation!**

---

## Return Value Patterns

### Simple Boolean Return
```python
def test_simple():
    if condition:
        return True
    return False
```

**Use when:** Quick yes/no check

### Dictionary Return
```python
def test_complex():
    return {
        "test_name": "My Test",
        "passed": True/False,
        "details": "Additional info",
        "data": [samples]
    }
```

**Use when:** Need rich diagnostic information

### Why Dictionaries?
- Self-documenting (keys explain values)
- Flexible (easy to add new fields)
- Easy to process in loops
- Standard in Python testing frameworks

---

## Git Integration

### Automated Commits Pattern
```bash
# Stage specific files
git add logs/summary.md
git add logs/data.csv

# Commit with informative message
git commit -m "Automated test - $(date '+%Y-%m-%d %H:%M:%S')"
```

### Commit Message Best Practices
- Include timestamp
- Indicate automated vs manual
- Keep format consistent
- Makes history searchable

### What to Commit
**DO commit:**
- Test summaries (markdown logs)
- Configuration files
- Test scripts themselves

**CONSIDER carefully:**
- Large CSV files (they grow!)
- Binary data
- Temporary outputs

**For this project:** We commit CSVs because they're small and valuable for historical analysis

---

## Workflow Optimization

### Current Workflow (What We Built)
```
Manual trigger (./run_dht_tests.sh)
  ↓
Run tests (6 seconds)
  ↓
Log results
  ↓
Commit to Git
```

### Future Enhancements

**1. Scheduled Execution (cron)**
```bash
# Run tests every hour
0 * * * * /path/to/run_dht_tests.sh
```

**2. Continuous Logging (Separate Script)**
```python
while True:
    sample = read_sensor()
    log_to_csv(sample)
    time.sleep(2)
```

**3. Alerts on Failure**
```bash
if [ $? -ne 0 ]; then
    echo "Test failed!" | mail -s "Alert" user@example.com
fi
```

**4. Dashboard/Plotting**
```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("dht_data.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])
plt.plot(df['timestamp'], df['temp_c'])
plt.show()
```

---

## Key Takeaways

### Technical Skills
✅ Serial communication between Python and Arduino
✅ Structured data formats for machine parsing
✅ Defensive programming (error handling)
✅ Separation of concerns (test vs report)
✅ File I/O with CSV and text files
✅ Bash scripting for orchestration
✅ Git automation

### Design Principles
✅ Make output parseable (TEMP:X,HUM:Y)
✅ Test functions return data, don't print
✅ Handle errors gracefully (don't crash)
✅ Log both summaries and raw data
✅ Use version control for accountability

### Real-World Applications
- IoT device validation
- Hardware-in-the-loop testing
- Environmental monitoring
- Quality assurance automation
- Continuous integration pipelines

---

## Quick Command Reference

### Python
```python
# Serial communication
import serial
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
    line = arduino.readline().decode().strip()

# CSV logging
import csv
with open("file.csv", "a") as file:
    writer = csv.writer(file)
    writer.writerow([timestamp, value1, value2])

# Timestamps
import datetime
timestamp = str(datetime.datetime.now())

# File existence check
import os
if not os.path.exists("file.csv"):
    # Create it
```

### Bash
```bash
# Run Python script
python3 /path/to/script.py

# Check exit status
if [ $? -eq 0 ]; then
    echo "Success"
fi

# Command substitution
git commit -m "Test - $(date '+%Y-%m-%d %H:%M:%S')"

# Make executable
chmod +x script.sh
```

### Git
```bash
# Stage files
git add file1.txt file2.csv

# Commit
git commit -m "message"

# View history
git log --oneline -5
```

---

## Project Files Created

### Python Script
- **File:** `test_dht_temp_hum.py`
- **Purpose:** Run automated tests on DHT11 sensor
- **Functions:**
  - `test_arduino_connection()` - Check serial connection
  - `test_dht_sensor_readings()` - Validate sensor data
  - `log_to_csv()` - Store time-series data
  - `log_summary()` - Store test summaries

### Bash Script
- **File:** `run_dht_tests.sh`
- **Purpose:** Orchestrate testing workflow
- **Actions:**
  1. Run Python tests
  2. Check results
  3. Commit to Git

### Log Files
- **CSV:** `dht_data.csv` - Raw sensor readings
- **Markdown:** `dht_temp_hum_log.md` - Test summaries

### Arduino Sketch
- **File:** `dht_sensor_read.ino`
- **Purpose:** Read DHT11 and output formatted data
- **Output:** `TEMP:22.5,HUM:68.0` or `ERROR:message`

---

## Resources for Further Learning

### Testing Frameworks
- **pytest** - Industry standard Python testing
- **unittest** - Built-in Python testing module
- **GitHub Actions** - Cloud-based CI/CD

### Data Analysis
- **pandas** - DataFrame manipulation
- **matplotlib** - Data visualization
- **jupyter** - Interactive notebooks

### IoT/Hardware
- **MQTT** - Messaging protocol for IoT
- **InfluxDB** - Time-series database
- **Grafana** - Real-time dashboards

### Automation
- **cron** - Scheduled task execution
- **systemd** - Service management
- **Docker** - Containerization

---

## Next Steps

### Immediate Improvements
1. Add more sensor types (pressure, light, etc.)
2. Implement trend analysis (detect anomalies)
3. Create visualization dashboard
4. Set up scheduled execution (cron)

### Advanced Features
1. Remote monitoring (send data to cloud)
2. Email/SMS alerts on failures
3. Machine learning for prediction
4. Multi-device testing

### Production Deployment
1. Error recovery (retry logic)
2. Logging levels (DEBUG, INFO, ERROR)
3. Configuration files (not hardcoded paths)
4. Documentation (README, API docs)

---

## Final Thoughts

This workflow demonstrates the **fundamentals of automated testing**:
- **Arrange** (connect to hardware, prepare test)
- **Act** (read data, execute test logic)
- **Assert** (validate results)
- **Report** (log outcomes)
- **Automate** (Bash orchestration + Git)

These same principles apply to:
- Software testing (unit tests, integration tests)
- Web application testing (Selenium, API tests)
- Database validation
- System administration tasks

**The pattern scales:** Add more tests, more sensors, more complexity - the architecture stays the same!
