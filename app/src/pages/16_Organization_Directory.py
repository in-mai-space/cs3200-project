import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Browse Organizations")

search_term = st.text_input("Search by Organization Name")

try:
    if search_term:
        response = requests.get(f"http://api:4000/organizations?search={search_term}")
    else:
        response = requests.get("http://api:4000/organizations")

    if response.status_code == 200:
        orgs = response.json()
    else:
        st.error("Failed to fetch organizations")
        st.stop()
except Exception as e:
    st.error(f"Error connecting to backend: {e}")
    st.stop()

for org in orgs:
    with st.expander(org["name"]):
        st.write(f"**Location:** {org.get('location', 'N/A')}")
        st.write(f"**Contact:** {org.get('contact_email', 'N/A')}")
        st.write(f"**Description:** {org.get('description', 'No description provided')}")

        if st.button(f"View Programs - {org['id']}"):
            st.session_state["selected_org_id"] = org["id"]
            st.session_state["selected_org_name"] = org["name"]
            st.switch_page("pages/17_Program_Detail.py")
