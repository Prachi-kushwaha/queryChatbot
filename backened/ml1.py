from fastapi import FastAPI
from fastapi.responses import JSONResponse
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
print("OPENAI_API_KEY loaded:", bool(os.getenv("OPENAI_API_KEY")))

vectorstore = None

class AnalyzeRequest(BaseModel):
    url: str
    content: str

class AskRequest(BaseModel):
    question:str



@app.post("/analyze")
def analyze_content(req: AnalyzeRequest):
    global vectorstore

    # Split content into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    docs = [Document(
        page_content=req.content,
        metadata={"url": req.url}
    )]
    print(docs[0])

    chunks = splitter.split_documents(docs)
    print(chunks)

    # Store embeddings in FAISS
    if vectorstore is None:
        vectorstore = FAISS.from_documents(chunks, embeddings)
    else:
        vectorstore.add_documents(chunks)

    # retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    # print(retriever)

    return {
        "status": "success",
        "chunks_stored": len(chunks)
    }


@app.post("/ask")
def ask_question(req: AskRequest):
    if vectorstore is None:
        return {"error": "No page analyzed yet"}

    # 1️⃣ Create retriever
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )
    print("Question received:", req.question)


    # 2️⃣ Retrieve relevant chunks
    docs = retriever.invoke(req.question)
    print(docs)

    # Debug: see what was retrieved
    print("Retrieved docs:")
    for d in docs:
        print("----")
        print(d.page_content[:200])

    # 3️⃣ Build context
    context = "\n\n".join(d.page_content for d in docs)

    # 4️⃣ Ask LLM
    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{req.question}
"""

    answer = llm.invoke(prompt).content

    return {
        "answer": answer
    }
