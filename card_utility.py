import json
import re

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

if __name__ == "__main__":
	with open('class-sample.json', 'r') as f:
		json_str = f.read()
	json_data = json.loads(json_str)

	with open('template.html', 'r') as f:
		html_template = f.read()

	with open('template.js', 'r') as f:
		js_template = f.read()

	html = generate_card(html_template, json_data)
	with open("output.html", 'w') as f:
		f.write(html)
	
	js = generate_card(js_template, json_data)
	with open("output.js", 'w') as f:
		f.write(js)