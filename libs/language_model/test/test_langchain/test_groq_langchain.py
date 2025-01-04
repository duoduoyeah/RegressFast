
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import unittest

load_dotenv()
    
class TestGroqLangchain(unittest.TestCase):
    def test_direct_api_basic_conversation(self):
        self.assertIsInstance(os.getenv("GROQ_API_KEY_MYSELF"), str)
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.0,
            max_retries=2,
            groq_api_key=os.getenv("GROQ_API_KEY_MYSELF"),
            base_url=None,
        )
        
        messages = [
            ("system", "You are a helpful translator. Translate the user \
            sentence to French."),
            ("human", "I love programming. What about you?"),
        ]
        ai_msg = llm.invoke(messages)
        self.assertIsInstance(ai_msg.content, str)
        self.assertTrue(len(ai_msg.content) > 0)
        print("ai_msg.content[:100]: ", ai_msg.content[:100])
        
    def test_basic_conversation(self):

        self.assertIsInstance(os.getenv("GROQ_API_KEY"), str)
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        print("GROQ_API_KEY: ", GROQ_API_KEY)
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.0,
            max_retries=2,
            base_url=None,
        )
        
        messages = [
            ("system", "You are a helpful translator. Translate the user \
            sentence to French."),
            ("human", "I love programming. What about you?"),
        ]
        ai_msg = llm.invoke(messages)
        self.assertIsInstance(ai_msg.content, str)
        self.assertTrue(len(ai_msg.content) > 0)
        print("ai_msg.content[:100]: ", ai_msg.content[:100])
        
    def test_basic_chain(self):
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            base_url=None,
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    ("You are a helpful assistant that answers questions about the user's input." \
                    "Your return should be in JSON format with the following keys: 'answer' and 'source'."
                    ),
                ),
                ("human", "{input}"),
            ]
        )

        chain = prompt | llm
        ai_msg = chain.invoke(
            {
                "input": "What is the capital of France?",
            }
        )
        
        self.assertIsInstance(ai_msg.content, str)
        self.assertTrue(len(ai_msg.content) > 0)

if __name__ == '__main__':
    unittest.main()