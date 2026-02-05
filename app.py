import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

CHROMA_PATH = "./flykite_hr_vectordb"
EMBEDDING_MODEL = "thenlper/gte-large"
MODEL_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"
HF_TOKEN = os.environ.get("HF_TOKEN", "")

RETRIEVAL_K = 5
MAX_TOKENS = 768
TEMPERATURE = 0.2
TOP_P = 0.92

SYSTEM_PROMPT = """You are the Flykite Airlines HR Policy Assistant.
Answer employee questions accurately and professionally based ONLY on the provided context.
Do not hallucinate or make assumptions beyond the given context.
If the answer is not in the context, politely say you cannot find that information."""

USER_TEMPLATE = """###Context
{context}

###Question
{question}

Please provide a detailed and accurate answer based on the context above."""

print("Loading embedding model...")
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

print("Loading ChromaDB...")
vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_model)
retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVAL_K})

print("Initializing HuggingFace Inference Client...")
client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)
print("Inference client ready.")

app = FastAPI(title="Flykite HR Chatbot API")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    question = request.question.strip()
    
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = f"{SYSTEM_PROMPT}\n\n{USER_TEMPLATE.format(context=context, question=question)}"
    
    output = client.text_generation(
        prompt=prompt,
        max_new_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P
    )
    
    answer = output.strip()
    
    return QueryResponse(question=question, answer=answer)

@app.get("/health")
def health():
    return {"status": "ok"}
