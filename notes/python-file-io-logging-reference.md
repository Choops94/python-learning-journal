# Python File I/O & Data Logging - Quick Reference

## What We Built Today
Created a **continuous data logger** that records timestamped temperature and humidity readings to CSV files - ready for future data analysis and plotting.

---

## CSV Files

### What is CSV?
- **CSV** = Comma Separated Values
- Simple text format for tabular data (rows and columns)
- Each line is a row, commas separate columns
- First row typically contains column headers

### Example CSV Structure
```
timestamp,temperature_c,humidity_percent
2025-01-14 10:30:00,22.5,65.0
2025-01-14 11:00:00,23.1,62.5
```

### When to Use CSV
- ✅ Time-series data (measurements over time)
- ✅ Tabular/spreadsheet-like data
- ✅ Easy to append new rows
- ✅ Simple to read by humans and programs
- ✅ Perfect for data analysis and plotting

---

## Python's csv Module

### Import the Module
```python
import csv
```

### Writing to CSV Files

#### Basic Pattern - Single Entry
```python
import csv

with open("data.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["header1", "header2"])      # Write headers
    writer.writerow(["value1", "value2"])        # Write data
```

#### Appending Data (Adding Rows)
```python
with open("data.csv", "a") as file:              # "a" = append mode
    writer = csv.writer(file)
    writer.writerow([timestamp, temp, humidity])
```

### Key Functions
- `csv.writer(file)` - Creates a writer object
- `writer.writerow([item1, item2, ...])` - Write single row (list of values)
- `writer.writerows([[row1], [row2], ...])` - Write multiple rows at once

---

## File Modes

### The Three Essential Modes
```python
"r"  # Read mode (default) - file must exist
"w"  # Write mode - OVERWRITES entire file (like > in bash)
"a"  # Append mode - adds to end of file (like >> in bash)
```

### Choosing the Right Mode
- **First time creating file with headers?** Use `"w"`
- **Adding new data entries?** Use `"a"`
- **Reading data back?** Use `"r"`

---

## Working with Dates and Times

### The datetime Module
```python
import datetime

# Get current date and time
now = datetime.datetime.now()

# Convert to string for storage
timestamp = str(datetime.datetime.now())
# Output: "2025-01-14 10:30:45.123456"
```

### Why Store as String?
- CSV files store text, not Python objects
- Strings are human-readable
- Easy to parse back into datetime objects later for analysis

---

## Checking if Files Exist

### The os Module
```python
import os

if os.path.exists("filename.csv"):
    # File exists - do something
    pass
else:
    # File doesn't exist - create it
    # Write headers here
```

### Common Pattern - Initialize CSV with Headers
```python
import os
import csv

if not os.path.exists("data.csv"):
    with open("data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "temperature_c"])
```

**Why?** Only write headers once when file is created, then all future runs just append data.

---

## Getting User Input

### The input() Function
```python
user_input = input("Prompt message: ")
# Function displays prompt, waits for user to type and press Enter
# Returns what user typed as a STRING
```

### Type Conversion for Numbers
```python
# input() always returns a string!
temp_string = input("Enter temperature: ")  # User types "23.5"
temp_float = float(temp_string)             # Convert to number: 23.5

# Or combine in one line:
temp = float(input("Enter temperature: "))
```

### Important Conversions
- `int("25")` → `25` (integer, whole numbers only)
- `float("25.5")` → `25.5` (float, handles decimals)
- `str(25)` → `"25"` (convert number to string)

---

## Continuous Logging with Loops

### While Loop Pattern
```python
while True:                          # Infinite loop
    # Get user input
    data = input("Enter data (or 'quit'): ")
    
    # Check for exit condition
    if data == "quit":
        break                        # Exit the loop
    
    # Process and log data
    log_data(data)
```

