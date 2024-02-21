import os
from typing import Any, List, Dict, Set

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone
from consts import INDEX_NAME
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.session_state["OPENAI_API_KEY"]
os.environ["PINECONE_API_KEY"] = st.session_state["PINECONE_API_KEY"]
os.environ["PINECONE_ENVIRONMENT_REGION"] = st.session_state["PINECONE_ENVIRONMENT_REGION"]

def run_llm(model: str, query: str, chat_history: List[Dict[str, Any]] = []) -> Any:
    """
    A function that runs a conversational retrieval chain using OpenAI embeddings and Pinecone for document search.

    Args:
        model (str): The model to be used for chat.
        query (str): The question to be asked.
        chat_history (List[Dict[str, Any]], optional): The chat history. Defaults to [].

    Returns:
        Any: The result of the conversational retrieval chain invocation.
    """
    embeddings = OpenAIEmbeddings(st.session_state["OPENAI_API_KEY"])
    docsearch = Pinecone.from_existing_index(
        index_name=INDEX_NAME, embedding=embeddings
    )
    chat = ChatOpenAI(verbose=True, model=model, temperature=0)

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, retriever=docsearch.as_retriever(), return_source_documents=True
    )

    return qa.invoke({"question": query, "chat_history": chat_history})


def create_sources_string(source_urls: Set[str]) -> str:
    """
    Creates a string representation of a list of source URLs.

    Args:
        source_urls (Set[str]): A set of source URLs.

    Returns:
        str: A string representation of the list of source URLs.
    """
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string


if __name__ == "__main__":
    print(run_llm(query="What is LangChain?"))
