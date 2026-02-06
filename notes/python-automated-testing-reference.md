# Python Automated Testing - Quick Reference

## What We Built Today
Created an **automated test suite** for Arduino hardware that runs tests, validates responses, logs results to a file, and provides a pass/fail summary - foundational skills for software testing and quality assurance.

---

## What is Automated Testing?

### Core Concepts
- **Automated Testing** = Writing code that tests other code/hardware automatically
- **Test Suite** = Collection of multiple tests that verify different aspects of a system
- **Test Result** = Pass or Fail outcome with details about what was tested

### Why Automate Tests?
- ✅ Consistency - Same tests run the exact same way every time
- ✅ Speed - Run hundreds of tests in seconds
- ✅ Repeatability - Test after every code change
- ✅ Documentation - Tests show how system should behave
- ✅ Confidence - Know immediately when something breaks

### The Testing Workflow
1. **Arrange** - Set up the test conditions
2. **Act** - Perform the action being tested
3. **Assert** - Verify the result is correct
4. **Report** - Log the outcome

---

## Error Handling with try/except

### Basic Pattern
```python
try:
    # Code that might fail
    risky_operation()
    return True  # Success!
except Exception:
    # What to do if it fails
    return False  # Failure
```

### Why Use try/except in Tests?
- Tests should **never crash** - they should report failures gracefully
- Catches errors and converts them to test failures
- Allows test suite to continue even if one test fails

### Common Exceptions
```python
try:
    num = int("hello")
except ValueError:
    print("Not a number!")

try:
    file = open("missing.txt")
except FileNotFoundError:
    print("File doesn't exist!")

try:
    port = serial.Serial('/dev/ttyUSB0', 9600)
except serial.SerialException:
    print("Can't open serial port!")
```

### Catching Any Exception
```python
except Exception:  # Catches all errors (use for general testing)
```

---

## Writing Test Functions

### Test Function Pattern
```python
def test_something():
    """Test that something works correctly"""
    try:
        # Arrange - Set up
        setup_needed_resources()
        
        # Act - Do the thing
        result = perform_action()
        
        # Assert - Check if correct
        if result == expected_value:
            return True
        return False
        
    except Exception:
        return False  # Any error = test failed
```

### Best Practices for Test Functions
- **Descriptive names** - `test_arduino_connection()` not `test1()`
- **Return boolean** - `True` for pass, `False` for fail
- **One concept per test** - Test one thing at a time
- **Independent tests** - Each test should work on its own
- **Use try/except** - Catch errors gracefully

### Example: Connection Test
```python
def test_arduino_connection():
    """Test if we can connect to Arduino"""
    try:
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
            time.sleep(2)  # Wait for Arduino to initialize
            return True
    except Exception:
        return False
```

### Example: Data Validation Test
```python
def test_arduino_response():
    """Test if Arduino responds to commands correctly"""
    try:
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
            time.sleep(2)
            
            # Send command
            arduino.write(b'1')
            time.sleep(0.5)
            
            # Read response
            response = arduino.readline().decode('utf-8').strip()
            
            # Validate response
            if "LED ON" in response:
                return True
            return False
            
    except Exception:
        return False
```

---

## Storing Test Results

### Using Dictionaries for Results
```python
result = {
    "test": "Connection Test",
    "passed": True,
    "message": "Arduino connected successfully"
}
```

### Building a Results List
```python
results = []  # Initialize empty list

# After each test
test_passed = test_arduino_connection()

if test_passed:
    results.append({
        "test": "Connection Test",
        "passed": True,
        "message": "Arduino connected successfully"
    })
else:
    results.append({
        "test": "Connection Test",
        "passed": False,
        "message": "Failed to connect to Arduino"
    })
```

### Why Store Results?
- Generate summary reports
- Log to files
- Track which tests failed
- Count pass/fail statistics
- Historical tracking

---

## Printing Test Summaries

### Summary Function Pattern
```python
def print_test_summary(results):
    """Print a formatted summary of all test results"""
    print("=== TEST SUMMARY ===")
    
    passes = 0
    fails = 0
    
    # Loop through each result
    for result in results:
        if result["passed"]:
            print(f"✅ {result['test']}: {result['message']}")
            passes += 1
        else:
            print(f"❌ {result['test']}: {result['message']}")
            fails += 1
    
    # Print statistics
    total = passes + fails
    print(f"\nTests run: {total}")
    print(f"Passed: {passes}")
    print(f"Failed: {fails}")
```

