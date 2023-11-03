

import os
import streamlit as st
import tempfile
imports


function_defs
function_defs

function_defs


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
2. In the sidebar, input your OpenAI API Key in the text field labeled "OpenAI API Key". The placeholder should be "sk-...".
3. Enter your stop recording command in the text field labeled "Enter stop recording command". The command to stop recording is 'stop'.
4. The application will automatically stop recording when the stop command is received.
5. The application will check the status of your microphone. If your microphone is off, an error message will be displayed: "Your microphone is off. Please turn it on."
6. If the microphone is on and the recording is stopped, the application will save the audio.
7. If the audio is successfully saved, a success message will be displayed: "Audio has been saved successfully!".
'''""")


st.sidebar.markdown("# About")
st.sidebar.markdown("Talk, I Dare Ya! is a voice recorder application that utilizes your browser's microphone to record and save voice notes. It features real-time audio visualization using d3js and provides feedback if the microphone is off. The app allows you to start and stop voice recording at your convenience and save your recordings as mono 16 bit wav files.")

with st.form(key="form"):
    st.title('Talk, I Dare Ya!')
    stop_recording_command = st.text_input("Enter stop recording command")

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        remaining_code
        remaining_code
        if not microphone_status:
            st.error("Your microphone is off. Please turn it on.")
        remaining_code
        if saved_audio is not None:
            st.success("Audio has been saved successfully!")
