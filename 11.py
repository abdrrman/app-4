

import os
import streamlit as st
import tempfile
imports


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


st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) above🔑
2. Enter the start date
3. Enter the end date
4. Enter the project name
5. Enter the task description
6. Enter the hours worked
7. Click on the "Generate Jira Timesheet" button
8. The generated Jira timesheet will be displayed to the user.""")


st.sidebar.markdown("# About")
st.sidebar.markdown("TimeSheet Genie! is a convenient website that helps you generate Jira timesheets effortlessly. Say goodbye to manual calculations and tedious data entry. With TimeSheet Genie!, you can easily track and record your work hours, ensuring accurate and efficient timesheet management.")

with st.form(key="form"):
    st.title('TimeSheet Genie!')
    start_date = st.date_input("Enter the start date")
    end_date = st.date_input("Enter the end date")
    project_name = st.text_input("Enter the project name")
    task_description = st.text_area("Enter the task description")
    hours_worked = st.number_input("Enter the hours worked", min_value=0.0)

    submit_button = st.form_submit_button(label='Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submit_button:

        remaining_code
        if jira_timesheet is not None and len(jira_timesheet) > 0:
            st.write(jira_timesheet)
