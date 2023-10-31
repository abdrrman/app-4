

import os
import streamlit as st
import tempfile
imports


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
2. Enter your registration data in the text input field.
3. Click on the "Validate" button to validate the registration data.
4. If the registration data is valid, a success message will be displayed.
5. If the registration is successful, a success message will be displayed.""")


st.sidebar.markdown("# About")
st.sidebar.markdown(
    "LMS: Registrier dich! is a comprehensive learning management platform that allows users to easily register and access a wide range of educational resources.")

with st.form(key="form"):
    st.title('LMS: Registrier dich!')
    registration_data = st.text_input("Enter registration data")

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        remaining_code
        remaining_code
        if 'success' in registration_result:
            st.success("Registration successful!")
