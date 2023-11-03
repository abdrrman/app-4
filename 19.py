

import os
import streamlit as st
import tempfile
imports


function_defs
function_defs
function_defs
function_defs
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
2. Enter a string prompt in the text input field.
3. Click on the "Execute" button to generate the desired output.
4. The output will be displayed below the button.""")


st.sidebar.markdown("# About")
st.sidebar.markdown("LangChain JSON Wizard is a powerful Python tool that converts string prompts into JSON format. It utilizes the langchain library, along with StructuredOutputParser, OutputFixingParser, PromptTemplate, and openai to provide a seamless and efficient conversion process. With LangChain JSON Wizard, you can easily transform your string prompts into structured JSON data, making it easier to work with and analyze.")

with st.form(key="form"):
    st.title('LangChain JSON Wizard')
    string_prompt = st.text_input("Enter string prompt")

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        remaining_code
        remaining_code
        remaining_code
        remaining_code
        remaining_code
        if output is not None:
            st.write(output)
