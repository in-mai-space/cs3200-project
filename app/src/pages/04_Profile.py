import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="My Profile",
    page_icon="👤",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("👤 My Profile")

# Profile information form
with st.form("profile_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name", value=st.session_state.get('first_name', ''))
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
    
    with col2:
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        city = st.text_input("City")
        state = st.text_input("State")
        zip_code = st.text_input("ZIP Code")
    
    if st.form_submit_button("Update Profile"):
        st.success("Profile updated successfully!")