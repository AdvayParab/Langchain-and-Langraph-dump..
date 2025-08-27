import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA

# Streamlit App
st.set_page_config(page_title="Free RAG App", layout="wide")
st.title("📄 RAG Chatbot (Free & Local)")

# Upload document
uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    st.success(f"Loaded file: {uploaded_file.name}")

    # 1. Load document
    if uploaded_file.type == "application/pdf":
        loader = PyPDFLoader(uploaded_file.name)
    else:
        loader = TextLoader(uploaded_file.name)
    documents = loader.load()

    # 2. Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    # 3. Embeddings (HuggingFace - free)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 4. Vectorstore (Chroma)
    vectorstore = Chroma.from_documents(docs, embeddings)

    # 5. Local LLM (Ollama)
    llm = ChatOllama(model="phi3")  # Try "mistral" or "llama3" if you want

    # 6. RetrievalQA
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff"
    )

    # Chat UI
    query = st.text_input("💬 Ask a question:")
    if query:
        with st.spinner("Thinking..."):
            answer = qa.run(query)
        st.write("### 🤖 Answer:")
        st.write(answer)
