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

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑

2. Run the provided app code.

3. Fill in your preferences when prompted.

4. Wait for the chatbot to generate a response.

5. View the chat conversation with history displayed on the screen.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("🌟Special Genius is an educational platform that provides a personalized learning experience for students with special needs. By utilizing LLM technology, it understands each student's strengths, weaknesses, and preferred learning methods. With personalized learning modules, sensory-friendly content, and progress tracking, Special Genius creates an engaging and effective educational journey. It also offers specialized communication tools, parental insight reports, and integration with existing IEPs (Individualized Education Programs).")

st.title('Special Genius')
# Initiate a chat with the user to get the student's preferences
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if user_preferences := st.chat_input("Hi there! I'm here to help you with your preferences. Could you please let me know your preferences?"):
    with st.chat_message("user"):
        st.markdown(user_preferences)
    st.session_state.messages.append(
        {"role": "user", "content": user_preferences})
# Generate a response based on the user's input

msgs = StreamlitChatMessageHistory()


def generate_response(user_preferences):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'user_preferences'], template='''You are a chatbot. Generate a response based on the user's input.

{chat_history}
User: {user_preferences}
Chatbot:'''
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history", input_key="user_preferences", chat_memory=msgs, return_messages=True)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k",
                     openai_api_key=openai_api_key, temperature=0.7)
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory
    )

    return chat_llm_chain.run(user_preferences=user_preferences)


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    chat_response = ""
elif user_preferences:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        chat_response = generate_response(user_preferences)
else:
    chat_response = ""
# Display the chat conversation with history

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in chat_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})