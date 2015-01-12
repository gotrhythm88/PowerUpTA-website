import json
import re
import sys
import argparse
import os

def replace_params(template, data):
	"""
	Match json strings found in data dictionary to parameters in template
	Replace the parameters and return new text
	"""
	# Find all variables between curly braces, potentially with some spaces
	matches = re.findall("({{ *)(\w*-*\w*)( *}})", template)
	# Process the matches
	for match in matches:
		key = match[1]
		if key in data:
			template = template.replace(match[0] + match[1] + match[2], data[key])
		# If no data supplied in dictionary, that was an optional parameter, just delete it
		else:
			template = template.replace(match[0] + match[1] + match[2], "")
	return template

def generate_card(template, data):
	"""
	Matches json data found in data to parameters in template
	Recursively fills in for loops
	"""
	# Look for a loop
	loop_start = re.search("{{( *)for (\w+) in (\w+)( *)}}", template)
	# If we found a loop, process it
	if loop_start:
		# Find the end of the for loop
		loop_start_begin = loop_start.start()
		loop_start_end = loop_start.end()
		loop_close = re.search("{{( *)endfor( *)}}", template[loop_start_end:])

		loop_close_begin = loop_start_end
		loop_close_end = loop_start_end

		# Find the end of the outermost for loop
		while loop_close:
			loop_close_begin = loop_close_end + loop_close.start()
			loop_close_end += loop_close.end()
			loop_close = re.search("{{( *)endfor( *)}}", template[loop_close_end:])

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

def make_parser():
	parser = argparse.ArgumentParser(
		prog='card_utility.py'
		, description = "Utility to generate html and other files from templates and json data"
	)

	parser.add_argument("template", help="HTML or other template to be filled in with JSON data")
	parser.add_argument("-j", "--json", help="JSON data to be filled into template")
	parser.add_argument("-f", "--filename", help="output filename", default="output")
	parser.add_argument("-i", "--input", help="directory of JSON files to be processed into template", default="cards")
	parser.add_argument("-o", "--output", help="directory of output files", default="output")

	return parser


def main():
	# Create command line parser
	parser = make_parser()
	args = parser.parse_args(sys.argv[1:])

	# Convert parsed arguments from Namespace to dictionary
	args = vars(args)
	
	# Get the template
	filename = args["template"]
	template_ext = filename[filename.find("."):]
	with open(filename, 'r') as f:
		template = f.read()

	# If user supplied single file of JSON data, process that data into the template
	if args["json"] != None:
		# Get JSON data
		filename = args["json"]
		with open(filename, 'r') as f:
			json_str = f.read()
		json_data = json.loads(json_str)
		# Process it into the template
		output = generate_card(template, json_data)
		filename = args["filename"]
		if filename == "output":
			filename += template_ext
		with open(filename, 'w') as f:
			f.write(output)
		return
	# Otherwise, check if user supplied a directory of JSON files to use (and try default "cards")
	else:
		input_dir = args["input"]
		output_dir = args["output"]
		for fn in os.listdir(input_dir):
			file_ext = fn[fn.find("."):]
			file_begin = fn[:fn.find(".")]
			filename = input_dir + '/' + fn
			# if file is a JSON file
			if (os.path.isfile(filename) and file_ext == ".json"):
				# Get JSON data
				with open(filename, 'r') as f:
					json_str = f.read()
				json_data = json.loads(json_str)
				# Process into the template
				output = generate_card(template, json_data)
				# Create the output directory if it does not already exist
				if not os.path.exists(output_dir):
					os.mkdir(output_dir)
				# Write to output directory
				with open(output_dir + "/" + file_begin + template_ext, 'w') as f:
					f.write(output)

if __name__ == "__main__":
	main()