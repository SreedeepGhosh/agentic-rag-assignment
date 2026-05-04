from crewai import Agent, Task, Crew
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM, OllamaEmbeddings
import time

VECTOR_DB_PATH = "vectorstore"

llm = OllamaLLM(
    model="ollama/llama3",
    temperature=0
)

embeddings = OllamaEmbeddings(model="llama3")

db = Chroma(
    persist_directory=VECTOR_DB_PATH,
    embedding_function=embeddings
)

retriever = db.as_retriever(search_kwargs={"k": 6})

def retrieve_context(question: str) -> str:
    docs = retriever.invoke(question)
    if not docs:
        return ""
    return "\n\n".join(d.page_content for d in docs)

def run_agentic_pipeline(question: str) -> dict:
    start_time = time.time()

    context = retrieve_context(question)

    if not context.strip():
        return {
            "answer": "I do not know based on the provided documents.",
            "latency": 0.0
        }

    analyst = Agent(
        role="Document Analyst",
        goal="Understand the overall structure and themes of the document.",
        backstory="You analyze documents and identify major topics and entities.",
        llm=llm,
        verbose=False
    )

    synthesizer = Agent(
        role="Project Synthesizer",
        goal="Produce a clear, high-level summary grounded in the document.",
        backstory="You summarize multiple projects and themes accurately.",
        llm=llm,
        verbose=False
    )

    validator = Agent(
        role="Validator",
        goal="Ensure the summary is supported by the provided context.",
        backstory="You remove unsupported or hallucinated claims.",
        llm=llm,
        verbose=False
    )

    analysis_task = Task(
        description=f"""
Analyze the document context and identify:
- The type of document
- Major themes
- Types of projects described

Context:
{context}
""",
        expected_output="High-level understanding of document structure.",
        agent=analyst
    )

    synthesis_task = Task(
        description="""
Using the analysis, write a concise document-level summary
in 1-2 short paragraphs.

Rules:
- No guessing beyond context
- Summarize projects and research themes
- DO NOT use bullet points
- DO NOT add external information
""",
        expected_output="Concise document summary.",
        agent=synthesizer
    )

    validation_task = Task(
        description="""
Review the summary and remove:
- Unsupported statements
- Exaggerations
- Hallucinations

If nothing meaningful remains, return:
"I do not know based on the provided documents."
""",
        expected_output="Validated final summary.",
        agent=validator
    )

    crew = Crew(
        agents=[analyst, synthesizer, validator],
        tasks=[analysis_task, synthesis_task, validation_task],
        verbose=False
    )

    result = crew.kickoff()
    latency = round(time.time() - start_time, 2)

    final_answer = result.raw.strip()
    if not final_answer:
        final_answer = "I do not know based on the provided documents."

    return {
        "answer": final_answer,
        "latency": latency
    }

if __name__ == "__main__":
    q = input("Ask a question: ")
    output = run_agentic_pipeline(q)
    print("\n✅ ANSWER\n")
    print(output["answer"])
    print("\nLatency:", output["latency"], "seconds")