import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime

st.set_page_config(
    page_title="Program Feedback",
    page_icon="📊",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📊 Program Feedback")

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

# Feedback form
st.markdown("## Feedback Form")
with st.form("feedback_form"):
    # Rating questions
    st.markdown("### Please rate the following aspects (1-5)")
    effectiveness = st.slider("Program Effectiveness", 1, 5, 3)
    experience = st.slider("Overall Experience", 1, 5, 3)
    support = st.slider("Support Received", 1, 5, 3)
    
    # Open-ended questions
    st.markdown("### Additional Feedback")
    strengths = st.text_area("What were the strengths of the program?")
    improvements = st.text_area("What could be improved?")
    comments = st.text_area("Additional comments or suggestions")
    
    # Submit button
    submitted = st.form_submit_button("Submit Feedback")
    
    if submitted:
        # Validate form
        if not all([strengths, improvements]):
            st.error("Please fill in all required fields")
        else:
            # Prepare feedback data
            feedback_data = {
                "program_id": st.session_state.selected_program_id,
                "effectiveness_rating": effectiveness,
                "experience_rating": experience,
                "support_rating": support,
                "strengths": strengths,
                "improvements": improvements,
                "comments": comments,
                "submission_date": datetime.now().isoformat()
            }
            
            # Submit feedback
            try:
                response = requests.post(
                    f"http://api:4000/api/v1/programs/{st.session_state.selected_program_id}/feedbacks",
                    json=feedback_data
                )
                if response.status_code == 201:
                    st.success("Feedback submitted successfully!")
                    st.balloons()
                    # Clear form
                    st.session_state.selected_program_id = None
                    st.switch_page("pages/02_Programs.py")
                else:
                    st.error("Failed to submit feedback")
            except Exception as e:
                st.error(f"Error submitting feedback: {str(e)}") 