import json


def read_json(filename):
    with open(filename) as readfile:
        data = json.load(readfile)
        return data


def write_json(data):
    with open("teams.json", "w") as outfile:
        json.dump(data, outfile, indent=2)
