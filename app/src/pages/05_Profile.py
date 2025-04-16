import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime, date
from dateutil import parser

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

# Load existing user and profile data
try:
    # Get user data
    user_response = requests.get(f"http://api:4000/api/v1/users/{st.session_state.user_id}")
    if user_response.status_code == 200:
        user_data = user_response.json()
    else:
        st.error(f"Failed to load user data. Status code: {user_response.status_code}")
        st.stop()

    # Get user profile data
    profile_response = requests.get(f"http://api:4000/api/v1/user_profiles/{st.session_state.user_id}")
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
    else:
        st.error(f"Failed to load profile data. Status code: {profile_response.status_code}")
        st.stop()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Profile information form
with st.form("profile_form"):
    st.markdown("### Basic Information")
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name", value=user_data.get('first_name', ''))
        last_name = st.text_input("Last Name", value=user_data.get('last_name', ''))
    
    st.markdown("### Additional Information")
    col3, col4 = st.columns(2)
    
    with col3:
        dob_str = profile_data.get('date_of_birth')
        try:
            dob = parser.parse(dob_str).date()
        except Exception as e:
            dob = date(1990, 1, 1)

        date_of_birth = st.date_input("Date of Birth", value=dob)
        
        gender = st.text_input("Gender", value=profile_data.get('gender', ''))
        income = st.number_input("Income", value=profile_data.get('income', 0))
        education_level = st.text_input("Education Level", value=profile_data.get('education_level', ''))
    
    with col4:
        employment_status = st.text_input("Employment Status", value=profile_data.get('employment_status', ''))
        veteran_status = st.checkbox("Veteran Status", value=profile_data.get('veteran_status', False))
        disability_status = st.checkbox("Disability Status", value=profile_data.get('disability_status', False))
        ssn = st.text_input("SSN", value=profile_data.get('ssn', ''))
    
    submit_button = st.form_submit_button("Update Profile")
    
    if submit_button:
        try:
            # Update user data
            user_update = {
                "first_name": first_name,
                "last_name": last_name
            }
            user_response = requests.put(
                f"http://api:4000/api/v1/users/{st.session_state.user_id}",
                json=user_update
            )
            
            if user_response.status_code != 200:
                st.error(f"Failed to update user data. Status code: {user_response.status_code}")
                st.error(f"Response: {user_response.text}")
                st.stop()
            
            # Update user profile data
            profile_update = {
                "date_of_birth": date_of_birth.isoformat(),
                "gender": gender,
                "income": income,
                "education_level": education_level,
                "employment_status": employment_status,
                "veteran_status": veteran_status,
                "disability_status": disability_status,
                "ssn": ssn
            }
            profile_response = requests.put(
                f"http://api:4000/api/v1/user_profiles/{st.session_state.user_id}",
                json=profile_update
            )
            
            if profile_response.status_code != 200:
                st.error(f"Failed to update profile data. Status code: {profile_response.status_code}")
                st.error(f"Response: {profile_response.text}")
                st.error(f"Request data: {profile_update}")
                st.stop()
            
            st.success("Profile updated successfully!")
        except Exception as e:
            st.error(f"Error updating profile: {str(e)}")
            st.error(f"User update data: {user_update}")
            st.error(f"Profile update data: {profile_update}")