# Python Basics - Quick Reference

## What is Python?

### Python vs Bash - Key Differences
- **Bash** = Shell program that controls your operating system (command-focused)
  - Like a "remote control" for your computer
  - Best for: Running system commands, file operations, automation of terminal tasks
  
- **Python** = General-purpose programming language (data-focused)
  - Like a "workshop" where you build things
  - Best for: Data processing, building applications, complex calculations, analysis

### Two Modes of Operation
1. **Interactive Mode (REPL)** - Type `python3` in terminal, get `>>>` prompt
   - Execute Python code line by line
   - Great for testing and learning
   - Exit with `exit()` or `Ctrl+D`

2. **Script Mode** - Write `.py` files and execute them
   - Permanent, reusable programs
   - Standard way to write Python programs

---

## Setup & First Script

### Check Python Installation
```bash
which python3                # Show where Python is installed
python3 --version            # Show Python version
```

### Basic Script Structure
```python
#!/usr/bin/python3           # Shebang - full path to interpreter
# This is a comment

print("Hello, World!")       # Your code here
```

### Make Script Executable
```bash
chmod +x script.py           # Add execute permission
./script.py                  # Run the script
```

---

## Variables & Data Types

### Creating Variables
```python
name = "Alice"               # String (text) - needs quotes
age = 25                     # Integer (number) - no quotes
height = 5.8                 # Float (decimal number)
is_student = True            # Boolean (True/False)
```

**Key Rules:**
- Spaces around `=` are OK (unlike Bash!)
- No `$` when reading variables (unlike Bash!)
- Variable names are case-sensitive

### Using Variables
```python
print(name)                  # Print variable (no $ needed)
print(f"Hello {name}")       # f-string for formatting
```

### Data Types Matter!
```python
age = 25                     # Integer
age_str = "25"               # String (looks like number, but it's text!)

# Operations depend on type:
print(25 + 25)               # 50 (addition)
print("25" + "25")           # "2525" (concatenation)
```

### Type Conversion
```python
int("25")                    # Convert string to integer
str(25)                      # Convert integer to string
float("3.14")                # Convert string to float
```

### F-Strings (Formatted Strings)
```python
name = "Alice"
age = 25
print(f"My name is {name} and I'm {age}")    # f-string - interprets {}
print("My name is {name} and I'm {age}")     # Regular string - prints literally
```

---

## Loops

### For Loop - Iterate Over List
```python
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(f"I like {fruit}")     # Note: indentation required!
```

### For Loop - Using Range
```python
# range(stop) - starts at 0, stops before 'stop'
for i in range(5):               # 0, 1, 2, 3, 4
    print(i)

# range(start, stop) - custom start
for i in range(1, 6):            # 1, 2, 3, 4, 5
    print(i)

# range(start, stop, step) - custom increment
for i in range(10, 0, -1):       # 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 (countdown!)
    print(i)
```

---

## Conditionals (If Statements)

### Basic If Statement
```python
if condition:
    # code runs if condition is True
    print("Condition met")
```

### If-Elif-Else
```python
number = 15

if number > 10:
    print("Big number")
elif number == 10:
    print("Perfect ten!")
else:
    print("Small number")
```

### Comparison Operators
- `==` equals (double equals!)
- `!=` not equals
- `>` greater than
- `<` less than
- `>=` greater than or equal
- `<=` less than or equal

### Why Double Equals?
- `=` assigns a value: `x = 5`
- `==` compares values: `x == 5`

### Combining Loops and Conditionals
```python
for number in range(1, 21):
    if number % 2 == 0:          # % is modulo (remainder)
        print(f"{number} is even")
    else:
        print(f"{number} is odd")
```

---

## Functions

### Defining Functions
```python
def function_name():
    # code here (indented!)
    print("Function called")

# Call the function
function_name()
```

### Functions with Parameters
```python
def greet(name):                 # 'name' is a parameter
    print(f"Hello, {name}!")

greet("Alice")                   # "Alice" is an argument
greet("Bob")
```

### Functions that Return Values
```python
def add(a, b):
    return a + b                 # Returns result instead of printing

result = add(5, 3)               # Store returned value
print(f"Sum: {result}")          # Use the result
print(f"Double: {add(5, 3) * 2}")  # Use directly in expressions
```

### Real Example: Temperature Converter
```python
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

temps = [0, 25, 100]
for temp in temps:
    fahrenheit = celsius_to_fahrenheit(temp)
    print(f"{temp}°C is {fahrenheit}°F")
```

---

## File Operations

### Reading Entire File
```python
with open("filename.txt", "r") as file:
    content = file.read()        # Read entire file as one string
    print(content)
# File automatically closes after 'with' block
```

### Reading Line by Line
```python
with open("filename.txt", "r") as file:
    for line in file:
        print(line.strip())      # .strip() removes newline characters
```

### File Modes
- `"r"` - Read mode (default)
- `"w"` - Write mode (overwrites file)
- `"a"` - Append mode (adds to end)

### Handling Newlines
```python
# Each line in file ends with \n
# print() adds another \n by default

# Solution 1: Remove the file's newline
print(line.strip())

# Solution 2: Tell print not to add newline
print(line, end="")
```

### File Paths
- **Relative paths** are relative to where you RUN the script
- `./file.txt` - current directory
- `../file.txt` - parent directory
- `folder/file.txt` - subdirectory

