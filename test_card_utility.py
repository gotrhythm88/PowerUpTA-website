import unittest
import json

from card_utility import replace_params, generate_card, process_json

class TestCardUtility(unittest.TestCase):
	def test_process_json(self):
		json_str = """{
			"tab1": "	This is tab 1."
			,"tab2": "This is tab 2.	"
			,"tab3": "	This is tab 3.	"
			,"newline1": "This
			is newline 1."
			,"newline2": "
			This is newline 2."
			,"newline3": "This is newline 3.
			"
			,"spaces1": "  This is spaces 1."
			,"spaces2": "This is spaces 2.  "
			,"spaces3": "  This is spaces 3.  "
			,"spaces4": "  This is  spaces 4.  "
		}"""

		correct_str = """{ "tab1": " This is tab 1." ,
"tab2": "This is tab 2. " ,
"tab3": " This is tab 3. " ,
"newline1": "This is newline 1." ,
"newline2": " This is newline 2." ,
"newline3": "This is newline 3. " ,
"spaces1": " This is spaces 1." ,
"spaces2": "This is spaces 2. " ,
"spaces3": " This is spaces 3. " ,
"spaces4": " This is spaces 4. " }"""
		
		# Check that the string processes correctly
		self.assertEqual(process_json(json_str), correct_str)
		# Check that the json loads into the python dictionary correctly
		json_data = json.loads(process_json(json_str))
		self.assertEqual(json_data, json.loads(correct_str))
		self.assertEqual(len(json_data), 10)
		self.assertEqual(json_data["tab3"], " This is tab 3. ")
		self.assertEqual(json_data["spaces4"], " This is spaces 4. ")

	def test_replace_params(self):
		# Test some basic examples
		template = "Hello, my name is {{ name }}. I like to do {{activity}}. My friend's name is {{ friend-name}}. She likes to {{ friend-activity }}. This line is optional:{{ optional }}."

		json_str = """{
			"name": "Bob"
			,"activity": "stuff"
			,"friend-name": "Alice"
			,"friend-activity": "code"
		}"""
		json_data = json.loads(json_str)
 		
 		output = "Hello, my name is Bob. I like to do stuff. My friend's name is Alice. She likes to code. This line is optional:."

 		self.assertEqual(replace_params(template, json_data), output)

 	def test_generate_card(self):
		# Test a basic for loop
		template = """
			Hello, my name is {{ name }}. I have three friends:
			{{ for friend in friends }}
				{{ name }} lives in {{ city }}.
			{{endfor}}
			My three friends are {{ adjective }}."""

		json_str = """{
			"name": "Shannon"
			, "friends":
				[
					{
						"name": "Bob"
						,"city": "New York"
					},
					{
						"name": "Alice"
						,"city": "Houston"
					},
					{
						"name": "Jane"
						,"city": "Chicago"
					}
				]
			, "adjective": "awesome"
		}"""
		json_data = json.loads(json_str)
 		
 		output = """
			Hello, my name is Shannon. I have three friends:
				Bob lives in New York.
				Alice lives in Houston.
				Jane lives in Chicago.
			My three friends are awesome."""

		# Remove random tabs before checking equivalence (just here for readability)
		template = template.replace("\t", "")
		output = output.replace("\t", "")
 		self.assertEqual(generate_card(template, json_data), output)

 		# Test a nested for loop
 		template = """
			Hello, my name is {{ name }}. I have two friends with pets:
			{{ for friend in friends }}
				{{ name }}
				{{ for pet in pets }}
					{{ name }} is a {{ species }}.
				{{endfor}}
			{{endfor}}
			"""

		json_str = """{
			"name": "Shannon"
			, "friends":
				[
					{
						"name": "Bob"
						,"pets":
						[
							{
								"name":"Fluffy"
								,"species":"cat"
							},
							{
								"name":"Roger"
								,"species":"fish"
							}

						]
					},
					{
						"name": "Alice"
						,"pets":
						[
							{
								"name":"Knuckles"
								,"species":"echidna"
							},
							{
								"name":"Sonic"
								,"species":"hedgehog"
							}

						]
					}
				]
		}"""
		json_data = json.loads(json_str)
 		
 		output = """
			Hello, my name is Shannon. I have two friends with pets:
				Bob
					Fluffy is a cat.
					Roger is a fish.
				Alice
					Knuckles is a echidna.
					Sonic is a hedgehog.
			"""
		
		# Remove random tabs before checking equivalence (just here for readability)
		template = template.replace("\t", "")
		output = output.replace("\t", "")
 		self.assertEqual(generate_card(template, json_data), output)

if __name__ == "__main__":
    unittest.main()