

import os
import streamlit as st
import tempfile
imports


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


st.sidebar.markdown("""'''
# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) above🔑
2. Provide the path of the XML file you want to parse.
3. Enter the JSON spec that will be used to parse the XML file.
4. The application will parse the JSON spec and load the XML file from the provided path.
5. The parsed XML will be converted into objects.
6. If the objects are successfully created, they will be displayed to you.
'''""")


st.sidebar.markdown("# About")
st.sidebar.markdown("XML Whisperer is a specialized XML parser that converts specific elements into objects. It uses an input spec in JSON format to determine whether each XML element is considered as an object or a collection, supporting both list and dict types. For leaf objects under its parent, they are grouped based on the name of the designated attribute.")

with st.form(key="form"):
    st.title('XML Whisperer')

    uploaded_file = st.file_uploader("Please upload your XML file", type=[
                                     'xml'], key='xml_file_path')

    json_spec = st.text_area("Enter JSON spec")

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        if uploaded_file is not None:
            # Create a temporary file to store the uploaded content
            extension = uploaded_file.name.split(".")[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}') as temp_file:
                temp_file.write(uploaded_file.read())
                xml_file_path = temp_file.name  # it shows the file path
        else:
            xml_file_path = ''

        remaining_code
        remaining_code
        remaining_code
        for obj in objects:
            st.write(obj)
