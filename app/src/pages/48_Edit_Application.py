import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Edit Application",
    page_icon="✏️",
    layout="wide"
)

st.title("Edit Application")
st.write("Fill out the form below to update an existing application.")

with st.form("edit_application_form"):
    application_id = st.text_input(
        "Application ID",
        placeholder="Enter the application’s UUID",
        help="Must be a 36‑character UUID"
    )
    user_id = st.text_input(
        "User ID",
        placeholder="Enter the user’s UUID",
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
        help="Leave as today and we’ll convert it, or change if needed"
    )
    decision_notes = st.text_area(
        "Decision Notes (optional)",
        help="Any extra notes about the decision"
    )
    submitted = st.form_submit_button("Update Application")

if submitted:
    if not application_id:
        st.error("❗️ You must provide an Application ID.")
    else:
        payload = {
            "user_id": user_id,
            "status": status,
            "qualification_status": qualification_status,
        }
        if decision_date:
            payload["decision_date"] = datetime.combine(decision_date, datetime.min.time()).isoformat()
        if decision_notes:
            payload["decision_notes"] = decision_notes

        api_url = f"http://api:4000/api/v1/applications/{application_id}"
        try:
            resp = requests.put(api_url, json=payload)
            if resp.status_code == 200:
                st.success("✅ Application updated successfully!")
            else:
                st.error(
                    f"Failed to update application.\n"
                    f"Status code: {resp.status_code}\nResponse: {resp.text}"
                )
        except Exception as e:
            st.error(f"An error occurred: {e}")
