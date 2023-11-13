import os
import time
import yaml

# Define the file path you want to monitor
file_path = "personinfo.yaml"

# Get the initial modification timestamp of the file
initial_timestamp = os.path.getmtime(file_path)

def is_yaml_file_corrupted(file_path):
    try:
        with open(file_path, 'r') as yaml_file:
            yaml.safe_load(yaml_file)
        print(f"The YAML file at {file_path} is not corrupted.")
        print('')
        return False  # Parsing successful, file is not corrupted
    except yaml.YAMLError as e:
        print(f"The YAML file at {file_path} is corrupted.")
        print(f"YAML parsing error: {str(e)}")
        print('')
        return True  # Parsing failed, file is corrupted

try:
    print(f"Monitoring changes to {file_path}. Press Ctrl+C to stop.")
    while True:
        current_timestamp = os.path.getmtime(file_path)
        
        if current_timestamp != initial_timestamp:
            print(f"File {file_path} has been modified!")
            initial_timestamp = current_timestamp
            is_yaml_file_corrupted(file_path)
        
        time.sleep(1)  # Poll every 1 second (adjust as needed)
except KeyboardInterrupt:
    pass
