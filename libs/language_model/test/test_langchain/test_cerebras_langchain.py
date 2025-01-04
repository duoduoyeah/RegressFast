import unittest
import asyncio
from langchain_cerebras import ChatCerebras
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class TestCerebrasConcurrency(unittest.TestCase):
    def setUp(self):
        self.llm = ChatCerebras(
            model="llama-3.3-70b",
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "human",
                "Let's play a game of opposites. What's the opposite of {topic}? Just give me the answer with no extra input.",
            )
        ])
        self.chain = self.prompt | self.llm
        self.topics = ["fire", "light", "summer", "happiness", "day"]

    async def async_test_concurrent_requests(self):
        tasks = []
        for topic in self.topics:
            task = self.chain.ainvoke({"topic": topic})
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # Verify we got responses for all topics
        self.assertEqual(len(results), len(self.topics))
        
        # Verify each result has content
        for result in results:
            self.assertIsNotNone(result.content)
            self.assertIsInstance(result.content, str)
            self.assertGreater(len(result.content), 0)

    def test_concurrent_requests(self):
        asyncio.run(self.async_test_concurrent_requests())

if __name__ == '__main__':
    unittest.main()