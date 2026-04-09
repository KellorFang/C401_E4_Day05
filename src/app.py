"""
AI Tutor — C401 AI in Action — Streamlit Chat UI.

Usage:
    streamlit run src/app.py
"""

import streamlit as st

from agent import create_tutor_agent

# --- Page Config ---
st.set_page_config(page_title="AI Tutor — C401", page_icon="🎓")
st.title("AI Tutor — C401 AI in Action")

# TODO (Teammate): Implement the chat UI
#
# Suggested approach using Streamlit chat components:
#
# 1. Initialize agent in session state (run once):
#    if "agent" not in st.session_state:
#        st.session_state.agent = create_tutor_agent()
#
# 2. Initialize message history:
#    if "messages" not in st.session_state:
#        st.session_state.messages = []
#
# 3. Display chat history:
#    for msg in st.session_state.messages:
#        with st.chat_message(msg["role"]):
#            st.markdown(msg["content"])
#
# 4. Handle user input:
#    if prompt := st.chat_input("Hỏi mình về khoá học AI in Action..."):
#        st.session_state.messages.append({"role": "user", "content": prompt})
#        with st.chat_message("user"):
#            st.markdown(prompt)
#
#        # 5. Get agent response (streaming):
#        with st.chat_message("assistant"):
#            response = st.session_state.agent.invoke(
#                {"messages": [{"role": "user", "content": prompt}]}
#            )
#            # Extract the final message content from response
#            # st.markdown(response_content)
#
#        st.session_state.messages.append(
#            {"role": "assistant", "content": response_content}
#        )

st.info("🚧 Chat UI chưa được implement. Xem TODOs trong source code.")
