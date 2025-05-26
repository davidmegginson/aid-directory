import json, os.path

with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as input:
    CONFIG = json.load(input)
