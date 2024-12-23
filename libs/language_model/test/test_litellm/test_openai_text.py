import os 
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")

# openai call
response = completion(
    model = "gpt-4o", 
    messages=[
        {"role": "system", "content": "You are a helpful assistant with language model tech configuration."},
        {
            "role": "user",
            "content": "Which model is trained in Oct 2023?"
        }
    ],
)

print(response.choices[0].message.content)