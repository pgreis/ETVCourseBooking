
def read_json_file(file_path):
    import json
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def read_yaml_file(file_path):
    import yaml
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data

