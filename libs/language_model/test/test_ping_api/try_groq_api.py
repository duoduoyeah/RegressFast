from groq import Groq
import os

class TryGroqAPI:
    def setUp(self):
        # self.official = os.getenv("GROQ_API_KEY")
        self.key = os.getenv("GROQ_API_KEY_TEMP")
        self.url = os.getenv("GROQ_API_BASE")
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
        client = Groq(
            api_key=self.key,
        )
        # print("API Key:", self.official)
        # print("Base URL:", self.url)
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.prompt,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stop=None,
        )
        
        response_content = completion.choices[0].message.content
        print("response_content[:5]: ", response_content[:5])
        
if __name__ == '__main__':
    try_groq = TryGroqAPI()
    try_groq.setUp()
    try_groq.test_chat_completion()
