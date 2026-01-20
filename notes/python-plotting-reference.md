# Python Data Plotting & Analysis - Quick Reference

## What We Built Today
Created a complete data visualization and analysis script that reads CSV files, calculates statistics, and generates multiple plot types using matplotlib.

---

## Reading CSV Files

### Basic Reading Pattern
```python
import csv

with open("filename.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)  # Each row is a list: ['value1', 'value2', 'value3']
```

### Skipping Header Row
```python
with open("filename.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        # Process data rows only
        print(row)
```

**Why skip headers?** First row contains column names, not actual data values.

### Accessing Values in a Row
```python
row = ['2025-01-14 10:30:00', '22.5', '65.0']

timestamp = row[0]    # First column (index 0)
temp = row[1]         # Second column (index 1)
humidity = row[2]     # Third column (index 2)
```

**Remember:** Zero-based indexing! First item is `[0]`, not `[1]`

### Important: CSV Values Are Strings!
```python
# When reading from CSV, ALL values are strings
temp_string = row[1]        # "22.5" (string)
temp_float = float(row[1])  # 22.5 (number)

# Always convert for numerical operations
temperatures.append(float(row[1]))
```

---

## Building Lists from CSV Data

### The Pattern
```python
import csv

# Create empty lists
timestamps = []
temperatures = []
humidity = []

# Read and populate lists
with open("weather_log.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    
    for row in reader:
        timestamps.append(row[0])           # String timestamp
        temperatures.append(float(row[1]))  # Convert to number
        humidity.append(float(row[2]))      # Convert to number

print(f"Loaded {len(temperatures)} data points")
```

**Key concept:** Build parallel lists - same index in each list represents one complete data point.

---

## Matplotlib Basics

### Import Convention
```python
import matplotlib.pyplot as plt
```

**Why `as plt`?** Standard abbreviation - makes code shorter and more readable.

### Simple Line Plot
```python
# Basic plot
plt.plot(x_values, y_values)
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.title('Plot Title')
plt.show()  # Display the plot
```

### Using Indices Instead of Timestamps
```python
# When timestamps are messy strings, use indices
plt.plot(range(len(temperatures)), temperatures)
plt.xlabel('Reading Number')
plt.ylabel('Temperature (°C)')
```

**What is `range(len(temperatures))`?**
- `len(temperatures)` = number of data points (e.g., 10)
- `range(10)` = generates 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
- Perfect for X-axis when you just want sequential numbering

---

## Creating Subplots

### Why Subplots?
Multiple separate graphs in one figure instead of overlapping lines on a single plot.

### Basic Subplot Pattern
```python
# Create figure with custom size
plt.figure(figsize=(10, 8))  # (width, height) in inches

# First subplot
plt.subplot(2, 1, 1)  # (rows, columns, position)
plt.plot(x1, y1)
plt.ylabel('Y Label')
plt.title('First Plot')

# Second subplot
plt.subplot(2, 1, 2)
plt.plot(x2, y2)
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.title('Second Plot')

plt.tight_layout()  # Prevent labels from overlapping
plt.show()
```

### Understanding plt.subplot(rows, cols, position)
```python
plt.subplot(3, 1, 1)  # 3 rows, 1 column, position 1 (top)
plt.subplot(3, 1, 2)  # 3 rows, 1 column, position 2 (middle)
plt.subplot(3, 1, 3)  # 3 rows, 1 column, position 3 (bottom)
```

**Pattern:** Create a grid, then specify which cell to draw in.

---

## Scatter Plots

### When to Use Scatter Plots
- Show relationship between two variables
- Look for correlations or patterns
- Each point represents one observation

### Creating Scatter Plots
```python
plt.scatter(x_values, y_values)
plt.xlabel('Variable 1')
plt.ylabel('Variable 2')
plt.title('Relationship Between Variables')
plt.show()
```

