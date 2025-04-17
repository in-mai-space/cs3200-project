import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Program Analytics",
    page_icon="📊",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📊 Program Analytics")

# Initialize session state for infinite scroll and program selection
if 'all_programs' not in st.session_state:
    st.session_state.all_programs = []
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'page_size' not in st.session_state:
    st.session_state.page_size = 20
if 'filters' not in st.session_state:
    st.session_state.filters = {}
if 'has_more' not in st.session_state:
    st.session_state.has_more = True
if 'view' not in st.session_state:
    st.session_state.view = None
if 'program_id' not in st.session_state:
    st.session_state.program_id = None

# Search and filters section
st.markdown("### Search & Filters")
col1, col2, col3 = st.columns(3)
with col1:
    search_query = st.text_input("Search programs (by name, description, or organization)")
with col2:
    sort_by = st.selectbox("Sort By", ["name", "start_date", "deadline"])
with col3:
    sort_order = st.selectbox("Sort Order", ["asc", "desc"])

# Apply filters
st.session_state.filters = {}  # Reset filters
if search_query and search_query.strip():
    st.session_state.filters['search_query'] = search_query.strip()
    st.session_state.all_programs = []  # Reset programs when search changes
    st.session_state.page = 1
    st.session_state.has_more = True
if sort_by:
    st.session_state.filters['sort_by'] = sort_by
    st.session_state.all_programs = []  # Reset programs when search changes
    st.session_state.page = 1
    st.session_state.has_more = True
if sort_order:
    st.session_state.filters['sort_order'] = sort_order
    st.session_state.all_programs = []  # Reset programs when search changes
    st.session_state.page = 1
    st.session_state.has_more = True

# Function to load more programs
def load_more_programs():
    try:
        params = {
            'page': st.session_state.page,
            'limit': st.session_state.page_size,
            **st.session_state.filters
        }
        response = requests.get("http://api:4000/api/v1/programs", params=params)
        
        if response.status_code == 200:
            new_programs = response.json()
            if new_programs:
                st.session_state.all_programs.extend(new_programs)
                st.session_state.page += 1
                st.session_state.has_more = len(new_programs) == st.session_state.page_size
            else:
                st.session_state.has_more = False
    except Exception as e:
        st.error(f"Error loading more programs: {str(e)}")

# Load initial programs if needed
if not st.session_state.all_programs and st.session_state.has_more:
    load_more_programs()

