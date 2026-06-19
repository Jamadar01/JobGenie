import streamlit as st
import requests

st.title("JobGenie")

# --- Sidebar: upload from device ---
with st.sidebar:
    st.header("Your resume")
    resume = st.file_uploader("Upload from device", type=["pdf"])
    if resume is not None:
        st.success(f"Loaded: {resume.name}")
        st.session_state["resume_bytes"] = resume.getvalue()   # store so it persists
        st.session_state["resume_name"] = resume.name

# --- Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask about jobs...")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if "resume_bytes" in st.session_state:          # send resume if uploaded
        resp = requests.post(
            "http://localhost:8000/match",
            files={"resume": (st.session_state["resume_name"],
                              st.session_state["resume_bytes"], "application/pdf")},
            data={"question": prompt},
        ).json()
    else:
        resp = requests.post("http://localhost:8000/ask",
                             json={"question": prompt}).json()

    answer = resp.get("answer", "")
    with st.chat_message("assistant"):
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})