### Best Practice - Check After Each Input
```python
while True:
    temp = input("Temperature: ")
    if temp == "quit":
        break
    
    humidity = input("Humidity: ")
    if humidity == "quit":
        break
    
    # Only reaches here if neither was "quit"
    log_reading(float(temp), float(humidity))
```

---

## Complete Data Logger Pattern

### Full Working Example
```python
#!/usr/bin/python3
import csv
import datetime
import os

# Initialize file with headers if it doesn't exist
if not os.path.exists("weather_log.csv"):
    with open("weather_log.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "temperature_c", "humidity_percent"])

# Function to log a reading
def log_reading(temp, humidity):
    with open("weather_log.csv", "a") as file:
        writer = csv.writer(file)
        timestamp = str(datetime.datetime.now())
        writer.writerow([timestamp, temp, humidity])
        print("Data logged successfully!")

# Continuous logging loop
while True:
    temp = input("Enter temperature (or 'quit'): ")
    if temp == "quit":
        break
    
    humidity = input("Enter humidity: ")
    if humidity == "quit":
        break
    
    log_reading(float(temp), float(humidity))

print("Logging session ended.")
```

---

## JSON vs CSV

### JSON (JavaScript Object Notation)
```json
{
  "timestamp": "2025-01-14 10:30:00",
  "temperature_c": 22.5,
  "location": "living_room",
  "sensor": {
    "id": "temp_01",
    "status": "active"
  }
}
```

**Best for:**
- Nested/hierarchical data
- Configuration files
- API responses
- Complex structured data

### CSV
```csv
timestamp,temperature_c,location
2025-01-14 10:30:00,22.5,living_room
2025-01-14 11:00:00,23.1,living_room
```

**Best for:**
- Time-series data (our use case!)
- Tabular data (rows and columns)
- Easy appending of new entries
- Spreadsheet-compatible data
- Simple data analysis and plotting

**Rule of thumb:** If you're logging measurements over time → CSV. If you have complex nested structures → JSON.

---

## Common Patterns

### Check Then Append Pattern
```python
# Only write headers if file is new
if not os.path.exists("data.csv"):
    with open("data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["header1", "header2"])

# Always append data
with open("data.csv", "a") as file:
    writer = csv.writer(file)
    writer.writerow([value1, value2])
```

### Safe User Input Pattern
```python
while True:
    user_input = input("Enter value: ")
    
    # Always check for exit before conversion
    if user_input == "quit":
        break
    
    # Convert to appropriate type
    try:
        value = float(user_input)
        process_value(value)
    except ValueError:
        print("Invalid number, try again")
```

---

## Best Practices

### Column Naming
```python
# ✅ GOOD - no spaces, descriptive, lowercase with underscores
["timestamp", "temperature_c", "humidity_percent"]

# ❌ AVOID - spaces and special characters make programming harder
["Time (dd/mm/yyyy)", "Temperature °C", "Humidity %"]
```

### Data Types in CSV
- Store numbers as actual numbers (floats/ints), not strings
- This makes future analysis and plotting much easier
- Convert user input: `float(input("Value: "))`

### File Organization
```python
# ✅ GOOD - descriptive filename
"weather_log.csv"

# ❌ AVOID - vague names
"data.csv"
"output.csv"
```

### Function Design
```python
# ✅ GOOD - clear purpose, reusable
def log_reading(temp, humidity):
    # logs one reading with timestamp

# ❌ AVOID - doing everything in main code
# Hard to reuse, test, or modify
```

---

## Common Mistakes to Avoid

### File Mode Confusion
```python
# ❌ WRONG - overwrites file every time
with open("data.csv", "w") as file:
    writer.writerow([new_data])

# ✅ CORRECT - appends to existing file
with open("data.csv", "a") as file:
    writer.writerow([new_data])
```

### Forgetting Type Conversion
```python
temp = input("Temperature: ")    # Returns string "23.5"
log_reading(temp, humidity)      # Stores string, not number!

# ✅ CORRECT
temp = float(input("Temperature: "))
```