---

## Python's Critical Rule: INDENTATION

### Indentation Defines Code Blocks
```python
# ✓ CORRECT
for i in range(5):
    print(i)              # Indented - inside loop

# ✗ WRONG
for i in range(5):
print(i)                  # IndentationError!
```

### Standard: 4 Spaces or 1 Tab
- Pick one and be consistent
- Everything at same "level" must have same indentation

### Where Indentation Matters
- After `if`, `elif`, `else`
- After `for`, `while`
- After `def` (function definitions)
- After `with` (file handling)

---

## Common Patterns

### Checking if String Contains Text
```python
if "ERROR" in line:           # Check if "ERROR" appears anywhere in line
    print("Found error!")
```

### Counting in Loops
```python
count = 0
for item in items:
    if condition:
        count = count + 1     # Or: count += 1
print(f"Total: {count}")
```

### DRY Principle (Don't Repeat Yourself)
```python
# ✗ BAD - Repetitive
result = convert(0)
print(f"0 is {result}")
result = convert(25)
print(f"25 is {result}")
result = convert(100)
print(f"100 is {result}")

# ✓ GOOD - Use a loop
temps = [0, 25, 100]
for temp in temps:
    result = convert(temp)
    print(f"{temp} is {result}")
```

---

## Bash vs Python Quick Comparison

| Task | Bash | Python |
|------|------|--------|
| **Assign variable** | `NAME="value"` (no spaces!) | `name = "value"` (spaces OK) |
| **Use variable** | `$NAME` or `${NAME}` | `name` (no $) |
| **Print** | `echo "text"` | `print("text")` |
| **Comment** | `# comment` | `# comment` |
| **For loop** | `for i in *; do ... done` | `for i in list: ...` |
| **If statement** | `if [ condition ]; then ... fi` | `if condition: ...` |
| **Code blocks** | `do`/`done`, `{}`/braces | Indentation |
| **String interpolation** | `"Value: $VAR"` | `f"Value: {var}"` |

---

## Common Mistakes to Avoid

### Variable Assignment
```python
name = "Alice"               # ✓ CORRECT
name="Alice"                 # ✓ Also correct (spaces optional)
$name = "Alice"              # ✗ WRONG - no $ when assigning
```

### Comparison vs Assignment
```python
if x == 5:                   # ✓ CORRECT - comparison (double =)
if x = 5:                    # ✗ WRONG - assignment (single =)
```

### Indentation
```python
# ✓ CORRECT
if True:
    print("yes")

# ✗ WRONG - no indentation
if True:
print("yes")
```

### Forgetting Colons
```python
if condition:                # ✓ CORRECT - colon required
if condition                 # ✗ WRONG - missing colon
```

### String vs Number
```python
age = 25                     # Number
age = "25"                   # String (can't do math with it!)

# Convert when needed:
int("25") + 5                # 30
"25" + str(5)                # "255"
```

---

## Useful Built-in Functions

```python
print(value)                 # Display output
len(list)                    # Length of list/string
type(variable)               # Show variable's data type
range(start, stop, step)     # Generate number sequence
int(value)                   # Convert to integer
str(value)                   # Convert to string
float(value)                 # Convert to float
```

---

## Getting Help

```bash
python3 --help               # Python command help
python3                      # Start interactive mode to test code
```

```python
help(function_name)          # Inside Python - get help on function
type(variable)               # Check what type a variable is
```

---

## Scripts Created Today

1. **hello.py** - Basic print statement
2. **variables.py** - Variable assignment and types
3. **loops.py** - Iterating over lists
4. **countdown.py** - Using range() for countdown
5. **number_checker.py** - If/elif/else conditionals
6. **even_odd.py** - Combining loops and conditionals
7. **greet.py** - Basic function definition
8. **calculator.py** - Functions with return values
9. **temp_converter.py** - Practical function with loop
10. **file_reader.py** - Reading files line by line
11. **log_analyzer.py** - Real-world file processing (counting errors)

---

## Next Steps for Learning

### Topics to Explore
- Lists, tuples, and dictionaries (data structures)
- While loops
- String methods (`.split()`, `.replace()`, `.lower()`, etc.)
- Exception handling (try/except)
- Reading command-line arguments (`sys.argv`)
- Writing to files
- Working with modules and imports
- Classes and object-oriented programming

### Practice Ideas
- File organizer (sort files by extension)
- CSV data processor
- Password generator
- Todo list manager
- Web scraper (with requests library)
- Data visualization (with matplotlib)

---

## Key Takeaways

1. **Python is data-focused** - excels at processing information, not running system commands
2. **Indentation is syntax** - unlike Bash where it's just style
3. **Variables don't need $** - simpler than Bash
4. **F-strings are powerful** - `f"Value: {variable}"` for formatting
5. **Functions return values** - use `return` to give back results
6. **Files need context managers** - use `with open()` for safety
7. **Everything is an object** - strings, numbers, lists all have methods
8. **Python is explicit** - `"ERROR" in line` not `line == "ERROR"`

---

## Resources

- **Official Python Tutorial:** https://docs.python.org/3/tutorial/
- **Python Documentation:** https://docs.python.org/3/
- **Interactive Practice:** https://www.learnpython.org/
- **Style Guide (PEP 8):** https://pep8.org/
