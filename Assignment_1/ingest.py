import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

DATA_PATH = "data/pdfs"
VECTOR_DB_PATH = "vectorstore"

documents = []

for file in os.listdir(DATA_PATH):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(DATA_PATH, file))
        pages = loader.load()
        documents.extend(pages)

documents = [
    d for d in documents if d.page_content and d.page_content.strip()
]

if not documents:
    raise ValueError("No readable text found. PDFs may be scanned images.")

print(f"Loaded {len(documents)} pages with text")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

embeddings = OllamaEmbeddings(model="llama3")

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=VECTOR_DB_PATH
)

print("Vector database created and automatically persisted")
