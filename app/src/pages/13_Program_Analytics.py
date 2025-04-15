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

# Initialize session state for pagination and filters
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'page_size' not in st.session_state:
    st.session_state.page_size = 10
if 'filters' not in st.session_state:
    st.session_state.filters = {}

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
if search_query and search_query.strip():  # Only add if search query is not empty
    st.session_state.filters['search_query'] = search_query.strip()
if sort_by:
    st.session_state.filters['sort_by'] = sort_by
if sort_order:
    st.session_state.filters['sort_order'] = sort_order

# Fetch programs with pagination
try:
    params = {
        'page': st.session_state.page,
        'limit': st.session_state.page_size,
        **st.session_state.filters
    }
    response = requests.get("http://api:4000/api/v1/programs", params=params)
    
    if response.status_code == 200:
        programs = response.json()
        
        if programs:
            # Display programs in a table
            df = pd.DataFrame(programs)
            st.markdown("### Programs")
            st.dataframe(
                df[['name', 'organization_name', 'status', 'start_date', 'deadline']],
                use_container_width=True
            )
            
            # Program selection
            selected_program = st.selectbox(
                "Select a program to view details",
                options=[f"{p['name']} - {p['organization_name']}" for p in programs],
                index=0
            )
            
            if selected_program:
                program_id = programs[[f"{p['name']} - {p['organization_name']}" for p in programs].index(selected_program)]['id']
                
                # Program details section
                st.markdown("### Program Details")
                program = programs[[f"{p['name']} - {p['organization_name']}" for p in programs].index(selected_program)]
                
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
                        st.session_state['view'] = 'applications'
                        st.session_state['program_id'] = program_id
                with col2:
                    if st.button("View Profiles"):
                        st.session_state['view'] = 'profiles'
                        st.session_state['program_id'] = program_id
                with col3:
                    if st.button("View Feedbacks"):
                        st.session_state['view'] = 'feedbacks'
                        st.session_state['program_id'] = program_id
                with col4:
                    if st.button("View Feedback Stats"):
                        st.session_state['view'] = 'feedback_stats'
                        st.session_state['program_id'] = program_id
                
                # Display selected view
                if 'view' in st.session_state and st.session_state['program_id'] == program_id:
                    if st.session_state['view'] == 'applications':
                        try:
                            response = requests.get(
                                f"http://api:4000/api/v1/programs/{program_id}/applications",
                                params={'page': st.session_state.page, 'limit': st.session_state.page_size}
                            )
                            if response.status_code == 200:
                                applications = response.json()
                                if applications:
                                    df = pd.DataFrame(applications)
                                    st.markdown("### Applications")
                                    st.dataframe(df, use_container_width=True)
                                else:
                                    st.info("No applications found for this program")
                            else:
                                st.error("Failed to fetch applications")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    
                    elif st.session_state['view'] == 'profiles':
                        try:
                            response = requests.get(
                                f"http://api:4000/api/v1/programs/{program_id}/profiles",
                                params={'page': st.session_state.page, 'limit': st.session_state.page_size}
                            )
                            if response.status_code == 200:
                                profiles = response.json()
                                if profiles:
                                    df = pd.DataFrame(profiles)
                                    st.markdown("### User Profiles")
                                    st.dataframe(df, use_container_width=True)
                                else:
                                    st.info("No profiles found for this program")
                            else:
                                st.error("Failed to fetch profiles")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    
                    elif st.session_state['view'] == 'feedbacks':
                        try:
                            response = requests.get(
                                f"http://api:4000/api/v1/programs/{program_id}/feedbacks",
                                params={'page': st.session_state.page, 'limit': st.session_state.page_size}
                            )
                            if response.status_code == 200:
                                feedbacks = response.json()
                                if feedbacks:
                                    df = pd.DataFrame(feedbacks)
                                    st.markdown("### Feedback Details")
                                    st.dataframe(df, use_container_width=True)
                                else:
                                    st.info("No feedbacks found for this program")
                            else:
                                st.error("Failed to fetch feedbacks")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    
                    elif st.session_state['view'] == 'feedback_stats':
                        try:
                            response = requests.get(f"http://api:4000/api/v1/programs/{program_id}/feedbacks/stats")
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
            st.info("No programs found matching your criteria")
    else:
        st.error("Failed to fetch programs")
except Exception as e:
    st.error(f"Error: {str(e)}") 