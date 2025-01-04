import unittest
from openai import OpenAI

class TestO1API(unittest.TestCase):
    def setUp(self):
        self.client = OpenAI()
        self.prompt = """
Write a bash script that takes a matrix represented as a string with 
format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
"""

    def test_o1_api(self):
        try:
            response = self.client.chat.completions.create(
                model="o1",
                messages=[
                    {
                        "role": "user",
                        "content": self.prompt
                    }
                ],
                max_tokens=100
            )
            
            # Verify we got a response
            self.assertIsNotNone(response)
            self.assertIsNotNone(response.choices[0].message.content)
            self.assertGreater(len(response.choices[0].message.content), 0)
            
        except Exception as e:
            self.fail(f"API call failed with error: {str(e)}")

if __name__ == '__main__':
    unittest.main()