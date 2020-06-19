import json

configfile = "config/config.json"
stringsFile = "config/strings.json"

jsonConfig = json.loads(open(configfile, "r").read())
jsonStrings = json.loads(open(stringsFile, "r").read())


def get_config(key):
    return jsonConfig[key]


def get_string(key):
    return jsonStrings[key]
