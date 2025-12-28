from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://medium.com/")

embeddings = OpenAIEmbeddings(
    model = "text-embedding-small"
)

vectorStore = FAISS.from_documents(loader, embeddings)
retriever = vectorStore.as_retriever(search_kwargs={"k": 4})