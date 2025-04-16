import streamlit as st
import requests
from datetime import datetime, date
from dateutil import parser

st.set_page_config(
    page_title="Edit Program",
    page_icon="✏️",
    layout="wide"
)

# Get program ID from session state
program_id = st.session_state.get('edit_program_id')

if not program_id:
    st.error("No program ID provided")
    st.stop()

st.title("✏️ Edit Program")

# Fetch program details
try:
    response = requests.get(f"http://api:4000/api/v1/programs/{program_id}")
    if response.status_code == 200:
        program = response.json()
    else:
        st.error(f"Failed to fetch program details. Status code: {response.status_code}")
        st.stop()
except Exception as e:
    st.error(f"Error fetching program details: {str(e)}")
    st.stop()

# Create form with current program details
with st.form("edit_program_form"):
    # Fields corresponding to the Program schema
    name = st.text_input("Program Name", value=program.get('name', ''))
    description = st.text_area("Description", value=program.get('description', ''))
    
    # Parse dates from the program data using dateutil.parser for more flexible parsing
    try:
        start_date = parser.parse(program.get('start_date', '')).date()
    except:
        start_date = date.today()
    
    try:
        deadline = parser.parse(program.get('deadline', ''))
        deadline_date = deadline.date()
        deadline_time = deadline.time()
    except:
        deadline_date = date.today()
        deadline_time = datetime.now().time()
    
    # Input dates and times with current values
    start_date = st.date_input("Start Date", value=start_date)
    deadline_date = st.date_input("Deadline Date", value=deadline_date)
    deadline_time = st.time_input("Deadline Time", value=deadline_time)
    
    # End date is optional
    try:
        end_date = parser.parse(program.get('end_date', '')).date() if program.get('end_date') else None
    except:
        end_date = None
    end_date = st.date_input("End Date (optional)", value=end_date)
    
    # Add submit button
    submitted = st.form_submit_button("Update Program")

if submitted:
    # Combine deadline date and time
    deadline = datetime.combine(deadline_date, deadline_time)
    
    # Prepare the payload
    payload = {
        "name": name,
        "description": description,
        "start_date": start_date.isoformat(),
        "deadline": deadline.isoformat(),
        "end_date": end_date.isoformat() if end_date else None,
    }
    
    try:
        response = requests.put(f"http://api:4000/api/v1/programs/{program_id}", json=payload)
        if response.status_code == 200:
            st.success("Program updated successfully!")
            # Clear the session state and go back to program management
            st.session_state.edit_program_id = None
            st.switch_page("pages/22_Program_Management.py")
        else:
            st.error(f"Failed to update program. Status code: {response.status_code}\nResponse: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}") 