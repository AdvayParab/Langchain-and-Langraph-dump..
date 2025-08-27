## Data Ingestion
from langchain_community.document_loaders import TextLoader
loader=TextLoader("speech.txt")
text_documents=loader.load()
print(text_documents)

import os
import bs4
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
load_dotenv()

os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")

# web based loader


## load,chunk and index the content of the html page

loader=WebBaseLoader(web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
                     bs_kwargs=dict(parse_only=bs4.SoupStrainer(
                         class_=("post-title","post-content","post-header")

                     )))

text_documents=loader.load()


print(text_documents)

## Pdf reader
from langchain_community.document_loaders import PyPDFLoader
loader=PyPDFLoader('attention.pdf')
docs=loader.load()

print(docs)

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
documents=text_splitter.split_documents(docs)
print(documents[:5])

print(documents)

## Vector Embedding And Vector Store
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
db = Chroma.from_documents(documents,OpenAIEmbeddings())

query = "Who are the authors of attention is all you need?"
retireved_results=db.similarity_search(query)
print(retireved_results[0].page_content)

## FAISS Vector Database
from langchain_community.vectorstores import FAISS
db = FAISS.from_documents(documents[:15], OpenAIEmbeddings())

