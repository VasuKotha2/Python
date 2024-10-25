import json

def remove_duplicates_from_json(input_file, output_file):
    # Read data from the input JSON file
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    # Function to remove duplicates from a list while preserving order
    def remove_duplicates(lst):
        seen = set()
        result = []
        for item in lst:
            # Convert dictionaries to tuples of sorted key-value pairs to handle unhashable types
            if isinstance(item, dict):
                item_tuple = tuple(sorted(item.items()))
            else:
                item_tuple = item
            
            if item_tuple not in seen:
                seen.add(item_tuple)
                result.append(item)
        return result

    # If the data is a list, remove duplicates from it
    if isinstance(data, list):
        data = remove_duplicates(data)
    # If the data is a dictionary, process each list value in it
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                data[key] = remove_duplicates(value)

    # Write the cleaned data to the output JSON file
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
input_file = 'Python/Basics/keywords/input.json'
output_file = 'output.json'
remove_duplicates_from_json(input_file, output_file)
