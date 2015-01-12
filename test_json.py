import json

json_file = open('class-sample.json')
json_str = json_file.read()
json_data = json.loads(json_str)

for key in json_data.keys():
   print "key: %s , value: %s" % (key, json_data[key])