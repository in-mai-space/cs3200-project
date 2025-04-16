import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Your Profile")

USER_ID = 1

response = requests.get(f"http://api:4000/users/{USER_ID}")
if response.status_code == 200:
    user = response.json()
else:
    st.error("Failed to load profile")
    st.stop()

with st.form("edit_profile_form"):
    name = st.text_input("Full Name", user.get("name", ""))
    email = st.text_input("Email", user.get("email", ""))
    phone = st.text_input("Phone", user.get("phone", ""))
    address = st.text_input("Address", user.get("address", ""))

    submitted = st.form_submit_button("Save Changes")
    if submitted:
        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address
        }
        update_response = requests.put(f"http://api:4000/users/{USER_ID}", json=payload)
        if update_response.status_code == 200:
            st.success("Profile updated successfully!")
        else:
            st.error("Failed to update profile.")
