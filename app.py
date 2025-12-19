import streamlit as st
from langchain_community.llms import Ollama

st.set_page_config(page_title="Open Source AI", layout="centered")

# -------------------------
# SIMPLE LOGIN
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []

USERNAME = "user"
PASSWORD = "user"

if not st.session_state.logged_in:
    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == USERNAME and p == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

# -------------------------
# CHAT UI
# -------------------------
else:
    st.title("Personal AI")

    model = st.selectbox(
        "Choose Model",
        ["llama3", "mistral", "phi3"]
    )

    llm = Ollama(model=model)

    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input (NO LOOP)
    prompt = st.chat_input("Ask something")

    if prompt:
        # User message
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Build context
        context = ""
        for m in st.session_state.messages:
            context += f"{m['role']}: {m['content']}\n"

        # AI response
        response = llm.invoke(context)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

        with st.chat_message("assistant"):
            st.markdown(response)
