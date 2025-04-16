import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime

st.set_page_config(
    page_title="Program Feedback",
    page_icon="📝",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📝 Program Feedback")

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

# Feedback form
st.markdown("### Feedback Form")
with st.form("feedback_form"):
    # Title
    title = st.text_input("Feedback Title", help="A brief title for your feedback")
    
    # Rating sliders
    st.markdown("### Program Ratings")
    effectiveness = st.slider("Effectiveness", 1, 5, 3, help="How effective was the program?")
    experience = st.slider("Experience", 1, 5, 3, help="How was your overall experience?")
    simplicity = st.slider("Simplicity", 1, 5, 3, help="How simple was the application process?")
    recommendation = st.slider("Recommendation", 1, 5, 3, help="How likely are you to recommend this program to others?")
    
    # Improvement suggestions
    improvement = st.text_area(
        "Suggestions for Improvement",
        help="Please provide any suggestions for how the program could be improved"
    )
    
    # Submit button
    submitted = st.form_submit_button("Submit Feedback")
    
    if submitted:
        try:
            # Prepare feedback data
            feedback_data = {
                "user_id": st.session_state.user_id,  # Assuming user_id is stored in session
                "title": title,
                "effectiveness": effectiveness,
                "experience": experience,
                "simplicity": simplicity,
                "recommendation": recommendation,
                "improvement": improvement
            }
            
            # Submit feedback
            response = requests.post(
                f"http://api:4000/api/v1/programs/{st.session_state.selected_program_id}/feedbacks",
                json=feedback_data
            )
            
            if response.status_code == 201:
                st.success("Feedback submitted successfully!")
                st.balloons()
                # Redirect to programs page after 2 seconds
                st.markdown("Redirecting to programs page...")
                st.markdown('<meta http-equiv="refresh" content="2;url=/02_Programs.py">', unsafe_allow_html=True)
            else:
                st.error(f"Failed to submit feedback: {response.text}")
                
        except Exception as e:
            st.error(f"Error submitting feedback: {str(e)}") 