import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime

st.set_page_config(
    page_title="Program Application",
    page_icon="📝",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📝 Program Application")

# Check if program is selected
if 'selected_program_id' not in st.session_state:
    st.error("Please select a program first")
    st.stop()

# Load program details
try:
    response = requests.get(f"http://api:4000/api/v1/programs/{st.session_state.selected_program_id}")
    if response.status_code == 200:
        program = response.json()
    else:
        st.error("Failed to load program details")
        st.stop()
except Exception as e:
    st.error(f"Error loading program: {str(e)}")
    st.stop()

# Display program details
st.markdown("## Program Details")
st.write(f"**Program Name:** {program['name']}")
st.write(f"**Description:** {program['description']}")
st.write(f"**Organization:** {program['organization_name']}")
st.write(f"**Application Deadline:** {program['deadline']}")

# Application form
st.markdown("## Application Form")
with st.form("application_form"):
    # Personal Information
    st.markdown("### Personal Information")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    
    # Address
    st.markdown("### Address")
    street = st.text_input("Street Address")
    city = st.text_input("City")
    state = st.text_input("State")
    zip_code = st.text_input("ZIP Code")
    
    # Additional Information
    st.markdown("### Additional Information")
    qualifications = st.text_area("Qualifications")
    experience = st.text_area("Relevant Experience")
    motivation = st.text_area("Why do you want to participate in this program?")
    
    # Submit button
    submitted = st.form_submit_button("Submit Application")
    
    if submitted:
        # Validate form
        if not all([first_name, last_name, email, phone, street, city, state, zip_code, qualifications, experience, motivation]):
            st.error("Please fill in all required fields")
        else:
            # Prepare application data
            application_data = {
                "program_id": st.session_state.selected_program_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "street": street,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "qualifications": qualifications,
                "experience": experience,
                "motivation": motivation,
                "submission_date": datetime.now().isoformat()
            }
            
            # Submit application
            try:
                response = requests.post(
                    "http://api:4000/api/v1/applications",
                    json=application_data
                )
                if response.status_code == 201:
                    st.success("Application submitted successfully!")
                    st.balloons()
                    # Clear form
                    st.session_state.selected_program_id = None
                    st.switch_page("pages/02_Programs.py")
                else:
                    st.error("Failed to submit application")
            except Exception as e:
                st.error(f"Error submitting application: {str(e)}") 