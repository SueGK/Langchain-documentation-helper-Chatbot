import os
from typing import Any

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone

from consts import INDEX_NAME

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)

def run_llm(query: str) -> Any:
    """Run LLM on query and return answer"""
    embeddings = OpenAIEmbeddings()
    docsearch = Pinecone.from_existing_index(
        index_name=INDEX_NAME, embedding=embeddings
        )
    retriever = docsearch.as_retriever()
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0, verbose=True),
        chain_type="stuff",
        retriever=retriever
    )
    return qa.run({"query": query})

if __name__ == "__main__":
    print(run_llm("What is Langchain?"))


