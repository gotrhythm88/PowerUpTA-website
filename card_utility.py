import json
import re

def replace_params(template, data):
	"""
	Match json strings found in data dictionary to parameters in template
	Replace the parameters and return new text
	"""
	# Find all variables between curly braces, potentially with some spaces
	matches = re.findall("({{ *)(.*)( *}})", template)
	# Process the matches
	for match in matches:
		key = match[1].strip()
		if key in data:
			template = template.replace(match[0] + match[1] + match[2], data[key])
		# If no data supplied in dictionary, that was an optional parameter, just delete it
		else:
			template.replace(match[0] + match[1] + match[2], "")
	return template

def generate_card(template, data):
	"""
	Matches json data found in data to parameters in template
	Recursively fills in data with for loops
	"""
	# Look for a loop
	loop_start = re.search("{{( *)for (\w+) in (\w+)( *)}}", template)
	# If we found a loop, process it
	if loop_start:
		# Pull out the data for that loop
		key = loop_start.group(3)
		dict_ = data[key]

		# Find the end of the for loop
		begin = loop_start.end()
		loop_end = re.search("{{( *)endfor( *)}}", template[begin:])
		end = 0

		if loop_end:
			while loop_end.start() > end:
				end = begin + loop_end.start()
				loop_end = re.search("{{( *)endfor( *)}}", template[end:])
		
		# Split up the template
		beginning = template[:begin]
		middle = template[begin:end]
		#print "middle is " + middle
		end = template[end:]

		# Recursively process the middle and concatenate to the beginning
		for element in dict_:
			#print "element is " + str(element)
			#print "middle is " + middle
			beginning += generate_card(middle, element)

		# Add back on the end
		template = beginning + end

		# Clean up
		template = template.replace("{{( *)for (\w+) in (\w+)( *)}}", "")
		template = template.replace("{{( *)endfor( *)}}", "")

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