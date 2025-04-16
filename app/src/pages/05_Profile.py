import streamlit as st
from modules.nav import SideBarLinks
import requests
import uuid

st.set_page_config(
    page_title="My Profile",
    page_icon="👤",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("👤 My Profile")

# Check if user is logged in
if 'user_id' not in st.session_state:
    st.error("Please log in to view your profile")
    st.stop()

# Load existing profile data
try:
    # Get user profile
    profile_response = requests.get(f"http://api:4000/api/v1/user_profiles/{st.session_state.user_id}")
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
    else:
        st.error("Failed to load profile data")
        st.stop()
except Exception as e:
    st.error(f"Error loading profile: {str(e)}")
    st.stop()

# Profile information form
with st.form("profile_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name", value=profile_data.get('first_name', ''))
        last_name = st.text_input("Last Name", value=profile_data.get('last_name', ''))
        email = st.text_input("Email", value=profile_data.get('email', ''))
    
    with col2:
        phone = st.text_input("Phone Number", value=profile_data.get('phone', ''))
        address = st.text_area("Address", value=profile_data.get('address', ''))
        city = st.text_input("City", value=profile_data.get('city', ''))
        state = st.text_input("State", value=profile_data.get('state', ''))
        zip_code = st.text_input("ZIP Code", value=profile_data.get('zip_code', ''))
    
    if st.form_submit_button("Update Profile"):
        try:
            # Update user data
            user_data = {
                "email": email
            }
            user_response = requests.put(
                f"http://api:4000/api/v1/users/{st.session_state.user_id}",
                json=user_data
            )
            
            # Update user profile data
            profile_data = {
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "address": address,
                "city": city,
                "state": state,
                "zip_code": zip_code
            }
            profile_response = requests.put(
                f"http://api:4000/api/v1/user_profiles/{st.session_state.user_id}",
                json=profile_data
            )
            
            if user_response.status_code == 200 and profile_response.status_code == 200:
                st.success("Profile updated successfully!")
            else:
                st.error("Failed to update profile")
        except Exception as e:
            st.error(f"Error updating profile: {str(e)}")