### Example: Temperature vs Humidity
```python
plt.subplot(3, 1, 3)
plt.scatter(temperatures, humidity)
plt.xlabel('Temperature (°C)')
plt.ylabel('Humidity (%)')
plt.title('Temperature vs Humidity Relationship')
```

**Look for:** Trends, clusters, outliers, correlation (positive/negative/none)

---

## Adding Reference Lines

### Horizontal Line (e.g., for averages)
```python
avg_temp = sum(temperatures) / len(temperatures)

plt.plot(range(len(temperatures)), temperatures)
plt.axhline(y=avg_temp, color='r', linestyle='--', label='Average')
plt.legend()  # Show the label
```

### Line Styling Options
- `color='r'` - Red (also: 'b'=blue, 'g'=green, 'k'=black)
- `linestyle='--'` - Dashed (also: '-'=solid, ':'=dotted, '-.'=dash-dot)
- `label='text'` - Label for legend

### Vertical Line
```python
plt.axvline(x=value, color='g', linestyle=':')
```

---

## Basic Statistical Analysis

### Built-in Functions
```python
# Sum all values
total = sum(temperatures)

# Count values
count = len(temperatures)

# Calculate average
average = sum(temperatures) / len(temperatures)

# Find maximum
max_value = max(temperatures)

# Find minimum
min_value = min(temperatures)
```

### Example: Complete Statistics
```python
# Calculate statistics
avg_temp = sum(temperatures) / len(temperatures)
max_temp = max(temperatures)
min_temp = min(temperatures)

# Display with formatting
print(f"Average temperature: {avg_temp:.1f}°C")
print(f"Max temperature: {max_temp:.1f}°C")
print(f"Min temperature: {min_temp:.1f}°C")
```

**Format string `:.1f`** means 1 decimal place for floats.

---

## Complete Example Script

### Full Data Analysis & Plotting Script
```python
#!/usr/bin/python3
import csv
import matplotlib.pyplot as plt

# Initialize lists
timestamps = []
temperatures = []
humidity = []

# Read CSV file
with open("weather_log.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    
    for row in reader:
        timestamps.append(row[0])
        temperatures.append(float(row[1]))
        humidity.append(float(row[2]))

# Calculate statistics
avg_temp = sum(temperatures) / len(temperatures)
avg_hum = sum(humidity) / len(humidity)
max_temp = max(temperatures)
min_temp = min(temperatures)

# Display statistics
print(f"Data points: {len(temperatures)}")
print(f"Temperature: {min_temp:.1f}°C to {max_temp:.1f}°C (avg: {avg_temp:.1f}°C)")
print(f"Humidity: avg {avg_hum:.1f}%")

# Create plots
plt.figure(figsize=(10, 8))

# Temperature over time
plt.subplot(3, 1, 1)
plt.plot(range(len(temperatures)), temperatures)
plt.axhline(y=avg_temp, color='r', linestyle='--', label='Average')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Over Time')
plt.legend()

# Humidity over time
plt.subplot(3, 1, 2)
plt.plot(range(len(humidity)), humidity)
plt.axhline(y=avg_hum, color='r', linestyle='--', label='Average')
plt.xlabel('Reading Number')
plt.ylabel('Humidity (%)')
plt.title('Humidity Over Time')
plt.legend()

# Scatter plot
plt.subplot(3, 1, 3)
plt.scatter(temperatures, humidity)
plt.xlabel('Temperature (°C)')
plt.ylabel('Humidity (%)')
plt.title('Temperature vs Humidity Relationship')

plt.tight_layout()
plt.show()
```

---

## Common Plot Types Quick Reference

### Line Plot
```python
plt.plot(x, y)
```
**Use for:** Time-series data, trends over time

### Scatter Plot
```python
plt.scatter(x, y)
```
**Use for:** Correlations, relationships between variables

### Bar Chart
```python
plt.bar(categories, values)
```
**Use for:** Comparing categories

