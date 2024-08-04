import os, json
import pandas as pd


path_to_json = 'test_files/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
print(json_files)