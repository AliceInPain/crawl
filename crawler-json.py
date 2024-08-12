import json
from pprint import pprint
from crawler3 import data


with open("data.json", 'w', encoding="utf-8") as file:
    json.dump(data, file)
