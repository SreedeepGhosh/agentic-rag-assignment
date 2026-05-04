from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM, OllamaEmbeddings

VECTOR_DB_PATH = "vectorstore"

prompt = PromptTemplate(
    template="""
You are a question-answering system.
Answer the question using ONLY the provided context.
If the answer cannot be found in the context, say exactly:
"I do not know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=["context", "question"],
)

embeddings = OllamaEmbeddings(model="llama3")

db = Chroma(
    persist_directory=VECTOR_DB_PATH,
    embedding_function=embeddings,
)

llm = OllamaLLM(model="llama3")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
)

if __name__ == "__main__":
    query = input("Ask a question: ")
    response = qa_chain.invoke({"query": query})
    print("\nAnswer:\n", response["result"])