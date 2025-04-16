import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Feedback Management",
    page_icon="👥",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("🏢 Feedback Management")

# Initialize session state variables
if 'all_users' not in st.session_state:
    st.session_state.all_users = []
if 'user_page' not in st.session_state:
    st.session_state.user_page = 1
if 'all_programs' not in st.session_state:
    st.session_state.all_programs = []
if 'program_page' not in st.session_state:
    st.session_state.program_page = 1
if 'selected_program' not in st.session_state:
    st.session_state.selected_program = None
if 'feedback_forms' not in st.session_state:
    st.session_state.feedback_forms = []

# Function to load programs for dropdown
def load_programs():
    try:
        params = {
            'page': st.session_state.program_page,
            'limit': 100  # Load more at once for dropdown
        }
        response = requests.get("http://api:4000/api/v1/programs", params=params)
        if response.status_code == 200:
            new_programs = response.json()
            st.session_state.all_programs.extend(new_programs)
            st.session_state.program_page += 1
            return new_programs
        else:
            st.error(f"Failed to load programs: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error loading programs: {str(e)}")
        return []

# Function to load feedback forms for selected program
def load_feedback_forms(program_id):
    try:
        response = requests.get(f"http://api:4000/api/v1/programs/{program_id}/feedbacks")
        if response.status_code == 200:
            st.session_state.feedback_forms = response.json()
            return response.json()
        else:
            st.error(f"Failed to load feedback forms: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error loading feedback forms: {str(e)}")
        return []

# Function to load users for dropdown
def load_users():
    try:
        params = {
            'page': st.session_state.user_page,
            'limit': 100 
        }
        st.write(f"Loading users with params: {params}")  # Debug log
        response = requests.get("http://api:4000/api/v1/users", params=params)
        st.write(f"Response status code: {response.status_code}")  # Debug log
        
        if response.status_code == 200:
            new_users = response.json()
            st.write(f"Received users: {new_users}")  # Debug log
            
            if isinstance(new_users, list) and new_users:  # Check if we got a list of users
                # Only add users that aren't already in the list
                existing_ids = {user['id'] for user in st.session_state.all_users}
                unique_new_users = [user for user in new_users if user['id'] not in existing_ids]
                
                st.write(f"Existing users count: {len(st.session_state.all_users)}")  # Debug log
                st.write(f"New unique users count: {len(unique_new_users)}")  # Debug log
                
                if unique_new_users:
                    st.session_state.all_users.extend(unique_new_users)
                    st.session_state.user_page += 1
                    return unique_new_users
                else:
                    st.warning("No new users to load")
                    return []
            else:
                st.warning("No users found in the response")
                return []
        else:
            st.error(f"Failed to load users: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error loading users: {str(e)}")
        return []

# Load initial programs
if not st.session_state.all_programs:
    load_programs()

# Program selection with infinite scroll
st.markdown("### Select Program")
program_options = [f"{prog['name']} (ID: {prog['id']})" for prog in st.session_state.all_programs]
selected_program = st.selectbox(
    "Select a program to manage feedback forms",
    options=program_options if program_options else ["No programs available"],
    index=0
)

# Load more programs if we're near the end
if len(st.session_state.all_programs) > 0 and len(st.session_state.all_programs) % 100 == 0:
    load_programs()
    st.rerun()

