import streamlit as st
import requests
from datetime import datetime, date

# Set page configuration for the Edit Application page.
st.set_page_config(
    page_title="Edit Application",
    page_icon="✏️",
    layout="wide"
)

st.title("Edit Application")
st.write("Update the application details below and submit to update the application in the database.")

with st.form("edit_application_form"):
    application_id = st.text_input("Application ID", placeholder="Enter application UUID")
    
    user_id = st.text_input("User ID", placeholder="Enter user UUID")
    program_id = st.text_input("Program ID", placeholder="Enter program UUID")
    
    status_options = ['draft', 'submitted', 'under_review', 'additional_info_needed', 'approved', 'rejected', 'waitlisted', 'withdrawn']
    status = st.selectbox("Status", options=status_options)
    
    qualification_options = ['pending', 'verified', 'incomplete', 'rejected']
    qualification_status = st.selectbox("Qualification Status", options=qualification_options)
    
    decision_date = st.date_input("Decision Date", value=date.today(), help="Select the decision date")
    decision_notes = st.text_area("Decision Notes", placeholder="Enter any decision notes here")
    
    submitted = st.form_submit_button("Update Application")

if submitted:
    # Constructs the payload that the update endpoint expects.
    payload = {
        "user_id": user_id,
        "program_id": program_id,
        "status": status,
        "qualification_status": qualification_status,
        "decision_date": decision_date.isoformat() if decision_date else None,
        "decision_notes": decision_notes
    }
    
    api_url = f"http://api:4000/api/v1/applications/applications/{application_id}"
    
    try:
        # Send the PUT request with the payload.
        response = requests.put(api_url, json=payload)
        
        if response.status_code == 200:
            st.success("Application updated successfully!")
        else:
            st.error(f"Failed to update application. (Status code: {response.status_code})\nResponse: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
