import streamlit as st
from query import get_response

st.title("Maahra Customer Service")
st.caption("Ask us anything about our products, shipping, and policies.")

# initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# chat input
if prompt := st.chat_input("Ask a question..."):
    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response(prompt, st.session_state.chat_history)
            st.write(response)

    # save to both display and memory
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.chat_history.append((prompt, response))