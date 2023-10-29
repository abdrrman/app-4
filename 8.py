

import os
import streamlit as st
import tempfile


from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)


from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chains import LLMMathChain
from langchain.callbacks import StreamlitCallbackHandler


def searchStringCombiner(search_prompt, filters):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant designed to combine a search prompt and filters into a single string."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Combine the search prompt '{search_prompt}' with the filters {filters} into a single string."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(search_prompt=search_prompt, filters=filters)
    return result  # returns string


def search_products(search_query):
    search_input = "Use the combined search query to find the products: {search_query}".format(
        search_query=search_query)
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


st.sidebar.markdown("""'''
# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) above🔑

2. In the sidebar, you will find a text input field labeled "OpenAI API Key". Enter your OpenAI API key here.

3. In the main application window, you will find a text input field labeled "Enter search prompt". Enter your desired search term here.

4. Below the search prompt input, you will find a multi-select field labeled "Select filters". You can select one or more filters from the dropdown list.

5. After entering the search prompt and selecting the filters, the application will combine these into a single search string. This process is handled by the `searchStringCombiner` function.

6. If the OpenAI API key is valid and the search prompt and filters are provided, the application will start processing your request. You will see a spinner with the message 'DemoGPT is working on it. It takes less than 10 seconds...'.

7. The combined search query is then used to search for products. This is handled by the `search_products` function.

8. If the OpenAI API key is valid and the search query is provided, the application will start searching for products.

9. Once the products are found, they will be displayed in the main application window.

Please note that the application requires a valid OpenAI API key to function properly. If the key is not provided or is incorrect, you will see a warning message.
'''""")


st.sidebar.markdown("# About")
st.sidebar.markdown("Shop n Oops! is a unique discovery platform designed for direct-to-consumer brands. It offers a comprehensive search functionality, product listing, and filtration system. Users can search with a prompt and receive a curated list of ideal products complete with images, descriptions, ratings, prices, and personalized recommendations.")

with st.form(key="form"):
    st.title('Shop n Oops!')
    search_prompt = st.text_input("Enter search prompt")
    filters = st.multiselect(
        "Select filters", ["Filter 1", "Filter 2", "Filter 3", "Filter 4", "Filter 5"])

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            search_query = ""
        elif (isinstance(search_prompt, bool) or search_prompt) and (isinstance(filters, bool) or filters):
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                search_query = searchStringCombiner(search_prompt, filters)
        else:
            search_query = ""

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            product_list = ""
        elif search_query:
            product_list = search_products(search_query)
        else:
            product_list = ''

        if product_list is not None and len(product_list) > 0:
            st.write(product_list)
