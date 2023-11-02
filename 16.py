

import os
import streamlit as st
import tempfile
imports


function_defs


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)


st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) above🔑
2. Enter the topic you want to search for in the text input field.
3. Click on the "Search" button to perform the search.
4. The search results will be displayed below the input field.""")


st.sidebar.markdown("# About")
st.sidebar.markdown("BioArc: Totally Boring is an app that provides a comprehensive history of Biophilic architecture. Explore the origins, key concepts, and notable examples of this architectural style in a concise and engaging manner.")

with st.form(key="form"):
    st.title('BioArc: Totally Boring')
    topic = st.text_input("Enter the topic")

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        remaining_code
        if history is not None and len(history) > 0:
            st.write(history)
