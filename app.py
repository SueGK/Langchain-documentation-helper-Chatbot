from backend.core import run_llm, create_sources_string
import streamlit as st


st.set_page_config(page_title="Docs Helper", layout="wide")

st.title("🤠 Langchain Documentation Helper Bot")

# configure session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# configure run_llm to use the session state
model = st.session_state["openai_model"]

# display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# run the chat
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # display the current user prompt
    with st.chat_message("user"):
        st.markdown(prompt)

    # generate and display model response
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            output = run_llm(
                model=st.session_state["openai_model"],
                query=prompt,
                chat_history=st.session_state.chat_history,
            )
            answer = output["answer"]
            # add sources to the response
            sources = set(
                [doc.metadata["source"] for doc in output["source_documents"]]
            )
            answer_with_sources = f"{answer} \n\n {create_sources_string(sources)}"

            st.markdown(answer_with_sources)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer_with_sources}
            )
            # store chat history
            st.session_state.chat_history.append((prompt, answer))
