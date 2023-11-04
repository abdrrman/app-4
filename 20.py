import os
import streamlit as st
import tempfile

import shutil
from langchain.document_loaders import *


from langchain.docstore.document import Document


from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain


def load_document(doc_path):
    if doc_path.endswith('.txt'):
        loader = TextLoader(doc_path)
    if doc_path.endswith('.csv'):
        loader = CSVLoader(doc_path)
    if doc_path.endswith('.zip'):
        if os.path.exists('Notion_DB') and os.path.isdir('Notion_DB'):
            shutil.rmtree('Notion_DB')
        os.system(f"unzip {doc_path} -d Notion_DB")
        loader = NotionDirectoryLoader("Notion_DB")
    docs = loader.load()
    return docs


def summarize_document(doc_for_summarization):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k",
                     openai_api_key=openai_api_key)
    chain = load_summarize_chain(llm, chain_type="stuff")
    with st.spinner('DemoGPT is working on it. It might take 5-10 seconds...'):
        return chain.run(doc_for_summarization)


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

2. Get the file path of the document you want to summarize.

3. Load the document from the file path.

4. Convert the document to a string for processing.

5. Convert the string back to a document object for summarization.

6. Summarize the document.

7. Display the summarized document to the user.""")


st.sidebar.markdown("# About")
st.sidebar.markdown("📚Article Brevity revolutionizes reading by providing concise, accurate summaries of academic or long-form articles. Designed for students, professionals, and anyone seeking to save time while staying informed, this app allows users to dive deeper into topics of interest and save articles and summaries for convenient offline access.")

with st.form(key="form"):
    st.title('Article Brevity')

    uploaded_file = st.file_uploader("Upload Document", type=[
                                     'txt', 'csv', 'zip'], key='doc_path')

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        if uploaded_file is not None:
            # Create a temporary file to store the uploaded content
            extension = uploaded_file.name.split(".")[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}') as temp_file:
                temp_file.write(uploaded_file.read())
                doc_path = temp_file.name  # it shows the file path
        else:
            doc_path = ''

        if doc_path:
            doc = load_document(doc_path)
        else:
            doc = ''

        doc_string = "".join([doc.page_content for doc in doc])

        doc_for_summarization = [
            Document(page_content=doc_string, metadata={'source': 'local'})]

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            summarized_doc = ""
        elif doc_for_summarization:
            summarized_doc = summarize_document(doc_for_summarization)
        else:
            variable = ""

        if summarized_doc is not None and len(str(summarized_doc)) > 0:
            st.markdown(summarized_doc)