### Accessing Dictionary Values
```python
result = {"test": "My Test", "passed": True, "message": "Success!"}

# Access values with brackets
test_name = result["test"]
did_pass = result["passed"]
msg = result["message"]
```

### Counting with Loops
```python
# Method 1: Counter variable
count = 0
for item in items:
    if condition:
        count += 1  # Same as: count = count + 1

# Method 2: List comprehension with sum
count = sum(1 for item in items if condition)

# Method 3: Simple math
total = passes + fails
```

---

## Logging Results to Files

### File Logging Pattern
```python
import datetime

def log_results_to_file(results, filename):
    """Append test results to a log file"""
    with open(filename, "a") as file:  # "a" = append mode
        # Write timestamp
        timestamp = str(datetime.datetime.now())
        file.write(f"\n=== Test Run: {timestamp} ===\n")
        
        # Write each result
        for result in results:
            if result["passed"]:
                file.write(f"✅ {result['test']}: {result['message']}\n")
            else:
                file.write(f"❌ {result['test']}: {result['message']}\n")
        
        # Write summary
        passes = sum(1 for r in results if r["passed"])
        fails = len(results) - passes
        file.write(f"Tests: {len(results)}, Passed: {passes}, Failed: {fails}\n")
        file.write("---\n\n")  # Separator
```

### File Modes Reminder
- `"r"` - Read (file must exist)
- `"w"` - Write (overwrites entire file)
- `"a"` - Append (adds to end of file)

### Initializing Log Files
```python
import os

# Create file with header if it doesn't exist
if not os.path.exists("test_log.txt"):
    with open("test_log.txt", "w") as file:
        file.write("=== TEST LOG ===\n")
```

### Adding Timestamps
```python
import datetime

# Get current date/time
now = datetime.datetime.now()

# Convert to string for logging
timestamp = str(now)
# Output: "2025-01-15 14:30:45.123456"

# Use in log
file.write(f"Test run at: {timestamp}\n")
```

---

## Complete Test Suite Example

### Full Working Script
```python
#!/usr/bin/python3
import serial
import time
import datetime
import os

# Initialize results list
results = []

# Create log file if doesn't exist
if not os.path.exists("test_log.txt"):
    with open("test_log.txt", "w") as file:
        file.write("=== TEST LOG ===\n")

def test_arduino_connection():
    """Test if Arduino connects successfully"""
    try:
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
            time.sleep(2)
            return True
    except Exception:
        return False

def test_arduino_command():
    """Test if Arduino responds to LED command"""
    try:
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as arduino:
            time.sleep(2)
            arduino.write(b'1')
            time.sleep(0.5)
            response = arduino.readline().decode('utf-8').strip()
            
            if "LED ON" in response:
                return True
            return False
    except Exception:
        return False

def print_test_summary(results):
    """Print formatted test summary"""
    print("=== TEST SUMMARY ===")
    passes = 0
    fails = 0
    
    for result in results:
        if result["passed"]:
            print(f"✅ {result['test']}: {result['message']}")
            passes += 1
        else:
            print(f"❌ {result['test']}: {result['message']}")
            fails += 1
    
    total = passes + fails
    print(f"\nTests run: {total}")
    print(f"Passed: {passes}")
    print(f"Failed: {fails}")

def log_results_to_file(results, filename):
    """Log test results to file"""
    with open(filename, "a") as file:
        timestamp = str(datetime.datetime.now())
        file.write(f"\n=== Test Run: {timestamp} ===\n")
        
        for result in results:
            status = "✅" if result["passed"] else "❌"
            file.write(f"{status} {result['test']}: {result['message']}\n")
        
        passes = sum(1 for r in results if r["passed"])
        fails = len(results) - passes
        file.write(f"Tests: {len(results)}, Passed: {passes}, Failed: {fails}\n")
        file.write("---\n\n")

# Run Test 1
check = test_arduino_connection()
if check:
    results.append({
        "test": "Connection Test",
        "passed": True,
        "message": "Arduino connected successfully"
    })
else:
    results.append({
        "test": "Connection Test",
        "passed": False,
        "message": "Failed to connect to Arduino"
    })

# Run Test 2
check = test_arduino_command()
if check:
    results.append({
        "test": "LED Command Test",
        "passed": True,
        "message": "Arduino responded with LED ON"
    })
else:
    results.append({
        "test": "LED Command Test",
        "passed": False,
        "message": "Arduino did not respond correctly"
    })

# Display and log results
print_test_summary(results)
log_results_to_file(results, "test_log.txt")
```

