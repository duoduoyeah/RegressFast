# https://python.langchain.com/api_reference/community/chat_models/langchain_community.chat_models.perplexity.ChatPerplexity.html

from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import ChatPromptTemplate

chat = ChatPerplexity(
    model="llama-3.1-sonar-small-128k-online",
    temperature=0.7,
)