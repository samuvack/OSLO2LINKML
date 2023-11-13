import yaml

def is_yaml_file_corrupted(file_path):
    try:
        with open(file_path, 'r') as yaml_file:
            yaml.safe_load(yaml_file)
        return False  # Parsing successful, file is not corrupted
    except yaml.YAMLError as e:
        print(f"YAML parsing error: {str(e)}")
        return True  # Parsing failed, file is corrupted

# Replace 'path/to/your/file.yaml' with the actual file path you want to check
file_path = 'personinfo.yaml'

if is_yaml_file_corrupted(file_path):
    print(f"The YAML file at {file_path} is corrupted.")
else:
    print(f"The YAML file at {file_path} is not corrupted.")
