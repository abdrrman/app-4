
import time
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import streamlit as st
import tempfile


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) above🔑
2. Run the code provided.
3. Enter your message in the chat input.
4. Wait for the Trump-style response to be generated.
5. View the generated response in the chat history.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("Trump Talk is an app that allows you to generate text that mimics the speaking style of former President Donald Trump. With just a few clicks, you can create Trump-like statements and speeches for various purposes.")


st.title('Trump Talk')
# Get message from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if message := st.chat_input("Enter the message"):
    with st.chat_message("user"):
        st.markdown(message)
    st.session_state.messages.append({"role": "user", "content": message})
# Generate a response in the style of Trump

msgs = StreamlitChatMessageHistory()


def trump_style_response(message):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'message'], template='''You are a chatbot imitating the style of Donald Trump. Generate a response in his style.

{chat_history}
Human: {message}
Trump:'''
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history", input_key="message", chat_memory=msgs, return_messages=True)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k",
                     openai_api_key=openai_api_key, temperature=0.7)
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory
    )

    return chat_llm_chain.run(message=message)


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    trump_response = ""
elif (isinstance(message, bool) or message):
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        trump_response = trump_style_response(message)
else:
    trump_response = ""
# Display the generated Trump response to the user

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in trump_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
