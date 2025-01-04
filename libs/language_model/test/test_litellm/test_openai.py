import litellm
from dotenv import load_dotenv
import os

load_dotenv()

## set ENV variables
model="gpt-4o"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")

litellm.api_base = "http://chatapi.littlewheat.com/v1"
# os.environ['LITELLM_LOG'] = 'DEBUG'
messages=[{ "content": "Tell me a joke","role": "user"}]
response = litellm.completion(messages=messages, model=model)

print(response.choices[0].message.content)