import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Organization Settings",
    page_icon="⚙️",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("⚙️ Organization Settings")

st.markdown("### Program Settings")
with st.form("program_settings"):
    col1, col2 = st.columns(2)
    
    with col1:
        auto_approve = st.checkbox("Enable Auto-approval", value=False)
        notification_email = st.text_input("Notification Email", value="notifications@example.org")
    
    with col2:
        max_applications = st.number_input("Maximum Applications per Program", value=1000)
        review_period = st.number_input("Review Period (days)", value=30)
    
    if st.form_submit_button("Save Program Settings"):
        st.success("Program settings saved successfully!")