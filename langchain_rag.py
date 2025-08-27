from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA

# 1. Load Documents (PDF or TXT)
loader = PyPDFLoader("attention.pdf")   # For PDF
# loader = TextLoader("sample.txt")        # For a text file
documents = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

# 3. Create Embeddings (FREE with HuggingFace)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4. Store in Vector DB (Chroma)
vectorstore = Chroma.from_documents(docs, embeddings)

# 5. Use Local LLM (Ollama)
llm = ChatOllama(model="phi3")  # You can also try "mistral" or "llama3"

# 6. Build RAG Chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type="stuff"  # simple strategy
)

# 7. Ask Questions!
while True:
    query = input("Ask a question (or type 'exit'): ")
    if query.lower() == "exit":
        break
    answer = qa.run(query)
    print("\nAnswer:", answer, "\n")
