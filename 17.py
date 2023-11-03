

import os
import streamlit as st
import tempfile


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
2. In the sidebar, input your OpenAI API Key in the "OpenAI API Key" field.
3. In the "Enter start recording command" field, input your command to start recording.
4. The status of your recording will be displayed under the "Recording Status" section.
5. To stop the recording, input your command in the "Enter stop recording command" field. A warning message will be displayed indicating that the recording has been stopped.
6. Check the "Microphone status" checkbox if your microphone is on. If your microphone is off, a warning message will be displayed asking you to turn it on.
7. If you want to save the recording, check the "Do you want to save the recording?" checkbox. The status of the saved recording will be displayed under the "Recording saved" section.
'''""")


st.sidebar.markdown("# About")
st.sidebar.markdown("Talk, I Dare Ya! is a voice recording app that allows you to start and stop voice recordings, visualize audio streams in real-time, and save your recordings as mono 16 bit wav files. It also provides feedback if your microphone is off, ensuring a seamless recording experience.")

with st.form(key="form"):
    st.title('Talk, I Dare Ya!')
    start_command = st.text_input("Enter start recording command")

    stop_command = st.text_input("Enter stop recording command")

    microphone_status = st.checkbox("Microphone status")

    save_command = st.checkbox("Do you want to save the recording?")

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        if start_command is not None and len(str(start_command)) > 0:
            st.info(f"Recording Status: {start_command}")

        if stop_command:
            st.warning("Recording has been stopped.")

        if microphone_status == 'off':
            st.warning('Your microphone is off. Please turn it on.')

        if save_command is not None and len(str(save_command)) > 0:
            st.success(f"Recording saved: {save_command}")
