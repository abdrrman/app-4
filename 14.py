

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


from langchain.docstore.document import Document


from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain


def faqGenerator(article_title):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to generate frequently asked questions from the given article title: '{article_title}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Based on the article title '{article_title}', please generate some frequently asked questions."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(article_title=article_title)
    return result  # returns string


def query_google(faq):
    search_input = "Query Google for the latest factual and relevant data for each question: {faq}".format(
        faq=faq)
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


def summarize_doc(google_doc):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")
    with st.spinner('DemoGPT is working on it. It might take 5-10 seconds...'):
        return chain.run(google_doc)


def markdownWriter(summarized_google_doc):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to write a longform article in markdown format using the summarized data from a Google document."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please write a 3000+ word article using the summarized data: '{summarized_google_doc}'. The article should be in markdown format."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(summarized_google_doc=summarized_google_doc)
    return result  # returns string


def seoOptimizer(longform_article):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an SEO expert. Your task is to optimize the given longform article for search engines."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please apply SEO optimizations to the following longform article: '{longform_article}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(longform_article=longform_article)
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
2. Input the title for the article in the text box labeled "Enter the title for the article".
3. The application will generate frequently asked questions based on the article title.
4. The application will then query Google for the latest factual and relevant data for each question.
5. The Google data is converted into a Document object.
6. The application will summarize the Google document.
7. The application will write a 3000+ word longform article in markdown format using the summarized Google data.
8. The application will apply SEO optimizations to the longform article.
9. The SEO optimized article will be displayed to the user.
'''""")


st.sidebar.markdown("# About")
st.sidebar.markdown("Know-It-All Writer is a comprehensive writing assistant that generates detailed, SEO-optimized longform articles. It uses the provided title to create relevant FAQs, conducts thorough internet research, and presents the information in a well-structured markdown format. The app also includes links to all sources used, ensuring transparency and credibility.")

with st.form(key="form"):
    st.title('Know-It-All Writer')
    article_title = st.text_input("Enter the title for the article")

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            faq = ""
        elif (isinstance(article_title, bool) or article_title):
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                faq = faqGenerator(article_title)
        else:
            faq = ""

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            google_data = ""
        elif faq:
            google_data = query_google(faq)
        else:
            google_data = ''

        google_doc = [Document(page_content=google_data,
                               metadata={'source': 'local'})]

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            summarized_google_doc = ""
        elif google_doc:
            summarized_google_doc = summarize_doc(google_doc)
        else:
            variable = ""

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            longform_article = ""
        elif (isinstance(summarized_google_doc, bool) or summarized_google_doc):
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                longform_article = markdownWriter(summarized_google_doc)
        else:
            longform_article = ""

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            seo_optimized_article = ""
        elif (isinstance(longform_article, bool) or longform_article):
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                seo_optimized_article = seoOptimizer(longform_article)
        else:
            seo_optimized_article = ""

        if seo_optimized_article is not None and len(str(seo_optimized_article)) > 0:
            st.text(seo_optimized_article)
