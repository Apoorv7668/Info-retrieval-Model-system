import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import GooglePalm
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Ensure the API key is set
if not GOOGLE_API_KEY:
    raise ValueError("Google API Key is missing. Please set it in your .env file.")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

print("Google API Key Loaded:", GOOGLE_API_KEY[:5] + "..." + GOOGLE_API_KEY[-5:])  # Partially hide the key for security

def get_pdf_text(pdf_docs):
    """Extract text from uploaded PDF files."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""  # Avoid NoneType errors
    return text

def get_text_chunks(text):
    """Split text into smaller chunks for embedding."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    """Generate vector embeddings and store them in FAISS."""
    embeddings = GooglePalmEmbeddings(google_api_key=GOOGLE_API_KEY)  # Pass the API key explicitly
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store

def get_conversational_chain(vector_store):
    """Create a conversational chain using GooglePalm LLM and FAISS retriever."""
    llm = GooglePalm(google_api_key=GOOGLE_API_KEY)  # Pass the API key explicitly
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vector_store.as_retriever(), memory=memory
    )
    return conversation_chain
