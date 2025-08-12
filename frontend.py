# 4. Frontend with Streamlit (frontend.py)
# UPDATED SCRIPT: This now uses st.markdown to correctly render multi-line code.

import streamlit as st
import requests

st.title("Coding Doubts GPT")
st.write("Ask any coding-related question and get an answer from the AI assistant.")

user_question = st.text_input("Your question:")

if st.button("Get Answer"):
    if user_question:
        api_url = "http://127.0.0.1:5000/ask"
        payload = {"question": user_question}
        
        with st.spinner("Thinking..."):
            try:
                response = requests.post(api_url, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.success("Here's the answer:")
                    # Use st.markdown with a code block to ensure newlines are rendered
                    answer_text = result['answer']
                    st.markdown(f"```python\n{answer_text}\n```")
                else:
                    st.error(f"Error from API: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to the backend API. Is it running? Error: {e}")
    else:
        st.warning("Please enter a question.")