# Display programs in a table
if st.session_state.all_programs:
    df = pd.DataFrame(st.session_state.all_programs)
    st.markdown("### Programs")
    st.dataframe(
        df[['name', 'organization_name', 'status', 'start_date', 'deadline']],
        use_container_width=True
    )
    
    # Program selection
    selected_program = st.selectbox(
        "Select a program to view details",
        options=[f"{p['name']} - {p['organization_name']}" for p in st.session_state.all_programs],
        index=0
    )

    if selected_program:
        # Get the selected program's ID
        selected_index = [f"{p['name']} - {p['organization_name']}" for p in st.session_state.all_programs].index(selected_program)
        selected_program_id = st.session_state.all_programs[selected_index]['id']
        
        # Program details section
        st.markdown("### Program Details")
        program = st.session_state.all_programs[selected_index]
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {program['name']}")
            st.write(f"**Organization:** {program['organization_name']}")
            st.write(f"**Status:** {program['status']}")
        with col2:
            st.write(f"**Start Date:** {program['start_date']}")
            st.write(f"**Deadline:** {program['deadline']}")
            st.write(f"**End Date:** {program['end_date']}")
        
        st.write(f"**Description:** {program['description']}")
        
        # Display categories if available
        if 'categories' in program and program['categories']:
            st.write("**Categories:**")
            for category in program['categories']:
                st.write(f"- {category['name']}")
        
        # Display locations if available
        if 'locations' in program and program['locations']:
            st.write("**Locations:**")
            for location in program['locations']:
                st.write(f"- {location['city']}, {location['state']} {location['zip_code']}")
        
        # Navigation buttons
        st.markdown("### Program Analytics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("View Applications"):
                st.session_state.view = 'applications'
                st.session_state.program_id = selected_program_id
        with col2:
            if st.button("View Profiles"):
                st.session_state.view = 'profiles'
                st.session_state.program_id = selected_program_id
        with col3:
            if st.button("View Feedbacks"):
                st.session_state.view = 'feedbacks'
                st.session_state.program_id = selected_program_id
        with col4:
            if st.button("View Feedback Stats"):
                st.session_state.view = 'feedback_stats'
                st.session_state.program_id = selected_program_id
        
        # Display selected view with infinite scroll
        if st.session_state.view and st.session_state.program_id == selected_program_id:
            if st.session_state.view == 'applications':
                if 'all_applications' not in st.session_state:
                    st.session_state.all_applications = []
                if 'app_page' not in st.session_state:
                    st.session_state.app_page = 1
                
                def load_more_applications():
                    try:
                        response = requests.get(
                            f"http://api:4000/api/v1/programs/{selected_program_id}/applications",
                            params={'page': st.session_state.app_page, 'limit': st.session_state.page_size}
                        )
                        if response.status_code == 200:
                            new_applications = response.json()
                            if new_applications:
                                st.session_state.all_applications.extend(new_applications)
                                st.session_state.app_page += 1
                    except Exception as e:
                        st.error(f"Error loading more applications: {str(e)}")
                
                if not st.session_state.all_applications:
                    load_more_applications()
                
                if st.session_state.all_applications:
                    df = pd.DataFrame(st.session_state.all_applications)
                    st.markdown("### Applications")
                    st.dataframe(df, use_container_width=True)
                    
                    if st.button("Load More Applications"):
                        load_more_applications()
                        st.experimental_rerun()
                else:
                    st.info("No applications found for this program")
            
            elif st.session_state.view == 'profiles':
                if 'all_profiles' not in st.session_state:
                    st.session_state.all_profiles = []
                if 'profiles_page' not in st.session_state:
                    st.session_state.profiles_page = 1
                if 'has_more_profiles' not in st.session_state:
                    st.session_state.has_more_profiles = True
                
                def load_more_profiles():
                    try:
                        response = requests.get(
                            f"http://api:4000/api/v1/programs/{selected_program_id}/profiles",
                            params={'page': st.session_state.profiles_page, 'limit': st.session_state.page_size}
                        )
                        if response.status_code == 200:
                            new_profiles = response.json()
                            if new_profiles:
                                st.session_state.all_profiles.extend(new_profiles)
                                st.session_state.profiles_page += 1
                                st.session_state.has_more_profiles = len(new_profiles) == st.session_state.page_size
                            else:
                                st.session_state.has_more_profiles = False
                    except Exception as e:
                        st.error(f"Error loading more profiles: {str(e)}")
                
                if not st.session_state.all_profiles and st.session_state.has_more_profiles:
                    load_more_profiles()
                
                if st.session_state.all_profiles:
                    df = pd.DataFrame(st.session_state.all_profiles)
                    st.markdown("### User Profiles")
                    st.dataframe(df, use_container_width=True)
                    
                    if st.session_state.has_more_profiles:
                        if st.button("Load More Profiles"):
                            load_more_profiles()
                            st.experimental_rerun()
                else:
                    st.info("No profiles found for this program")
            
            elif st.session_state.view == 'feedbacks':
                if 'all_feedbacks' not in st.session_state:
                    st.session_state.all_feedbacks = []
                if 'feedbacks_page' not in st.session_state:
                    st.session_state.feedbacks_page = 1
                if 'has_more_feedbacks' not in st.session_state:
                    st.session_state.has_more_feedbacks = True
                
                def load_more_feedbacks():
                    try:
                        response = requests.get(
                            f"http://api:4000/api/v1/programs/{selected_program_id}/feedbacks",
                            params={'page': st.session_state.feedbacks_page, 'limit': st.session_state.page_size}
                        )
                        if response.status_code == 200:
                            new_feedbacks = response.json()
                            if new_feedbacks:
                                st.session_state.all_feedbacks.extend(new_feedbacks)
                                st.session_state.feedbacks_page += 1
                                st.session_state.has_more_feedbacks = len(new_feedbacks) == st.session_state.page_size
                            else:
                                st.session_state.has_more_feedbacks = False
                    except Exception as e:
                        st.error(f"Error loading more feedbacks: {str(e)}")
                
                if not st.session_state.all_feedbacks and st.session_state.has_more_feedbacks:
                    load_more_feedbacks()
                
                if st.session_state.all_feedbacks:
                    df = pd.DataFrame(st.session_state.all_feedbacks)
                    st.markdown("### Feedback Details")
                    st.dataframe(df, use_container_width=True)
                    
                    if st.session_state.has_more_feedbacks:
                        if st.button("Load More Feedbacks"):
                            load_more_feedbacks()
                            st.experimental_rerun()
                else:
                    st.info("No feedbacks found for this program")
            
            elif st.session_state.view == 'feedback_stats':
                try:
                    response = requests.get(f"http://api:4000/api/v1/programs/{selected_program_id}/feedbacks/stats")
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
else:
    st.info("No programs found") 