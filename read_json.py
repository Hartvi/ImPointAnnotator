import json

json_dict = dict()
with open("test_annotations.json", "r") as f:
    json_dict = json.load(f)
    print(json_dict)





