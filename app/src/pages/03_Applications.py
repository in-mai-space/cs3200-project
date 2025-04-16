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

# Get program details
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
st.markdown("### Program Details")
st.write(f"**Program:** {program['name']}")
st.write(f"**Organization:** {program['organization_name']}")

# Application form
st.markdown("### Application Form")
with st.form("application_form"):
    # Notes field
    notes = st.text_area("Additional Notes", help="Please provide any additional information that might help with your application")
    
    # Submit button
    submitted = st.form_submit_button("Submit Application")
    
    if submitted:
        try:
            # Prepare application data
            application_data = {
                "user_id": st.session_state.user_id,  # Assuming user_id is stored in session
                "status": "pending",  # Default status
                "notes": notes
            }
            
            # Submit application
            response = requests.post(
                f"http://api:4000/api/v1/programs/{st.session_state.selected_program_id}/applications",
                json=application_data
            )
            
            if response.status_code == 201:
                st.success("Application submitted successfully!")
                st.balloons()
                # Redirect to programs page after 2 seconds
                st.markdown("Redirecting to programs page...")
                st.markdown('<meta http-equiv="refresh" content="2;url=/pages/02_Programs.py">', unsafe_allow_html=True)
            else:
                st.error(f"Failed to submit application: {response.text}")
                
        except Exception as e:
            st.error(f"Error submitting application: {str(e)}") 