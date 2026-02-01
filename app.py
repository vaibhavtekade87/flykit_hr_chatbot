
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# -----------------------------------------------------------
# Configuration
# -----------------------------------------------------------
CHROMA_PATH = "./flykite_hr_vectordb"
EMBEDDING_MODEL = "thenlper/gte-large"
HF_REPO = "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF"
MODEL_FILE = "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
RETRIEVAL_K = 5
MAX_TOKENS = 768
TEMPERATURE = 0.2
TOP_P = 0.92
TOP_K = 45

# -----------------------------------------------------------
# System and User Prompt Templates
# -----------------------------------------------------------
SYSTEM_PROMPT = """You are the Flykite Airlines HR Policy Assistant.
Answer employee questions accurately and professionally based ONLY on the provided context.
Do not hallucinate or make assumptions beyond the given context.
If the answer is not in the context, politely say you cannot find that information."""

USER_TEMPLATE = """###Context
{context}

###Question
{question}

Please provide a detailed and accurate answer based on the context above."""

# -----------------------------------------------------------
# Load Embedding Model
# -----------------------------------------------------------
print("Loading embedding model...")
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# -----------------------------------------------------------
# Load ChromaDB Vector Store
# -----------------------------------------------------------
print("Loading ChromaDB...")
vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_model)
retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVAL_K})

# -----------------------------------------------------------
# Download and Load Llama Model
# -----------------------------------------------------------
print("Downloading/loading Llama model...")
model_path = hf_hub_download(repo_id=HF_REPO, filename=MODEL_FILE)
llm = Llama(model_path=model_path, n_ctx=2048, verbose=False)
print("Model loaded successfully.")

# -----------------------------------------------------------
# FastAPI App
# -----------------------------------------------------------
app = FastAPI(title="Flykite HR Chatbot API")

# Request/Response schema
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str

# -----------------------------------------------------------
# API Endpoint
# -----------------------------------------------------------
@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Retrieve relevant chunks
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    # Format prompt in Llama 3.1 Instruct format
    prompt = (
        "<|begin_of_text|>"
        "<|start_header_id|>system<|end_header_id|>\n\n"
        f"{SYSTEM_PROMPT}<|eot_id|>"
        "<|start_header_id|>user<|end_header_id|>\n\n"
        f"{USER_TEMPLATE.format(context=context, question=question)}<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>\n\n"
    )

    # Generate response
    output = llm(
        prompt,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        top_k=TOP_K,
        stop=["<|eot_id|>"]
    )

    answer = output["choices"][0]["text"].strip()
    return QueryResponse(question=question, answer=answer)

# -----------------------------------------------------------
# Health Check
# -----------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}
