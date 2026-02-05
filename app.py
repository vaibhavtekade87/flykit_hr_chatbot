import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

CHROMA_PATH = "./flykite_hr_vectordb"
EMBEDDING_MODEL = "thenlper/gte-large"
MODEL_ID = "HuggingFaceTB/SmolLM3-3B"
HF_TOKEN = os.environ.get("HF_TOKEN", "")

RETRIEVAL_K = 5
MAX_TOKENS = 512
TEMPERATURE = 0.1
TOP_P = 0.9

SYSTEM_PROMPT = """You are Flykite Airlines HR Policy Assistant. Answer questions using ONLY the provided context. Be concise and direct. Do not add explanations, reasoning, or extra details not in the context."""

USER_TEMPLATE = """{context}

Question: {question}

Answer based strictly on the context above. Be brief and factual."""

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
    
    user_message = USER_TEMPLATE.format(context=context, question=question)
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]
    
    response = client.chat_completion(
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P
    )
    
    answer = response.choices[0].message.content.strip()
    
    return QueryResponse(question=question, answer=answer)

@app.get("/health")
def health():
    return {"status": "ok"}
