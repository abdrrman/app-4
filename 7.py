

import os
import streamlit as st
import tempfile

from langchain.docstore.document import Document


from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chains import LLMMathChain
from langchain.callbacks import StreamlitCallbackHandler


from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain


from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)


def queryGoogle(headings_subheadings):
    search_input = "Query each heading and subheading on Google: {headings_subheadings}".format(
        headings_subheadings=headings_subheadings)
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0)
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    tools = [
        DuckDuckGoSearchRun(name="Search"),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math"
        ),
    ]
    model = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
    return agent.run(search_input, callbacks=[st_cb])


def summarizeSERP(SERP_doc):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")
    with st.spinner('DemoGPT is working on it. It might take 5-10 seconds...'):
        return chain.run(SERP_doc)


def serpDescriber(summarized_SERP):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to write brief descriptions for each summarized Search Engine Results Page (SERP)."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """The summarized SERP is: '{summarized_SERP}'. Please write a brief description for each result."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(summarized_SERP=summarized_SERP)
    return result  # returns string


def descriptionInserter(descriptions):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant designed to insert descriptions back into an outline."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please insert the following descriptions: '{descriptions}' back into the outline."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(descriptions=descriptions)
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
2. In the text input field, enter the outline for which you want to generate content.
3. The application will convert your outline into a Document object.
4. The application will then extract each heading and subheading from your outline.
5. Each heading and subheading will be queried on Google.
6. The Search Engine Results Page (SERP) results will be converted into a Document object.
7. The application will then summarize the SERP results.
8. A brief description will be written for each summarized SERP result.
9. These descriptions will be inserted back into your original outline.
10. The updated outline, now filled with content, will be displayed to you.

Please note that the application uses OpenAI's GPT-3.5-turbo model to generate content. The process may take a few seconds to complete.
'''""")


st.sidebar.markdown("# About")
st.sidebar.markdown("Lazy Writers Dream is an innovative tool designed to streamline the content creation process. It takes each heading and subheading from a user-provided outline, queries them on Google, scrapes the first SERP result, and generates a brief description. This description, along with tips on how to rank higher, is then inserted back into the outline, providing valuable insights for copywriters.")

with st.form(key="form"):
    st.title('Lazy Writers Dream')
    outline = st.text_input("Enter the outline")

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        outline_doc = [Document(page_content=outline,
                                metadata={'source': 'local'})]

        headings_subheadings = "".join(
            [doc.page_content for doc in outline_doc])

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            SERP_results = ""
        elif headings_subheadings:
            SERP_results = queryGoogle(headings_subheadings)
        else:
            SERP_results = ''

        SERP_doc = [Document(page_content=SERP_results,
                             metadata={'source': 'local'})]

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            summarized_SERP = ""
        elif SERP_doc:
            summarized_SERP = summarizeSERP(SERP_doc)
        else:
            variable = ""

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            descriptions = ""
        elif (isinstance(summarized_SERP, bool) or summarized_SERP):
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                descriptions = serpDescriber(summarized_SERP)
        else:
            descriptions = ""

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            updated_outline = ""
        elif (isinstance(descriptions, bool) or descriptions):
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                updated_outline = descriptionInserter(descriptions)
        else:
            updated_outline = ""

        if updated_outline is not None and len(updated_outline) > 0:
            st.markdown(updated_outline)
