"""
AI Tutor — C401 AI in Action — Streamlit Chat UI.

Usage:
    cd src && streamlit run app.py
"""

import streamlit as st

from agent import create_tutor_agent

st.set_page_config(page_title="AI Tutor — C401", page_icon="🎓")
st.title("🎓 AI Tutor — C401 AI in Action")

if "agent" not in st.session_state:
    st.session_state.agent = create_tutor_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Hỏi mình về khoá học AI in Action..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang suy nghĩ..."):
            response = st.session_state.agent.invoke(
                {"messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]}
            )
            answer = response["messages"][-1].content
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
