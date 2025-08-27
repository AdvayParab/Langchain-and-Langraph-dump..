from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="phi3")

response = llm.invoke("Who is our india,s first Ai driven prime company?")
print(response.content)
