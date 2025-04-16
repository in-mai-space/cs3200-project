import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(
    page_title="Program Management",
    page_icon="👥",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("👥 Program Management")

# Initialize session state for pagination and filters
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'page_size' not in st.session_state:
    st.session_state.page_size = 3  # Show 3 programs per page
if 'filters' not in st.session_state:
    st.session_state.filters = {}
if 'selected_program' not in st.session_state:
    st.session_state.selected_program = None
if 'dropdown_page' not in st.session_state:
    st.session_state.dropdown_page = 1
if 'dropdown_programs' not in st.session_state:
    st.session_state.dropdown_programs = []
if 'org_page' not in st.session_state:
    st.session_state.org_page = 1
if 'organizations' not in st.session_state:
    st.session_state.organizations = []
if 'org_filters' not in st.session_state:
    st.session_state.org_filters = {}

# Function to load organizations with pagination
def load_organizations():
    try:
        params = {
            'page': st.session_state.org_page,
            'limit': 10
        }
        response = requests.get("http://api:4000/api/v1/organizations", params=params)
        
        if response.status_code == 200:
            new_orgs = response.json()
            if new_orgs:
                st.session_state.organizations.extend(new_orgs)
                st.session_state.org_page += 1
                return True
        return False
    except Exception as e:
        st.error(f"Error loading organizations: {str(e)}")
        return False

# Function to load more programs for dropdown
def load_more_programs():
    try:
        params = {
            'page': st.session_state.dropdown_page,
            'limit': 10,  # Load 10 at a time for dropdown
            **st.session_state.filters
        }
        response = requests.get("http://api:4000/api/v1/programs", params=params)
        if response.status_code == 200:
            new_programs = response.json()
            if new_programs:
                st.session_state.dropdown_programs.extend(new_programs)
                st.session_state.dropdown_page += 1
    except Exception as e:
        st.error(f"Error loading more programs: {str(e)}")

# Load initial organizations if not already loaded
if not st.session_state.organizations:
    load_organizations()

# Search and filter section
st.markdown("### Search & Filters")
col1, col2, col3 = st.columns(3)
with col1:
    search_query = st.text_input("Search programs")
with col2:
    sort_by = st.selectbox("Sort By", ["name", "start_date", "deadline"])
with col3:
    sort_order = st.selectbox("Sort Order", ["asc", "desc"])

# Apply filters
st.session_state.filters = {}  # Reset filters
if search_query and search_query.strip():
    st.session_state.filters['search_query'] = search_query.strip()
if sort_by:
    st.session_state.filters['sort_by'] = sort_by
if sort_order:
    st.session_state.filters['sort_order'] = sort_order

# Reset dropdown data when filters change
if any([search_query, sort_by, sort_order]):
    st.session_state.dropdown_page = 1
    st.session_state.dropdown_programs = []
    load_more_programs()

# Program list with pagination
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
            st.markdown("### Programs")
            df = pd.DataFrame(programs)
            st.dataframe(
                df[['name', 'organization_name', 'status', 'start_date', 'deadline']],
                use_container_width=True
            )
            
            # Pagination controls for table
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.session_state.page > 1:
                    if st.button("Previous Page"):
                        st.session_state.page -= 1
                        st.rerun()
            with col2:
                st.write(f"Page {st.session_state.page}")
            with col3:
                if len(programs) == st.session_state.page_size:
                    if st.button("Next Page"):
                        st.session_state.page += 1
                        st.rerun()
            
            # Program selection with infinite scroll
            st.markdown("### Update Program")
            program_options = [f"{p['name']} - {p['organization_name']}" for p in st.session_state.dropdown_programs]
            
            # Create a container for the selectbox
            select_container = st.container()
            with select_container:
                selected_program = st.selectbox(
                    "Select a program to manage",
                    options=program_options,
                    index=0,
                    key="program_select"
                )
                
                # Load more programs when user reaches the end of the dropdown
                if len(program_options) > 0 and program_options.index(selected_program) == len(program_options) - 1:
                    load_more_programs()
                    st.rerun()
            
            if selected_program:
                program_id = st.session_state.dropdown_programs[program_options.index(selected_program)]['id']
                st.session_state.selected_program = program_id
                
                # Program actions for selected program
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit Program", type='primary', use_container_width=True):
                        st.session_state.edit_program_id = program_id
                        st.switch_page("pages/44_Edit_Program.py")
                with col2:
                    if st.button("Delete Program", type='secondary', use_container_width=True):
                        if st.warning("Are you sure you want to delete this program?"):
                            try:
                                response = requests.delete(f"http://api:4000/api/v1/programs/{st.session_state.selected_program}")
                                if response.status_code == 200:
                                    st.success("Program deleted successfully")
                                    st.session_state.selected_program = None
                                    st.session_state.dropdown_page = 1
                                    st.session_state.dropdown_programs = []
                                    st.rerun()
                                else:
                                    st.error("Failed to delete program")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                
                # Display program details
                program = st.session_state.dropdown_programs[program_options.index(selected_program)]
                with st.expander("Program Details"):
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
                    
                    if 'categories' in program and program['categories']:
                        st.write("**Categories:**")
                        for category in program['categories']:
                            st.write(f"- {category['name']}")
                    
                    if 'locations' in program and program['locations']:
                        st.write("**Locations:**")
                        for location in program['locations']:
                            st.write(f"- {location['city']}, {location['state']} {location['zip_code']}")
            
            # Add new program section
            st.markdown("### Add New Program")
            
            # Organization selection with infinite scroll
            if not st.session_state.organizations:
                load_organizations()
            
            org_options = [f"{org['name']}" for org in st.session_state.organizations]
            org_container = st.container()
            with org_container:
                selected_org = st.selectbox(
                    "Select organization for new program",
                    options=org_options if org_options else ["No organizations available"],
                    index=0,
                    key="org_select"
                )
                
                # Load more organizations when user reaches the end of the dropdown
                if org_options and org_options.index(selected_org) == len(org_options) - 1:
                    if load_organizations():
                        st.rerun()
            
            if st.button("Add New Program", type='primary', use_container_width=True):
                if selected_org != "No organizations available":
                    selected_index = org_options.index(selected_org)
                    org_id = st.session_state.organizations[selected_index]['id']
                    st.session_state.add_program_org_id = org_id
                    st.switch_page("pages/43_Add_Program.py")
                else:
                    st.error("Please select an organization first")
        else:
            st.info("No programs found matching your criteria")
    else:
        st.error("Failed to fetch programs")
except Exception as e:
    st.error(f"Error: {str(e)}") 