### Histogram
```python
plt.hist(data, bins=20)
```
**Use for:** Distribution of a single variable

---

## Customization Options

### Figure Size
```python
plt.figure(figsize=(width, height))  # In inches
plt.figure(figsize=(10, 6))          # Wide plot
plt.figure(figsize=(8, 10))          # Tall plot
```

### Colors
- Single letter codes: 'r', 'g', 'b', 'c', 'm', 'y', 'k', 'w'
- Full names: 'red', 'green', 'blue', etc.
- Hex codes: '#FF5733'

### Line Styles
- `'-'` - Solid line (default)
- `'--'` - Dashed line
- `':'` - Dotted line
- `'-.'` - Dash-dot line

### Markers (for plot points)
```python
plt.plot(x, y, marker='o')  # Circles
plt.plot(x, y, marker='s')  # Squares
plt.plot(x, y, marker='^')  # Triangles
```

### Grid
```python
plt.grid(True)  # Add gridlines
plt.grid(True, linestyle=':', alpha=0.5)  # Subtle dotted grid
```

---

## Common Patterns

### Multiple Lines on One Plot
```python
plt.plot(x, y1, label='Dataset 1')
plt.plot(x, y2, label='Dataset 2')
plt.legend()
```

### Saving Plots to File
```python
plt.savefig('plot.png')      # Save as PNG
plt.savefig('plot.pdf')      # Save as PDF
plt.savefig('plot.png', dpi=300)  # High resolution
```

### Combining Statistics and Plotting
```python
# Calculate
avg = sum(data) / len(data)
std_dev = ...  # (Future lesson: statistics module)

# Plot with annotations
plt.plot(data)
plt.axhline(y=avg, label=f'Avg: {avg:.1f}')
plt.title(f'Data (n={len(data)})')
```

---

## Troubleshooting

### "TypeError: list indices must be integers, not str"
- **Problem:** Trying to access row columns with strings
- **Solution:** Use numeric indices: `row[0]`, `row[1]`, not `row['timestamp']`

### "ValueError: could not convert string to float"
- **Problem:** Trying to convert non-numeric string
- **Solution:** Check your CSV data, ensure correct column index

### Plot doesn't appear
- **Problem:** Forgot `plt.show()`
- **Solution:** Always end with `plt.show()` to display plot

### X-axis labels overlapping/messy
- **Problem:** Too many timestamp strings
- **Solution:** Use `range(len(data))` instead, or rotate labels:
  ```python
  plt.xticks(rotation=45)
  ```

### "NameError: name 'plt' is not defined"
- **Problem:** Forgot to import matplotlib
- **Solution:** Add `import matplotlib.pyplot as plt` at top

---

## Best Practices

### Script Organization
```python
# 1. Imports at top
import csv
import matplotlib.pyplot as plt

# 2. Initialize data structures
data_lists = []

# 3. Read/load data
# ... reading code ...

# 4. Calculate statistics
# ... calculations ...

# 5. Create visualizations
# ... plotting code ...

# 6. Display/save
plt.show()
```

### Descriptive Variable Names
```python
# ✅ GOOD
temperatures = []
avg_temp = sum(temperatures) / len(temperatures)

# ❌ BAD
t = []
a = sum(t) / len(t)
```

### Comments for Clarity
```python
# Calculate average temperature
avg_temp = sum(temperatures) / len(temperatures)

# Create subplot for temperature time-series
plt.subplot(2, 1, 1)
```

### Consistent Formatting
```python
# Use f-strings with consistent decimal places
print(f"Average: {avg:.1f}°C")
print(f"Maximum: {max_val:.1f}°C")
print(f"Minimum: {min_val:.1f}°C")
```

---

## Python vs Bash - Data Analysis

