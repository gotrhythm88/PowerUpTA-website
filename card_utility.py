import json
import re
import sys
import argparse
import os

def process_json(json_str):
	"""
	Process JSON data to remove any improper white space (tabs, newlines, multiple spaces)
	Replace these with a single space
	"""
	json_str = json_str.replace("\n", " ")
	json_str = json_str.replace("\t", " ")
	
	while json_str.find("  ") > -1:
		json_str = json_str.replace("  ", " ")
	
	return json_str

def replace_params(template, data):
	"""
	Match json strings found in data dictionary to parameters in template
	Replace the parameters and return new text
	"""
	# Find all variables between curly braces, potentially with some spaces
	matches = re.findall("({{\s*)(\w+(-\w+)*)(\s*}})", template)
	# Process the matches
	for match in matches:
		key = match[1]
		if key in data:
			template = template.replace(match[0] + match[1] + match[3], data[key])
		# If no data supplied in dictionary, that was an optional parameter, just delete it
		else:
			template = template.replace(match[0] + match[1] + match[3], "")
	return template

def generate_card(template, data):
	"""
	Matches json data found in data to parameters in template
	Recursively fills in for loops
	"""
	# Look for a loop
	loop_start = re.search("\t*{{( *)for (\w+) in (\w+)( *)}}\n", template)
	# If we found a loop, process it
	if loop_start:
		# Find the end of the for loop
		loop_start_begin = loop_start.start()
		loop_start_end = loop_start.end()
		loop_close = re.search("\t*{{( *)endfor( *)}}\n", template[loop_start_end:])

		loop_close_begin = loop_start_end
		loop_close_end = loop_start_end

		# Find the end of the outermost for loop
		while loop_close:
			loop_close_begin = loop_close_end + loop_close.start()
			loop_close_end += loop_close.end()
			loop_close = re.search("\t*{{( *)endfor( *)}}\n", template[loop_close_end:])

		# Split up the template
		beginning = template[:loop_start_begin]
		middle = template[loop_start_end:loop_close_begin]
		end = template[loop_close_end:]

		# Recursively process the middle and concatenate to the beginning
		# Pull out the data for the loop from the dictionary
		key = loop_start.group(3)
		dict_ = data[key]
		for element in dict_:
			beginning += generate_card(middle, element)

		# Add back on the end
		template = beginning + end

	# Process any remaining simple replacements
	template = replace_params(template, data)

	return template

def main():
	# Get the templates
	try:
		with open("templates/template.html", 'r') as f:
			html_template = f.read()
		with open("templates/template.js", 'r') as f:
			js_template = f.read()
		with open("templates/template.scss", 'r') as f:
			scss_template = f.read()
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)

	html_output = ""
	js_output = ""
	scss_output = ""

	# Look through all files in the card-data directory
	for fn in os.listdir("card-data"):
		file_ext = fn[fn.find("."):]
		filename = "card-data" + '/' + fn
		
		# if file is a JSON file
		if (os.path.isfile(filename) and file_ext == ".json"):
			# Get JSON data
			try:
				with open(filename, 'r') as f:
					json_str = f.read()
				json_str = process_json(json_str)
				try:
					json_data = json.loads(json_str)
				except ValueError as e:
					exit("Error processing JSON file: {} \n{}".format(filename, e))
			except IOError as e:
				print "I/O error({0}): {1}".format(e.errno, e.strerror)
			
			# Process the data into the templates and append to output strings
			html_output += generate_card(html_template, json_data) + "\n\n"
			js_output += generate_card(js_template, json_data)+ "\n\n"
			scss_output += generate_card(scss_template, json_data)+ "\n\n"

	# Create the output directory if it does not already exist
	if not os.path.exists("output"):
		os.mkdir("output")
	# Write files to output directory
	try:
		with open("output/output.html", 'w') as f:
			f.write(html_output)
		with open("output/output.js", 'w') as f:
			f.write(js_output)
		with open("output/output.scss", 'w') as f:
			f.write(scss_output)
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)

if __name__ == "__main__":
	main()