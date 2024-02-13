from backend.core import run_llm
import streamlit as st
from streamlit_chat import message

st.header("Langchain Documentation Helper Bot")
prompt = st.text_input("Prompt", placeholder="Ask your question here..")

