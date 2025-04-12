import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Organization Settings",
    page_icon="⚙️",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("⚙️ Organization Settings")

# Organization profile
st.markdown("### Organization Profile")
with st.form("org_profile"):
    col1, col2 = st.columns(2)
    
    with col1:
        org_name = st.text_input("Organization Name", value="Example Organization")
        org_type = st.selectbox("Organization Type", ["Non-profit", "Government", "Educational", "Other"])
        website = st.text_input("Website", value="www.example.org")
        description = st.text_area("Description", value="This is an example organization")
    
    with col2:
        email = st.text_input("Contact Email", value="contact@example.org")
        phone = st.text_input("Phone Number", value="(555) 123-4567")
        address = st.text_area("Address", value="123 Organization Street")
    
    if st.form_submit_button("Update Profile"):
        st.success("Profile updated successfully!")

# Program settings
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