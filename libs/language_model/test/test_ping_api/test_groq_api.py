from groq import Groq
import os
import unittest
from dotenv import load_dotenv

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("GROQ_API_KEY: ", GROQ_API_KEY)
        
class TestGroqAPI(unittest.TestCase):
    def setUp(self):
        self.prompt=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant that provides concise responses."
                                    "answer each question with less than 10 words."
                    },
                    {
                        "role": "user", 
                        "content": "Explain the importance of fast language models"
                    }
            ]
        
    def test_chat_completion(self):
        client = Groq()
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.prompt,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stop=None,
        )
        
        response_content = completion.choices[0].message.content
        print("response_content[:40]: ", response_content[:40])
        self.assertIsInstance(response_content, str)
        self.assertTrue(len(response_content) > 0)
        # Split response into words and check length
        word_count = len(response_content.split())
        self.assertLess(word_count, 20, "Response should be less than 20 words")

if __name__ == '__main__':
    unittest.main()