import mlflow
from fastapi import FastAPI
from schemas import AskRequest, AskResponse
from agentic_query import run_agentic_pipeline

mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("agentic_rag_experiments")

app = FastAPI(
    title="Agentic RAG API",
    description="Chat with local PDFs using an Agentic RAG pipeline (CrewAI + Ollama)",
    version="1.0.0"
)

@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    """
    Accepts a user query, runs the agentic RAG pipeline,
    and returns a grounded answer along with latency.
    """

    with mlflow.start_run():
        # Run agentic pipeline
        result = run_agentic_pipeline(request.query)

        # Log experiment parameters
        mlflow.log_param("query", request.query)
        mlflow.log_param("model", "ollama/llama3")
        mlflow.log_param("retriever_k", 5)

        mlflow.log_metric("latency", result["latency"])

        return AskResponse(
            answer=result["answer"],
            latency=result["latency"]
        )