| Task | Bash | Python |
|------|------|--------|
| **Read CSV** | `cat file.csv` | `csv.reader()` with loop |
| **Count lines** | `wc -l file.csv` | `len(data_list)` |
| **Find max** | `sort -n \| tail -1` | `max(data_list)` |
| **Calculate average** | Complex awk/bc | `sum(list) / len(list)` |
| **Plot data** | External tools | `matplotlib` built-in |

**Takeaway:** Python excels at data analysis; Bash excels at file/system operations.

---

## What We Learned Today

### Skills Demonstrated
✓ Read CSV files with `csv.reader()`
✓ Skip header rows with `next()`
✓ Build lists from CSV data
✓ Convert strings to floats for analysis
✓ Calculate basic statistics (sum, average, max, min)
✓ Create line plots with matplotlib
✓ Create scatter plots
✓ Use subplots for multiple graphs
✓ Add reference lines (average markers)
✓ Customize plots with labels, titles, legends

### Commands & Functions Mastered
- `csv.reader(file)`
- `next(reader)`
- `float(value)`
- `sum(list)`, `len(list)`, `max(list)`, `min(list)`
- `plt.figure(figsize=(w, h))`
- `plt.subplot(rows, cols, pos)`
- `plt.plot(x, y)`
- `plt.scatter(x, y)`
- `plt.axhline(y=value)`
- `plt.xlabel()`, `plt.ylabel()`, `plt.title()`
- `plt.legend()`
- `plt.tight_layout()`
- `plt.show()`

---

## Next Steps (Future Lessons)

### Statistics Module
```python
import statistics

mean = statistics.mean(data)
median = statistics.median(data)
stdev = statistics.stdev(data)
```

### DateTime Objects for Real Timestamps
```python
import datetime

# Convert string to datetime object
timestamp = datetime.datetime.strptime('2025-01-14 10:30:00', '%Y-%m-%d %H:%M:%S')

# Better X-axis formatting with real dates
```

### Real Sensor Data
- Reading system temperature with `psutil`
- Reading from actual sensors
- Live data streaming and plotting

### Advanced Plotting
- Multiple Y-axes on same plot
- Subplots with different layouts (2x2 grids)
- 3D plots
- Interactive plots with `plotly`
- Heatmaps and contour plots

### Data Analysis Libraries
- **pandas** - Powerful data manipulation (industry standard)
- **numpy** - Numerical computing (faster than lists)
- **scipy** - Scientific computing, advanced statistics
- **seaborn** - Statistical visualization (builds on matplotlib)

---

## Resources

- **Matplotlib Documentation:** https://matplotlib.org/stable/contents.html
- **Matplotlib Gallery:** https://matplotlib.org/stable/gallery/index.html (great for examples!)
- **Python CSV Module:** https://docs.python.org/3/library/csv.html
- **Statistics Module:** https://docs.python.org/3/library/statistics.html

---

## Quick Command Reference Card

```python
# Reading CSV
import csv
with open("file.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        value = float(row[1])

# Basic stats
avg = sum(data) / len(data)
maximum = max(data)
minimum = min(data)

# Basic plot
import matplotlib.pyplot as plt
plt.plot(x, y)
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.title('Title')
plt.show()

# Subplots
plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(x1, y1)
plt.subplot(2, 1, 2)
plt.scatter(x2, y2)
plt.tight_layout()
plt.show()
```

---

## Key Takeaways

1. **CSV values are always strings** - convert with `float()` or `int()`
2. **Skip headers with `next(reader)`** - prevents treating headers as data
3. **Build parallel lists** - same index = same data point
4. **range(len(list))** - quick way to create sequential X-axis values
5. **Subplots for multiple graphs** - `plt.subplot(rows, cols, position)`
6. **Line plots for time-series** - show trends over time
7. **Scatter plots for relationships** - reveal correlations
8. **Always end with `plt.show()`** - displays the plot
9. **Use `plt.tight_layout()`** - prevents label overlap
10. **F-strings with `:.1f`** - format numbers to 1 decimal place
