

import os
import streamlit as st
import tempfile


from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)


def llama2ContentGenerator(content_type, tenant_id):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to generate content using llama2. The content type is '{content_type}' and the tenant id is '{tenant_id}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please generate {content_type} for tenant with id {tenant_id}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(content_type=content_type, tenant_id=tenant_id)
    return result  # returns string


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
2. From the sidebar, select the content type you want to generate from the options: "Text", "Image", "Video", "Audio".
3. Enter the tenant id in the provided text input field.
4. Click on the 'Run' button to start the content generation process. If the OpenAI API key is not valid or the content type and tenant id are not provided, a warning message will be displayed.
5. Wait for the process to complete. A spinner will be displayed indicating that the content is being generated. This process usually takes less than 10 seconds.
6. Once the content is generated, it will be displayed on the screen. If the generated content is empty or None, nothing will be displayed.
'''""")


st.sidebar.markdown("# About")
st.sidebar.markdown("Llama Drama BizApp is a B2B multi-tenant application designed for efficient content generation. Utilizing the power of Llama2, it enables businesses to create high-quality content seamlessly across multiple tenants.")

with st.form(key="form"):
    st.title('Llama Drama BizApp')
    content_type = st.selectbox("Select the content type", [
                                "Text", "Image", "Video", "Audio"])
    tenant_id = st.text_input("Enter tenant id")

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            generated_content = ""
        elif (isinstance(content_type, bool) or content_type) and (isinstance(tenant_id, bool) or tenant_id):
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                generated_content = llama2ContentGenerator(
                    content_type, tenant_id)
        else:
            generated_content = ""

        for content in generated_content:
            if content is not None and len(str(content)) > 0:
                st.text(content)