if selected_program != "No programs available":
    # Get the selected program's data
    program_id = selected_program.split("(ID: ")[1].rstrip(")")
    program_data = next((prog for prog in st.session_state.all_programs if str(prog['id']) == program_id), None)
    
    if program_data:
        # Load feedback forms for the selected program
        feedback_forms = load_feedback_forms(program_id)
        
        # Display feedback forms
        if feedback_forms:
            st.markdown("### Feedback Forms")
            df = pd.DataFrame(feedback_forms)
            
            # Add a selectbox for feedback forms
            feedback_options = [f"{feedback['title']} (ID: {feedback['id']})" for feedback in feedback_forms]
            selected_feedback = st.selectbox(
                "Select a feedback form",
                options=[""] + feedback_options,
                index=0
            )
            
            if selected_feedback:
                # Get the selected feedback's data
                feedback_id = selected_feedback.split("(ID: ")[1].rstrip(")")
                feedback_data = next((feedback for feedback in feedback_forms if str(feedback['id']) == feedback_id), None)
                
                if feedback_data:
                    # Display feedback details
                    st.markdown("### Feedback Details")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Title:**", feedback_data['title'])
                        st.write("**Effectiveness Rating:**", feedback_data['effectiveness'])
                        st.write("**Experience Rating:**", feedback_data['experience'])
                    with col2:
                        st.write("**Simplicity Rating:**", feedback_data['simplicity'])
                        st.write("**Recommendation Rating:**", feedback_data['recommendation'])
                        st.write("**User ID:**", feedback_data['user_id'])
                    
                    st.write("**Areas for Improvement:**")
                    st.write(feedback_data['improvement'])
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Delete Feedback", type="secondary"):
                            try:
                                response = requests.delete(f"http://api:4000/api/v1/feedbacks/{feedback_id}")
                                if response.status_code == 200:
                                    st.success("Feedback form deleted successfully!")
                                    # Clear the feedback forms list to reload
                                    st.session_state.feedback_forms = []
                                    st.rerun()
                                else:
                                    st.error(f"Failed to delete feedback form. Status code: {response.status_code}")
                            except Exception as e:
                                st.error(f"An error occurred: {str(e)}")
            
        else:
            st.info("No feedback forms found for this program")
        
        # Add New Feedback Form Section
        st.markdown("### Add New Feedback Form")
        with st.form("add_feedback_form"):
            col1, col2 = st.columns(2)
            with col1:
                # User selection with infinite scroll
                st.markdown("### Select User")
                if st.session_state.all_users:
                    user_options = [f"{user['first_name']} {user['last_name']} (ID: {user['id']})" for user in st.session_state.all_users]
                    selected_user = st.selectbox(
                        "Select a user",
                        options=[""] + user_options,
                        index=0,
                        key="user_select"  # Add a unique key
                    )
                    
                    # Load more users if we're near the end
                    if len(st.session_state.all_users) > 0 and len(st.session_state.all_users) % 100 == 0:
                        load_users()
                        st.rerun()
                    
                    if selected_user and selected_user != "":
                        user_id = selected_user.split("(ID: ")[1].rstrip(")")
                    else:
                        user_id = ""
                else:
                    st.warning("No users available. Please try refreshing the page.")
                    user_id = ""
                
                title = st.text_input("Feedback Form Title", help="Required")
            with col2:
                effectiveness = st.number_input("Effectiveness", min_value=1, max_value=5, help="How effective was the program?")
                experience = st.number_input("Experience", min_value=1, max_value=5, help="How was your overall experience?")
            
            col3, col4 = st.columns(2)
            with col3:
                simplicity = st.number_input("Simplicity", min_value=1, max_value=5, help="How simple was the program to understand?")
            with col4:
                recommendation = st.number_input("Recommendation", min_value=1, max_value=5, help="Would you recommend this program?")
            
            improvement = st.text_area("Areas for Improvement", help="Required")
            
            submitted = st.form_submit_button("Create Feedback Form")
        
        if submitted:
            # Validate required fields
            if not user_id or not title or not improvement:
                st.error("Please fill in all required fields")
            else:
                # Prepare the payload
                payload = {
                    "user_id": user_id,
                    "title": title,
                    "effectiveness": effectiveness,
                    "experience": experience,
                    "simplicity": simplicity,
                    "recommendation": recommendation,
                    "improvement": improvement
                }
                
                try:
                    response = requests.post(f"http://api:4000/api/v1/programs/{program_id}/feedbacks", json=payload)
                    if response.status_code == 201:
                        st.markdown("""
                            <div style='background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; text-align: center;'>
                                <i class='fas fa-check-circle'></i> Feedback form created successfully!
                            </div>
                        """, unsafe_allow_html=True)
                        # Clear the feedback forms list to reload
                        st.session_state.feedback_forms = []
                        st.rerun()
                    else:
                        st.error(f"Failed to create feedback form. Status code: {response.status_code}\nResponse: {response.text}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please select a program to manage feedback forms")

# Load initial users if not already loaded
if not st.session_state.all_users:
    st.write("Loading initial users...")  # Debug log
    load_users()
    st.write(f"Total users after initial load: {len(st.session_state.all_users)}")  # Debug log