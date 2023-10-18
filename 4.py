
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
2. Run the provided app code.
3. Enter your message in the chat input.
4. Wait for the response from Elon Musk.
5. View the generated response in the chat interface.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("Elon 2.0: Be Musked! is an innovative app that allows you to experience being Elon Musk. With advanced AI technology, you can simulate Elon's decision-making process, explore his visionary ideas, and even interact with virtual versions of his colleagues and friends. Get ready to step into the shoes of one of the world's most influential entrepreneurs and change the future!")


st.title('Elon 2.0: Be Musked!')
# Get message from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if message := st.chat_input("Enter the message"):
    with st.chat_message("user"):
        st.markdown(message)
    st.session_state.messages.append({"role": "user", "content": message})
# Generate a response as if it's coming from Elon Musk

msgs = StreamlitChatMessageHistory()


def elon_musk_response(message):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'message'], template='''You are Elon Musk. Craft a response based on the given message.

{chat_history}
Message: {message}
Elon Musk:'''
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
    elon_response = ""
elif message:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        elon_response = elon_musk_response(message)
else:
    elon_response = ""
# Display the generated response to the user with chat interface

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in elon_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
