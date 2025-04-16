import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Browse Programs",
    page_icon="📋",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📋 Available Programs")

# Check if organization is selected
if 'selected_organization_id' not in st.session_state:
    st.error("Please select an organization first")
    st.stop()

# Initialize session state for programs
if 'all_programs' not in st.session_state:
    st.session_state.all_programs = []
    st.session_state.page = 1
    st.session_state.has_more = True
    st.session_state.last_search_query = ""

# Search section
search_query = st.text_input("Search programs by name")

# Reset programs when search changes
if search_query != st.session_state.last_search_query:
    st.session_state.all_programs = []
    st.session_state.page = 1
    st.session_state.has_more = True
    st.session_state.last_search_query = search_query

def load_more_programs():
    try:
        params = {
            'page': st.session_state.page,
            'limit': 10
        }
        
        # Only add search_query if it's not empty
        if search_query and search_query.strip():
            params['search_query'] = search_query.strip()
            
        response = requests.get(
            "http://api:4000/api/v1/programs",
            params=params
        )
        
        if response.status_code == 200:
            new_programs = response.json()
            
            if isinstance(new_programs, list):
                if new_programs:
                    st.session_state.all_programs.extend(new_programs)
                    st.session_state.page += 1
                    st.session_state.has_more = len(new_programs) == 10
                else:
                    st.session_state.has_more = False
            else:
                st.error("Invalid response format from API")
        else:
            st.error(f"API returned status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error loading programs: {str(e)}")

# Load initial programs if needed
if not st.session_state.all_programs and st.session_state.has_more:
    load_more_programs()

# Programs list
st.markdown("## Programs")
if st.session_state.all_programs:
    for program in st.session_state.all_programs:
        with st.expander(f"{program['name']} - {program['status']}"):
            st.write(f"**Description:** {program['description']}")
            st.write(f"**Organization:** {program['organization_name']}")
            st.write(f"**Start Date:** {program['start_date']}")
            st.write(f"**End Date:** {program['end_date']}")
            st.write(f"**Application Deadline:** {program['deadline']}")
            
            # Display categories if they exist
            if program.get('categories'):
                categories = [cat['name'] for cat in program['categories']]
                st.write(f"**Categories:** {', '.join(categories)}")
            
            # Display qualifications if they exist
            if program.get('qualifications'):
                st.write("**Qualifications:**")
                for qual in program['qualifications']:
                    st.write(f"- {qual['name']}: {qual['description']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if program['status'].lower() == 'open':
                    if st.button("Apply Now", key=f"apply_{program['id']}"):
                        try:
                            # Prepare application data
                            application_data = {
                                "user_id": st.session_state.user_id,
                                "status": "submitted",
                                "qualification_status": "pending"
                            }
                            
                            # Submit application
                            response = requests.post(
                                f"http://api:4000/api/v1/programs/{program['id']}/applications",
                                json=application_data
                            )
                            
                            if response.status_code == 201:
                                st.success("Application submitted successfully!")
                                st.balloons()
                            else:
                                st.error(f"Failed to submit application: {response.text}")
                        except Exception as e:
                            st.error(f"Error submitting application: {str(e)}")
                else:
                    st.button("Apply Now", key=f"apply_{program['id']}", disabled=True)
            with col2:
                if st.button("Give Feedback", key=f"feedback_{program['id']}"):
                    st.session_state.selected_program_id = program['id']
                    st.switch_page("pages/04_Feedback.py")
    
    # Auto-load more programs when reaching the bottom
    if st.session_state.has_more:
        load_more_programs()
        st.rerun()
else:
    st.info("No programs found") 