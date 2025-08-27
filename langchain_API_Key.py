import os
import sys
from langchain_openai import ChatOpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print('ERROR: OPENAI_API_KEY is not set. In PowerShell: $env:OPENAI_API_KEY="sk-..."')
    sys.exit(1)

llm = ChatOpenAI(api_key=api_key)
response = llm.invoke("Hello, world!")
print(response.content)