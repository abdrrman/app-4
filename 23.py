

import os
import streamlit as st
import tempfile


from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)


def contentPlanner(content_type, message, schedule, task_breakdown, time_management):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are a content planner. Your task is to generate ideas and outlines for the content of type '{content_type}', with the message '{message}', following the schedule '{schedule}', task breakdown '{task_breakdown}', and time management '{time_management}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please generate ideas and an outline for a {content_type} with the message '{message}', following the schedule '{schedule}', task breakdown '{task_breakdown}', and time management '{time_management}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(content_type=content_type, message=message, schedule=schedule,
                       task_breakdown=task_breakdown, time_management=time_management)
    return result  # returns string


def scriptGenerator(content_type, message, ideas_outlines):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are a scriptwriter. Your task is to generate a script for the given content type: '{content_type}', using the message: '{message}' and the ideas/outlines: '{ideas_outlines}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please generate a script for a {content_type} with the message: '{message}' and the following ideas/outlines: '{ideas_outlines}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(content_type=content_type,
                       message=message, ideas_outlines=ideas_outlines)
    return result  # returns string


def contentGenerator(content_type, message, ideas_outlines, script):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to generate a {content_type} from the given message, ideas, and script."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """The message is: '{message}', the ideas and outlines are: '{ideas_outlines}', and the script is: '{script}'. Please generate a {content_type} based on these inputs."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(content_type=content_type, message=message,
                       ideas_outlines=ideas_outlines, script=script)
    return result  # returns string


def contentPlanner(content_type, schedule):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are a content planner. Your task is to plan a content schedule for the given content type and schedule."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """The content type is {content_type} and the schedule is {schedule}. Please plan a content schedule based on these inputs."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(content_type=content_type, schedule=schedule)
    return result  # returns string


def contentTaskBreakdown(content_type, task_breakdown):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant designed to breakdown tasks for creating content. The content type is '{content_type}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """The task breakdown is as follows: {task_breakdown}. Please provide a detailed breakdown of these tasks."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(content_type=content_type,
                       task_breakdown=task_breakdown)
    return result  # returns string


def timeManager(content_type, time_management):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are a time management assistant. Your task is to manage time for the given content type: '{content_type}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """The content type is {content_type}. Please manage the time according to the following time management strategy: {time_management}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(content_type=content_type,
                       time_management=time_management)
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
2. Input the type of content you want to create.
3. Write down the message you want to convey through your content.
4. Specify the schedule for your content creation process.
5. Break down the tasks involved in your content creation process.
6. Describe how you plan to manage your time during the content creation process.
7. Once all inputs are filled, the application will generate ideas and outlines for your content.
8. The generated ideas and outlines will be displayed for your review.
9. The application will then generate a script for your content based on the provided inputs.
10. The generated script will be displayed for your review.
11. The application will then generate a blog post or article based on the provided inputs.
12. The generated blog post or article will be displayed for your review.
13. The application will also plan a content schedule based on your inputs.
14. The planned content schedule will be displayed for your review.
15. The application will break down the content tasks based on your inputs.
16. The broken down tasks will be displayed for your review.
17. The application will manage the time for the content based on your inputs.
18. The time management plan will be displayed for your review.

'''""")


st.sidebar.markdown("# About")
st.sidebar.markdown("VideoGenius, Not! is a comprehensive content mentor for YouTube creators. It assists in generating ideas, writing scripts, creating blog posts/articles, planning content schedules, and managing content tasks and time effectively. It's your all-in-one solution for content creation and management.")

with st.form(key="form"):
    st.title('VideoGenius, Not!')
    content_type = st.selectbox("Select the content type", [
                                "Text", "Image", "Video", "Audio"])
    message = st.text_input("Enter your message")
    schedule = st.date_input("Select the schedule")
    task_breakdown = st.text_area("Enter task breakdown")
    time_management = st.text_input("Enter your time management strategy")

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            ideas_outlines = ""
        elif (isinstance(content_type, bool) or content_type) and (isinstance(message, bool) or message) and (isinstance(schedule, bool) or schedule) and (isinstance(task_breakdown, bool) or task_breakdown) and (isinstance(time_management, bool) or time_management):
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                ideas_outlines = contentPlanner(
                    content_type, message, schedule, task_breakdown, time_management)
        else:
            ideas_outlines = ""

        for idea in ideas_outlines:
            if idea is not None and len(str(idea)) > 0:
                st.info(idea)

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            script = ""
        elif (isinstance(content_type, bool) or content_type) and (isinstance(message, bool) or message) and (isinstance(ideas_outlines, bool) or ideas_outlines):
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                script = scriptGenerator(content_type, message, ideas_outlines)
        else:
            script = ""

        if script is not None and len(str(script)) > 0:
            st.text(script)

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            blog_post = ""
        elif (isinstance(content_type, bool) or content_type) and (isinstance(message, bool) or message) and (isinstance(ideas_outlines, bool) or ideas_outlines) and (isinstance(script, bool) or script):
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                blog_post = contentGenerator(
                    content_type, message, ideas_outlines, script)
        else:
            blog_post = ""

        if blog_post is not None and len(str(blog_post)) > 0:
            st.markdown(blog_post)

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            content_schedule = ""
        elif (isinstance(content_type, bool) or content_type) and (isinstance(schedule, bool) or schedule):
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                content_schedule = contentPlanner(content_type, schedule)
        else:
            content_schedule = ""

        if content_schedule is not None and len(content_schedule) > 0:
            st.markdown(content_schedule)

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            content_tasks = ""
        elif (isinstance(content_type, bool) or content_type) and (isinstance(task_breakdown, bool) or task_breakdown):
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                content_tasks = contentTaskBreakdown(
                    content_type, task_breakdown)
        else:
            content_tasks = ""

        for task in content_tasks:
            st.text(task)

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            time_plan = ""
        elif (isinstance(content_type, bool) or content_type) and (isinstance(time_management, bool) or time_management):
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                time_plan = timeManager(content_type, time_management)
        else:
            time_plan = ""

        if time_plan is not None and len(time_plan) > 0:
            st.text(time_plan)
