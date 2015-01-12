import unittest
import json

from card_utility import replace_params, generate_card

class TestCardUtility(unittest.TestCase):
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