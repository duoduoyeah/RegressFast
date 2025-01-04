import unittest
from openai import OpenAI
from dotenv import load_dotenv
import os

class TestDeepSeekAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"), 
            base_url=os.getenv("DEEPSEEK_API_BASE")
        )

    def test_chat_completion(self):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"},
            ],
            stream=False
        )
        
        self.assertIsNotNone(response)
        self.assertTrue(hasattr(response, 'choices'))
        self.assertGreater(len(response.choices), 0)
        self.assertTrue(hasattr(response.choices[0], 'message'))
        self.assertIsNotNone(response.choices[0].message.content)

if __name__ == '__main__':
    unittest.main()