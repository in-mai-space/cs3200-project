import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Add New Application",
    page_icon="➕",
    layout="wide"
)

st.title("Add New Application")
st.write("Fill out the form below to create a new application.")

with st.form("add_application_form"):
    user_id = st.text_input(
        "User ID",
        placeholder="Enter the user’s UUID",
        help="Must be a 36‑character UUID"
    )
    program_id = st.text_input(
        "Program ID",
        placeholder="Enter the program’s UUID",
        help="Must be a 36‑character UUID"
    )
    status = st.selectbox(
        "Status",
        ['draft', 'submitted', 'under_review',
         'additional_info_needed', 'approved',
         'rejected', 'waitlisted', 'withdrawn'],
        index=0
    )
    qualification_status = st.selectbox(
        "Qualification Status",
        ['pending', 'verified', 'incomplete', 'rejected'],
        index=0
    )
    decision_date = st.date_input(
        "Decision Date (optional)",
        help="If you have one, otherwise leave as-is"
    )
    decision_notes = st.text_area(
        "Decision Notes (optional)",
        help="Any extra notes about the decision"
    )
    submitted = st.form_submit_button("Create Application")

if submitted:
    # build the payload
    payload = {
        "user_id": user_id,
        "status": status,
        "qualification_status": qualification_status,
    }

    if decision_date:
        payload["decision_date"] = datetime.combine(decision_date, datetime.min.time()).isoformat()
    if decision_notes:
        payload["decision_notes"] = decision_notes

    # call Flask API
    api_url = f"http://api:4000/api/v1/applications/programs/{program_id}/applications"
    try:
        resp = requests.post(api_url, json=payload)
        if resp.status_code == 201:
            st.success("✅ Application created successfully!")
        else:
            st.error(
                f"Failed to create application. "
                f"Status code: {resp.status_code}\nResponse: {resp.text}"
            )
    except Exception as e:
        st.error(f"An error occurred: {e}")
