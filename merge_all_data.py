import json

# List of file names to load
file_names = [
    'atm_use_me.json',
    'missouri_use_me.json',
    'OSU_use_me.json',
    'KSU_use_me.json',
    'wisonsin_use_me.json',

]

# Initialize an empty list to hold all the data
merged_data = []

# Loop through each file name
for file_name in file_names:
    try:
        with open(file_name, 'r') as f:
            data = json.load(f) # Load data
            if isinstance(data, list): # Check if it's a list
               merged_data.extend(data) # Extend the merged list by individual json objects
            elif isinstance(data, dict): # If the data is a single dict, append to the list
                merged_data.append(data)
            else:
                print(f"Warning: Unexpected data structure in {file_name}. Skipping.")
    except FileNotFoundError:
        print(f"Error: File {file_name} not found. Skipping.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON in {file_name}. Skipping.")


# Save the merged data to a new JSON file
with open('merged_extension_data.json', 'w') as outfile:
    json.dump(merged_data, outfile, indent=4)  # Use indent for readability

print("Merged data saved to merged_texas_bills.json")

print(len(merged_data))