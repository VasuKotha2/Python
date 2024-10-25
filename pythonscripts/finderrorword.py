# Python script to find lines with the word "error" in a file
file_name = "errors.txt"
try:
# Open the file in read mode
    with open('/Users/vasukotha/Desktop/Devops/python/Python/pythonscripts/errors.txt', 'r') as file:
    # Read the file line by line
        for line in file:
        # Check if the word "error" (case-insensitive) is in the line
            if 'error' in line.lower():
            # Print the line containing the word "error"
                print(line.strip())
except FileNotFoundError:
    print(f"Error: The file {file_name} is not found")
