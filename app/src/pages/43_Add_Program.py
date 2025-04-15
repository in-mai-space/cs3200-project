import streamlit as st
import requests
from datetime import datetime, date

st.set_page_config(
    page_title="Add New Program",
    page_icon="➕",
    layout="wide"
)

st.title("Add New Program")
st.write("Fill out the form below to create a new program.")

with st.form("new_program_form"):
    # Organization ID is required since the endpoint URL ichancludes it.
    org_id = st.text_input("Organization ID", placeholder="Enter organization UUID")
    
    # Fields corresponding to the Program schema
    name = st.text_input("Program Name", placeholder="Enter program name")
    description = st.text_area("Description", placeholder="Enter program description")
    
    # Input dates and times
    start_date = st.date_input("Start Date", value=date.today())
    deadline_date = st.date_input("Deadline Date", value=date.today(), help="Select the date for the deadline")
    deadline_time = st.time_input("Deadline Time", value=datetime.now().time(), help="Select the time for the deadline")
    
    # End date is optional. User should enter in YYYY-MM-DD format if provided.
    end_date = st.text_input("End Date (optional)", placeholder="YYYY-MM-DD (leave blank if not applicable)")
    
    submitted = st.form_submit_button("Create Program")

if submitted:
    # Combine deadline date and time to create an ISO formatted string for the deadline.
    deadline = datetime.combine(deadline_date, deadline_time)
    
    # Prepare the payload matching the ProgramBaseSchema.
    payload = {
        "name": name,
        "description": description,
        "start_date": start_date.isoformat(),
        "deadline": deadline.isoformat(),
        "end_date": end_date.strip() if end_date.strip() else None,
    }
    
    api_url = "http://api:4000/api/v1/"
    endpoint = f"{api_url}organizations/{org_id}/programs"

    try:
        response = requests.post(endpoint, json=payload)
        if response.status_code == 201:
            st.success("Program created successfully!")
        else:
            st.error(f"Failed to create program. (Status code: {response.status_code})\nResponse: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