### Checking Quit After Conversion
```python
# ❌ WRONG - crashes if user types "quit"
value = float(input("Enter number: "))
if value == "quit":    # Never reaches here, already crashed!
    break

# ✅ CORRECT - check before conversion
value = input("Enter number: ")
if value == "quit":
    break
value = float(value)
```

### Writing Headers Multiple Times
```python
# ❌ WRONG - adds headers every time script runs
with open("data.csv", "a") as file:
    writer.writerow(["timestamp", "value"])  # Oops!
    writer.writerow([timestamp, value])

# ✅ CORRECT - only write headers once when file created
if not os.path.exists("data.csv"):
    with open("data.csv", "w") as file:
        writer.writerow(["timestamp", "value"])
```

---

## Modules Used Today

### Quick Import Reference
```python
import csv                    # CSV file reading/writing
import datetime               # Date and time handling
import os                     # File system operations
```

### Key Functions
```python
# csv module
csv.writer(file)             # Create CSV writer
writer.writerow([values])    # Write single row

# datetime module
datetime.datetime.now()      # Current date/time
str(datetime_obj)            # Convert to string

# os module
os.path.exists(filename)     # Check if file exists

# Built-in functions
input(prompt)                # Get user input (returns string)
float(string)                # Convert string to decimal number
int(string)                  # Convert string to whole number
str(value)                   # Convert to string
```

---

## Workflow Summary

### Creating a Data Logger
1. **Import modules** (`csv`, `datetime`, `os`)
2. **Check if file exists** - create with headers if needed
3. **Define logging function** - accepts data, appends to CSV
4. **Get user input** - with type conversion
5. **Call logging function** - pass converted values
6. **Optional: Add loop** - for continuous logging

---

## Next Steps

### Future Lessons Will Cover
- **Reading CSV data back** into Python
- **Data analysis** - calculating averages, finding trends
- **Plotting data** - visualizing temperature/humidity over time
- **Data cleaning** - handling missing or invalid entries
- **Advanced CSV features** - different delimiters, quoting

### Your CSV Files Are Now Ready For
- ✅ Plotting with matplotlib
- ✅ Statistical analysis
- ✅ Importing into spreadsheets
- ✅ Machine learning projects
- ✅ Data science workflows

---

## Troubleshooting

### "FileNotFoundError"
- File doesn't exist and you used `"r"` mode
- **Solution:** Use `"a"` or `"w"` mode, or check with `os.path.exists()`

### "ValueError: could not convert string to float"
- Trying to convert non-numeric string (like "quit") to number
- **Solution:** Check for special strings BEFORE conversion

### Headers appearing multiple times
- Writing headers inside append loop
- **Solution:** Only write headers once when file is created

### Data appearing as strings in CSV
- Not converting `input()` result to float/int
- **Solution:** Use `float(input("..."))` for numbers

---

## Quick Command Reference

```bash
# View CSV file
cat filename.csv

# Count lines in CSV (including header)
wc -l filename.csv

# View last 10 entries
tail -10 filename.csv

# Search for specific values
grep "23.5" filename.csv
```

---

## Key Takeaways

1. **CSV is perfect for time-series data** - easy to append, analyze, and plot
2. **Use "a" mode for logging** - "w" overwrites, "a" appends
3. **Check file existence** - write headers only for new files
4. **Store numbers as floats** - not strings (easier for analysis)
5. **Check for "quit" BEFORE conversion** - avoid crashes
6. **datetime.datetime.now()** - automatic timestamps
7. **Functions make code reusable** - log_reading() can be called many times
8. **input() returns strings** - always convert for numbers

---

## Resources for Further Learning

- **Python csv documentation:** https://docs.python.org/3/library/csv.html
- **datetime documentation:** https://docs.python.org/3/library/datetime.html
- **os.path documentation:** https://docs.python.org/3/library/os.path.html
- **File I/O tutorial:** https://docs.python.org/3/tutorial/inputoutput.html
