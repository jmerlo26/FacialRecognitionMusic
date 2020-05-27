import json
with open("config.json") as config:
	data = json.load(config)

print(data['DisableOverride'])