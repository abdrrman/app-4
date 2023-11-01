

import os
import streamlit as st
import tempfile

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chains import LLMMathChain
from langchain.callbacks import StreamlitCallbackHandler


def search_news(keywords):
    search_input = "Search for news related to the keywords: {keywords}".format(
        keywords=keywords)
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
2. Enter keywords in the text input field.
3. Click on the "Search" button to search for news related to the keywords.
4. The news results will be displayed below the search button.""")


st.sidebar.markdown("# About")
st.sidebar.markdown("🔍Keyword Krazed is a news monitoring dashboard that helps you stay updated on the latest news by tracking keywords of your choice. Stay informed and never miss out on important information.")

with st.form(key="form"):
    st.title('Keyword Krazed')
    keywords = st.text_input("Enter keywords")

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            news_results = ""
        elif keywords:
            news_results = search_news(keywords)
        else:
            news_results = ''

        if news_results is not None and len(news_results) > 0:
            st.write(news_results)