---

## Common Testing Patterns

### Testing Serial Communication
```python
def test_serial_read():
    """Test reading data from serial device"""
    try:
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as device:
            time.sleep(2)
            data = device.readline().decode('utf-8').strip()
            
            # Check data is not empty
            if data == "":
                return False
            
            # Check data is valid
            if "EXPECTED_TEXT" in data:
                return True
            
            return False
    except Exception:
        return False
```

### Testing Numeric Ranges
```python
def test_sensor_reading():
    """Test if sensor reading is within valid range"""
    try:
        reading = get_sensor_value()
        
        # Convert to number
        value = float(reading)
        
        # Check range (e.g., temperature between 0-50°C)
        if 0 <= value <= 50:
            return True
        return False
        
    except (ValueError, Exception):
        return False
```

### Testing Data Validation
```python
def test_data_format():
    """Test if data matches expected format"""
    try:
        data = get_data()
        
        # Check not empty
        if not data:
            return False
        
        # Check contains expected parts
        if ":" in data:
            parts = data.split(":")
            if len(parts) == 2:
                return True
        
        return False
    except Exception:
        return False
```

---

## Testing Best Practices

### Organizing Tests
```python
# Group related tests
def test_connection():
    """Tests basic connectivity"""
    pass

def test_read_data():
    """Tests data reading"""
    pass

def test_write_command():
    """Tests sending commands"""
    pass

# Run all tests
results = []
results.append(run_and_record(test_connection, "Connection Test"))
results.append(run_and_record(test_read_data, "Read Data Test"))
results.append(run_and_record(test_write_command, "Write Command Test"))
```

### Helper Function for Running Tests
```python
def run_test(test_func, test_name, success_msg, fail_msg):
    """Run a test function and return formatted result"""
    passed = test_func()
    
    return {
        "test": test_name,
        "passed": passed,
        "message": success_msg if passed else fail_msg
    }

# Usage
result = run_test(
    test_arduino_connection,
    "Arduino Connection",
    "Connected successfully",
    "Connection failed"
)
results.append(result)
```

### Test Independence
```python
# ✅ GOOD - Each test is independent
def test_connection():
    with serial.Serial(...) as device:
        return device.is_open

def test_read():
    with serial.Serial(...) as device:
        data = device.readline()
        return len(data) > 0

# ❌ BAD - Tests depend on shared state
device = serial.Serial(...)  # Global connection

def test_connection():
    return device.is_open  # Depends on global state

def test_read():
    return device.readline()  # Shares same connection
```

### Meaningful Test Names
```python
# ✅ GOOD - Clear what's being tested
def test_arduino_responds_to_led_on_command():
    pass

def test_temperature_reading_within_valid_range():
    pass

# ❌ BAD - Unclear purpose
def test1():
    pass

def test_data():
    pass
```

---

## Common Mistakes to Avoid

### Forgetting to Return
```python
# ❌ WRONG - No return statement
def test_something():
    try:
        result = do_test()
        if result:
            True  # This does nothing!
    except Exception:
        False  # This does nothing!

# ✅ CORRECT - Actually return values
def test_something():
    try:
        result = do_test()
        if result:
            return True
        return False
    except Exception:
        return False
```

### Only Logging Success
```python
# ❌ WRONG - Only logs passes
if test_passed:
    results.append({"test": "My Test", "passed": True, "message": "Yay!"})
# Nothing happens if it fails!

# ✅ CORRECT - Log both pass and fail
if test_passed:
    results.append({"test": "My Test", "passed": True, "message": "Success"})
else:
    results.append({"test": "My Test", "passed": False, "message": "Failed"})
```

### Testing Without try/except
```python
# ❌ RISKY - Will crash if serial port fails
def test_connection():
    device = serial.Serial('/dev/ttyUSB0', 9600)
    return True  # Crashes if port doesn't exist!

# ✅ SAFE - Handles errors gracefully
def test_connection():
    try:
        device = serial.Serial('/dev/ttyUSB0', 9600)
        device.close()
        return True
    except Exception:
        return False  # Test fails instead of crashing
```

### Forgetting Newlines in File Writes
```python
# ❌ WRONG - Everything on one line
file.write("Result 1")
file.write("Result 2")
# Output: Result 1Result 2

# ✅ CORRECT - Each on its own line
file.write("Result 1\n")
file.write("Result 2\n")
# Output:
# Result 1
# Result 2
```

