import streamlit as st
import requests
from datetime import datetime, date

st.set_page_config(
    page_title="Add Program",
    page_icon="➕",
    layout="wide"
)

# Get organization ID from session state
organization_id = st.session_state.get('add_program_org_id')

if not organization_id:
    st.error("No organization selected. Please go back to Program Management and select an organization.")
    st.stop()

st.title("➕ Add New Program")

# Create form for new program
with st.form("add_program_form"):
    # Display organization ID (read-only)
    st.text_input("Organization ID", value=organization_id, disabled=True)
    
    name = st.text_input("Program Name")
    description = st.text_area("Description")
    
    # Date inputs
    start_date = st.date_input("Start Date")
    deadline_date = st.date_input("Deadline Date")
    deadline_time = st.time_input("Deadline Time")
    end_date = st.date_input("End Date (optional)")
    
    submitted = st.form_submit_button("Create Program")

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
        response = requests.post(f"http://api:4000/api/v1/organizations/{organization_id}/programs", json=payload)
        if response.status_code == 201:
            st.success("Program created successfully!")
            # Clear the session state and go back to program management
            st.session_state.add_program_org_id = None
            st.switch_page("pages/22_Program_Management.py")
        else:
            st.error(f"Failed to create program. Status code: {response.status_code}\nResponse: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
