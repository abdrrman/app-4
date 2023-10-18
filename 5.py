
from langchain.document_loaders import *
import shutil
import os
import streamlit as st
import tempfile


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) above🔑
2. Fill in the case details in the chat input.
3. Upload legal documents related to the case using the "Legal Documents" file uploader.
4. Wait for the legal documents to be loaded and summarized.
5. View the generated legal advice provided by the AI assistant in the chat interface.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("Lawbot+ is an AI-powered application designed to assist lawyers in their legal research and analysis. With its advanced algorithms, Lawbot+ can quickly analyze legal documents, provide relevant case law and statutes, and offer valuable insights to support legal professionals in their decision-making process.")


st.title('Lawbot+')
# Get case details from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if case_details := st.chat_input("Enter the case details"):
    with st.chat_message("user"):
        st.markdown(case_details)
    st.session_state.messages.append({"role": "user", "content": case_details})
# Get legal documents related to the case from the user
uploaded_file = st.file_uploader("Legal Documents", type=[
                                 'zip'], key='legal_documents')
if uploaded_file is not None:
    # Create a temporary file to store the uploaded content
    extension = uploaded_file.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}') as temp_file:
        temp_file.write(uploaded_file.read())
        legal_documents = temp_file.name  # it shows the file path
else:
    legal_documents = ''
# Load the legal documents as Document from the file path


def load_legal_documents(legal_documents):
    if os.path.exists('Notion_DB') and os.path.isdir('Notion_DB'):
            shutil.rmtree('Notion_DB')
        os.system(f"unzip {legal_documents} -d Notion_DB")
        loader = NotionDirectoryLoader("Notion_DB")
    docs = loader.load()
    return docs
if legal_documents:
    legal_docs = load_legal_documents(legal_documents)
else:
    legal_docs = ''
#Convert the loaded documents to string for further processing
legal_docs_string = "".join([doc.page_content for doc in legal_docs])
#Summarize the legal documents
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain

def summarize_legal_docs(legal_docs_string):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")
    with st.spinner('DemoGPT is working on it. It might take 5-10 seconds...'):
        return chain.run(legal_docs_string)
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    summarized_legal_docs = ""
elif legal_docs_string:
    summarized_legal_docs = summarize_legal_docs(legal_docs_string)
else:
    summarized_legal_docs = ""
#Convert the summarized legal documents back to Document object
from langchain.docstore.document import Document
summarized_legal_docs_doc =  [Document(page_content=summarized_legal_docs, metadata={'source': 'local'})]
#Analyze the case details and summarized legal documents to provide legal advice
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

msgs = StreamlitChatMessageHistory()

def provide_legal_advice(case_details,summarized_legal_docs_doc):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'case_details', 'summarized_legal_docs_doc'], template='''You are a legal advisor. Analyze the given case details and summarized legal documents to provide legal advice.

Case Details: {case_details}

Summarized Legal Documents: {summarized_legal_docs_doc}

{chat_history}
Human: {case_details}
Legal Advisor:'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="case_details", chat_memory=msgs, return_messages=True)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=openai_api_key, temperature=0)
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory
        )
    
    return chat_llm_chain.run(case_details=case_details, summarized_legal_docs_doc=summarized_legal_docs_doc)
    

if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    legal_advice = ""
elif case_details and summarized_legal_docs_doc:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        legal_advice = provide_legal_advice(case_details,summarized_legal_docs_doc)
else:
    legal_advice = ""
#Display the generated legal advice to the user
import time

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in legal_advice.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
