import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(
    page_title="Organization Programs",
    page_icon="📋",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📋 Organization Programs")

# Constants
PAGE_SIZE = 20

# Initialize session state
if 'all_programs' not in st.session_state:
    st.session_state.all_programs = []
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'has_more' not in st.session_state:
    st.session_state.has_more = True
if 'selected_program' not in st.session_state:
    st.session_state.selected_program = None
if 'view' not in st.session_state:
    st.session_state.view = None

# Check if organization ID is set
if 'selected_organization_id' not in st.session_state:
    st.error("No organization selected. Please select an organization from the role selection page.")
    st.stop()

# Clear cached data if coming from edit or create page
if ('from_edit_page' in st.session_state and st.session_state.from_edit_page) or \
   ('from_create_page' in st.session_state and st.session_state.from_create_page):
    st.session_state.all_programs = []
    st.session_state.page = 1
    st.session_state.has_more = True
    st.session_state.from_edit_page = False
    st.session_state.from_create_page = False
    st.rerun()

# Search and filter
search_query = st.text_input("Search programs")

# Reset programs when search changes
if 'last_search_query' not in st.session_state:
    st.session_state.last_search_query = search_query
elif st.session_state.last_search_query != search_query:
    st.session_state.all_programs = []
    st.session_state.page = 1
    st.session_state.has_more = True
    st.session_state.last_search_query = search_query

def load_more_programs():
    try:
        params = {
            'page': st.session_state.page,
            'limit': PAGE_SIZE,
            'search_query': search_query if search_query else None
        }

        response = requests.get(
            f"http://api:4000/api/v1/organizations/{st.session_state.selected_organization_id}/programs",
            params=params
        )

        if response.status_code == 200:
            new_programs = response.json()
            if new_programs:
                st.session_state.all_programs.extend(new_programs)
                st.session_state.page += 1
                st.session_state.has_more = len(new_programs) == PAGE_SIZE
            else:
                st.session_state.has_more = False
    except Exception as e:
        st.error(f"Error loading programs: {str(e)}")

# Load initial programs if needed
if not st.session_state.all_programs and st.session_state.has_more:
    load_more_programs()

# Program list
st.markdown("### Program List")
if st.session_state.all_programs:
    # Create a DataFrame for the program list
    program_data = {
        "Program Name": [p['name'] for p in st.session_state.all_programs],
        "Status": [p['status'] for p in st.session_state.all_programs],
        "Start Date": [p['start_date'] for p in st.session_state.all_programs],
        "Deadline": [p['deadline'] for p in st.session_state.all_programs],
        "End Date": [p['end_date'] for p in st.session_state.all_programs]
    }
    df = pd.DataFrame(program_data)
    st.dataframe(df, use_container_width=True)
    
    # Auto-load more programs when reaching the bottom
    if st.session_state.has_more:
        load_more_programs()
        st.rerun()
else:
    st.info("No programs found")

# Program actions
st.markdown("### Program Actions")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Add New Program", type='primary', use_container_width=True):
        st.switch_page("pages/36_Create_Program.py")
with col2:
    if st.button("Edit Program", type='primary', use_container_width=True):
        if st.session_state.selected_program:
            st.session_state.edit_program_id = st.session_state.selected_program['id']
            st.switch_page("pages/35_Edit_Program.py")
        else:
            st.warning("Please select a program to edit")
with col3:
    if st.button("Delete Program", type='secondary', use_container_width=True):
        if st.session_state.selected_program:
            if st.button("Confirm Delete", type='primary', key='confirm_delete'):
                try:
                    response = requests.delete(
                        f"http://api:4000/api/v1/programs/{st.session_state.selected_program['id']}"
                    )
                    if response.status_code == 200:
                        st.success("Program deleted successfully!")
                        # Reset the program list
                        st.session_state.all_programs = []
                        st.session_state.page = 1
                        st.session_state.has_more = True
                        st.rerun()
                    else:
                        st.error(f"Failed to delete program. (Status code: {response.status_code})")
                except Exception as e:
                    st.error(f"Error deleting program: {str(e)}")
        else:
            st.warning("Please select a program to delete")

# Program details and additional views
if st.session_state.all_programs:
    # Program selection
    program_options = [f"{p['name']} - {p['status']}" for p in st.session_state.all_programs]
    selected_program_name = st.selectbox(
        "Select a program to view details",
        options=program_options,
        index=0
    )
    
    # Find the selected program
    selected_program = next(
        (p for p in st.session_state.all_programs if f"{p['name']} - {p['status']}" == selected_program_name),
        None
    )
    
    if selected_program:
        st.session_state.selected_program = selected_program
        st.session_state.edit_program_id = selected_program['id']  # Set the program ID in session state
        
        # Program details
        with st.expander("Program Details"):
            st.write(f"**Program Name:** {selected_program['name']}")
            st.write(f"**Description:** {selected_program['description']}")
            st.write(f"**Status:** {selected_program['status']}")
            st.write(f"**Start Date:** {selected_program['start_date']}")
            st.write(f"**Deadline:** {selected_program['deadline']}")
            st.write(f"**End Date:** {selected_program['end_date']}")
        
        # Additional views
        st.markdown("### Additional Views")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("View Applications", type='secondary', use_container_width=True):
                st.session_state.view = 'applications'
        with col2:
            if st.button("View Feedbacks", type='secondary', use_container_width=True):
                st.session_state.view = 'feedbacks'
        with col3:
            if st.button("View Feedback Stats", type='secondary', use_container_width=True):
                st.session_state.view = 'feedback_stats'
        with col4:
            if st.button("View User Profiles", type='secondary', use_container_width=True):
                st.session_state.view = 'profiles'
        
        # Selected view content
        if st.session_state.view:
            if st.session_state.view == 'applications':
                if 'all_applications' not in st.session_state:
                    st.session_state.all_applications = []
                if 'app_page' not in st.session_state:
                    st.session_state.app_page = 1
                
                def load_more_applications():
                    try:
                        response = requests.get(
                            f"http://api:4000/api/v1/programs/{selected_program['id']}/applications",
                            params={'page': st.session_state.app_page, 'limit': PAGE_SIZE}
                        )
                        if response.status_code == 200:
                            new_applications = response.json()
                            if new_applications:
                                st.session_state.all_applications.extend(new_applications)
                                st.session_state.app_page += 1
                                return len(new_applications) == PAGE_SIZE
                    except Exception as e:
                        st.error(f"Error loading applications: {str(e)}")
                    return False
                
                if not st.session_state.all_applications:
                    load_more_applications()
                
                if st.session_state.all_applications:
                    df = pd.DataFrame(st.session_state.all_applications)
                    st.markdown("### Applications")
                    st.dataframe(df, use_container_width=True)
                    
                    if load_more_applications():
                        st.rerun()
                else:
                    st.info("No applications found for this program")
            
            elif st.session_state.view == 'feedbacks':
                if 'all_feedbacks' not in st.session_state:
                    st.session_state.all_feedbacks = []
                if 'feedback_page' not in st.session_state:
                    st.session_state.feedback_page = 1
                
                def load_more_feedbacks():
                    try:
                        response = requests.get(
                            f"http://api:4000/api/v1/programs/{selected_program['id']}/feedbacks",
                            params={'page': st.session_state.feedback_page, 'limit': PAGE_SIZE}
                        )
                        if response.status_code == 200:
                            new_feedbacks = response.json()
                            if new_feedbacks:
                                st.session_state.all_feedbacks.extend(new_feedbacks)
                                st.session_state.feedback_page += 1
                                return len(new_feedbacks) == PAGE_SIZE
                    except Exception as e:
                        st.error(f"Error loading feedbacks: {str(e)}")
                    return False
                
                if not st.session_state.all_feedbacks:
                    load_more_feedbacks()
                
                if st.session_state.all_feedbacks:
                    df = pd.DataFrame(st.session_state.all_feedbacks)
                    st.markdown("### Feedback Details")
                    st.dataframe(df, use_container_width=True)
                    
                    if load_more_feedbacks():
                        st.rerun()
                else:
                    st.info("No feedbacks found for this program")
            
            elif st.session_state.view == 'feedback_stats':
                try:
                    response = requests.get(f"http://api:4000/api/v1/programs/{selected_program['id']}/feedbacks/stats")
                    if response.status_code == 200:
                        stats = response.json()
                        st.markdown("### Feedback Statistics")
                        
                        if stats:
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Total Feedback", str(stats['total_feedback']))
                            with col2:
                                st.metric("Avg Effectiveness", str(round(float(stats['avg_effectiveness']), 1)))
                            with col3:
                                st.metric("Avg Simplicity", str(round(float(stats['avg_simplicity']), 1)))
                            with col4:
                                st.metric("Avg Experience", str(round(float(stats['avg_experience']), 1)))
                        else:
                            st.info("No feedback statistics available")
                    else:
                        st.error("Failed to fetch feedback statistics")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            elif st.session_state.view == 'profiles':
                if 'all_profiles' not in st.session_state:
                    st.session_state.all_profiles = []
                if 'profile_page' not in st.session_state:
                    st.session_state.profile_page = 1
                
                def load_more_profiles():
                    try:
                        response = requests.get(
                            f"http://api:4000/api/v1/programs/{selected_program['id']}/profiles",
                            params={'page': st.session_state.profile_page, 'limit': PAGE_SIZE}
                        )
                        if response.status_code == 200:
                            new_profiles = response.json()
                            if new_profiles:
                                st.session_state.all_profiles.extend(new_profiles)
                                st.session_state.profile_page += 1
                                return len(new_profiles) == PAGE_SIZE
                    except Exception as e:
                        st.error(f"Error loading profiles: {str(e)}")
                    return False
                
                if not st.session_state.all_profiles:
                    load_more_profiles()
                
                if st.session_state.all_profiles:
                    df = pd.DataFrame(st.session_state.all_profiles)
                    st.markdown("### User Profiles")
                    st.dataframe(df, use_container_width=True)
                    
                    if load_more_profiles():
                        st.rerun()
                else:
                    st.info("No profiles found for this program") 