import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

org_id = st.session_state.get("selected_org_id")
org_name = st.session_state.get("selected_org_name", "Unknown Organization")

st.title(f"Programs at {org_name}")

if not org_id:
    st.error("No organization selected.")
    st.stop()

response = requests.get(f"http://api:4000/organizations/{org_id}/programs")
if response.status_code != 200:
    st.error("Could not load programs.")
    st.stop()

programs = response.json()

for program in programs:
    with st.expander(program["name"]):
        st.write(f"**Description:** {program.get('description', 'No description provided')}")
        st.write(f"**Eligibility:** {program.get('eligibility', 'N/A')}")
        st.write(f"**Location:** {program.get('location', 'N/A')}")

        st.write("### Actions")

        if st.button(f"Apply - {program['id']}"):
            payload = {
                "user_id": 1,  # replace with session_state later
                "program_id": program["id"]
            }
            apply_response = requests.post("http://api:4000/applications", json=payload)
            if apply_response.status_code == 201:
                st.success("Application submitted!")
            else:
                st.error("Failed to apply.")

        feedback = st.text_area(f"Leave Feedback - {program['id']}", key=f"fb_{program['id']}")
        if st.button(f"Send Feedback - {program['id']}"):
            payload = {
                "user_id": 1,  # replace with session_state later
                "program_id": program["id"],
                "feedback": feedback
            }
            fb_response = requests.post("http://api:4000/feedbacks", json=payload)
            if fb_response.status_code == 201:
                st.success("Feedback sent!")
            else:
                st.error("Failed to send feedback.")
