import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(
    page_title="Browse Organizations",
    page_icon="🏢",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("🏢 Available Organizations")

# Initialize session state for organizations and programs
if 'all_organizations' not in st.session_state:
    st.session_state.all_organizations = []
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'has_more' not in st.session_state:
    st.session_state.has_more = True
if 'selected_organization_id' not in st.session_state:
    st.session_state.selected_organization_id = None
if 'organization_programs' not in st.session_state:
    st.session_state.organization_programs = []

# Search section
search_query = st.text_input("Search organizations by name")

# Reset organizations when search changes
if 'last_search_query' not in st.session_state:
    st.session_state.last_search_query = search_query
elif st.session_state.last_search_query != search_query:
    st.session_state.all_organizations = []
    st.session_state.page = 1
    st.session_state.has_more = True
    st.session_state.last_search_query = search_query

def load_more_organizations():
    try:
        params = {
            'page': st.session_state.page,
            'limit': 10,
            'search_query': search_query if search_query else None
        }
        response = requests.get("http://api:4000/api/v1/organizations", params=params)
        if response.status_code == 200:
            new_organizations = response.json()
            if new_organizations:
                st.session_state.all_organizations.extend(new_organizations)
                st.session_state.page += 1
                st.session_state.has_more = len(new_organizations) == 10
            else:
                st.session_state.has_more = False
    except Exception as e:
        st.error(f"Error loading organizations: {str(e)}")

# Load initial organizations if needed
if not st.session_state.all_organizations and st.session_state.has_more:
    load_more_organizations()

# Organizations table
st.markdown("## Organizations")
if st.session_state.all_organizations:
    # Convert to DataFrame for table display
    org_df = pd.DataFrame(st.session_state.all_organizations)
    org_df = org_df[['name', 'description']]  # Select only existing columns
    
    # Display table with selection
    selected_org = st.dataframe(
        org_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Organization selection
    selected_org_name = st.selectbox(
        "Select an organization to view its programs",
        options=[org['name'] for org in st.session_state.all_organizations],
        index=None
    )
    
    if selected_org_name:
        # Find the selected organization
        selected_org = next(org for org in st.session_state.all_organizations if org['name'] == selected_org_name)
        st.session_state.selected_organization_id = selected_org['id']
        
        # Load programs for selected organization
        try:
            response = requests.get(f"http://api:4000/api/v1/organizations/{selected_org['id']}/programs")
            if response.status_code == 200:
                st.session_state.organization_programs = response.json()
            else:
                st.error("Failed to load programs")
        except Exception as e:
            st.error(f"Error loading programs: {str(e)}")
        
        # Display programs
        if st.session_state.organization_programs:
            st.markdown(f"## Programs by {selected_org_name}")
            for program in st.session_state.organization_programs:
                with st.expander(f"{program['name']} - {program['status']}"):
                    st.write(f"**Description:** {program['description']}")
                    st.write(f"**Start Date:** {program['start_date']}")
                    st.write(f"**End Date:** {program['end_date']}")
                    st.write(f"**Application Deadline:** {program['deadline']}")
                    
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
        else:
            st.info(f"No programs found for {selected_org_name}")
    
    # Auto-load more organizations when reaching the bottom
    if st.session_state.has_more:
        load_more_organizations()
        st.rerun()
else:
    st.info("No organizations found") 