---

## New Python Concepts Learned

### try/except Blocks
```python
try:
    risky_code()
except SpecificError:
    handle_specific_error()
except Exception:
    handle_any_error()
```

### Dictionaries for Structured Data
```python
# Create dictionary
data = {
    "key1": "value1",
    "key2": 123,
    "key3": True
}

# Access values
print(data["key1"])  # "value1"

# Used in testing for results
result = {
    "test": "My Test",
    "passed": True,
    "message": "Success"
}
```

### List Comprehensions for Counting
```python
# Count items that match condition
count = sum(1 for item in items if condition)

# Example: Count passed tests
passed = sum(1 for r in results if r["passed"])
```

### datetime Module
```python
import datetime

# Get current date/time
now = datetime.datetime.now()

# Convert to string
timestamp = str(now)
```

### os Module for File Checking
```python
import os

# Check if file exists
if os.path.exists("filename.txt"):
    print("File exists!")
```

---

## Testing Workflow Summary

### Step-by-Step Process
1. **Write test functions** - Each returns True/False
2. **Run each test** - Call the function
3. **Store result** - Append to results list with details
4. **Print summary** - Show pass/fail for each test
5. **Log to file** - Permanent record of test run

### Running Tests Pattern
```python
# Initialize
results = []

# Run test
passed = test_function()

# Store result
if passed:
    results.append({"test": "Test Name", "passed": True, "message": "Success"})
else:
    results.append({"test": "Test Name", "passed": False, "message": "Failure"})

# Report
print_test_summary(results)
log_results_to_file(results, "log.txt")
```

---

## Real-World Applications

### Hardware Testing
- Test sensor readings are valid
- Verify device responses
- Check communication protocols
- Validate calibration

### Software Testing
- Test functions return correct values
- Verify calculations are accurate
- Check error handling works
- Validate data processing

### Integration Testing
- Test components work together
- Verify data flows correctly
- Check system behavior end-to-end
- Validate complete workflows

### Regression Testing
- Run tests after code changes
- Ensure nothing broke
- Catch bugs early
- Maintain code quality

---

## Key Takeaways

1. **Tests should never crash** - Always use try/except
2. **Return boolean values** - True = pass, False = fail
3. **Store results in dictionaries** - Structured, easy to process
4. **Log to files** - Permanent records of test runs
5. **One test, one purpose** - Keep tests focused
6. **Tests are documentation** - Show how system should work
7. **Automate everything** - Run tests frequently
8. **Independent tests** - Each test stands alone
9. **Meaningful names** - Clear what's being tested
10. **Track timestamps** - Know when tests were run

---

## Quick Command Reference

```python
# Error handling
try:
    risky_code()
except Exception:
    handle_error()

# Dictionary access
value = dictionary["key"]

# File operations
with open("file.txt", "a") as f:  # Append mode
    f.write("text\n")

# Check file exists
if os.path.exists("file.txt"):
    pass

# Get timestamp
timestamp = str(datetime.datetime.now())

# Count with condition
count = sum(1 for item in items if condition)
```

---

## Next Steps for Learning

### Beginner Level (What You've Learned)
✅ Basic test functions
✅ try/except error handling
✅ Storing results in dictionaries
✅ Printing test summaries
✅ Logging to files

### Intermediate Level (Next Steps)
- Assert statements (Python's built-in testing)
- unittest module (standard library)
- pytest framework (industry standard)
- Test fixtures (setup/teardown)
- Mocking external dependencies
- Parametrized tests (run same test with different data)

### Advanced Level (Future Topics)
- Test-Driven Development (TDD)
- Continuous Integration (CI)
- Code coverage analysis
- Performance testing
- Load testing
- Integration testing frameworks

---

## Resources for Further Learning

- **Python unittest:** https://docs.python.org/3/library/unittest.html
- **pytest framework:** https://docs.pytest.org/
- **Testing best practices:** Search "Python testing best practices"
- **TDD Tutorial:** Search "Python test-driven development tutorial"

---

## Scripts Created Today

**arduino_test.py** - Complete automated test suite
- Tests Arduino connection
- Tests command/response
- Stores results in dictionaries
- Prints formatted summary
- Logs results to file with timestamps

**arduino_test_log.md** - Test results log file
- Timestamped test runs
- Pass/fail for each test
- Summary statistics
- Historical record of all test runs
