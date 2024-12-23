import unittest
from openai import OpenAI
import os
from dotenv import load_dotenv

class TestOpenAIAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.client = OpenAI()

    def test_chat_completion(self):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user", 
                    "content": "Write a haiku about recursion in programming."
                }
            ]
        )
        
        self.assertIsNotNone(completion)
        self.assertTrue(hasattr(completion, 'choices'))
        self.assertGreater(len(completion.choices), 0)
        self.assertTrue(hasattr(completion.choices[0], 'message'))
        self.assertIsNotNone(completion.choices[0].message.content)

if __name__ == '__main__':
    unittest.main()