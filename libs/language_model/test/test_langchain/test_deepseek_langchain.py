import os
import unittest
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

class TestDeepSeekLangChain(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.deepseek_api_base = os.getenv("DEEPSEEK_API_BASE")
        
    def test_basic_chain(self):
        model = ChatOpenAI(
            model="deepseek-chat",
            api_key=self.deepseek_api_key, 
            base_url=self.deepseek_api_base                                                                                                                                                                                                                                          
        )

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a helpful assistant that translates {input_language} to {output_language}.",
            ),
            ("human", "{input}"),
        ])

        chain = prompt | model
        ai_msg = chain.invoke({
            "input_language": "English",
            "output_language": "German", 
            "input": "I love programming.",
        })

        self.assertIsInstance(ai_msg.content, str)
        self.assertTrue(len(ai_msg.content) > 0)

if __name__ == '__main__':
    unittest.main()