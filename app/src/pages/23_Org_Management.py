import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Organization Management",
    page_icon="🏢",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("🏢 Organization Management")

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'page_size' not in st.session_state:
    st.session_state.page_size = 3
if 'all_organizations' not in st.session_state:
    st.session_state.all_organizations = []
if 'selected_org' not in st.session_state:
    st.session_state.selected_org = None

# Check if we're returning from edit page
if st.session_state.get('edit_org_id') is None and st.session_state.get('returning_from_edit', False):
    st.session_state.all_organizations = []
    st.session_state.page = 1
    st.session_state.returning_from_edit = False

# Function to load organizations
def load_organizations():
    try:
        params = {
            'page': st.session_state.page,
            'limit': st.session_state.page_size
        }
        response = requests.get("http://api:4000/api/v1/organizations", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to load organizations: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error loading organizations: {str(e)}")
        return []

# Function to load all organizations for dropdown
def load_all_organizations():
    try:
        params = {
            'page': st.session_state.page,
            'limit': 100  # Load more at once for dropdown
        }
        response = requests.get("http://api:4000/api/v1/organizations", params=params)
        if response.status_code == 200:
            new_orgs = response.json()
            st.session_state.all_organizations.extend(new_orgs)
            st.session_state.page += 1
            return new_orgs
        else:
            st.error(f"Failed to load organizations: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error loading organizations: {str(e)}")
        return []

# Search section
[search_col] = st.columns(1)
with search_col:
    search_query = st.text_input("Search by organization name")

# Load initial organizations for dropdown
if not st.session_state.all_organizations:
    load_all_organizations()

# Load and display paginated organizations for table
organizations = load_organizations()

if organizations:
    # Convert to DataFrame for better display
    df = pd.DataFrame(organizations)
    
    # Apply search filter if query exists
    if search_query:
        df = df[df['name'].str.contains(search_query, case=False, na=False)]
    
    # Display organizations table
    st.markdown("### Organizations")
    st.dataframe(
        df[['name', 'description', 'website_url']],
        use_container_width=True
    )

    # Pagination controls for table
    pagination_col1, pagination_col2, pagination_col3 = st.columns([1, 2, 1])
    with pagination_col1:
        if st.session_state.page > 1:
            if st.button("Previous Page"):
                st.session_state.page -= 1
                st.rerun()
    with pagination_col2:
        st.write(f"Page {st.session_state.page}")
    with pagination_col3:
        if len(organizations) == st.session_state.page_size:
            if st.button("Next Page"):
                st.session_state.page += 1
                st.rerun()
    
    # Organization selection with infinite scroll
    st.markdown("### Select Organization")
    org_options = [f"{org['name']} (ID: {org['id']})" for org in st.session_state.all_organizations]
    if search_query:
        org_options = [opt for opt in org_options if search_query.lower() in opt.lower()]
    
    selected_org = st.selectbox(
        "Select an organization to manage",
        options=org_options if org_options else ["No organizations available"],
        index=0
    )
    
    # Load more organizations for dropdown if we're near the end
    if len(st.session_state.all_organizations) > 0 and len(st.session_state.all_organizations) % 100 == 0:
        load_all_organizations()
        st.rerun()
    
    if selected_org != "No organizations available":
        # Get the selected organization's data
        org_id = selected_org.split("(ID: ")[1].rstrip(")")
        org_data = next((org for org in st.session_state.all_organizations if str(org['id']) == org_id), None)
        
        if org_data:
            # Display organization details
            with st.expander("Organization Details"):
                details_col1, details_col2 = st.columns(2)
                with details_col1:
                    st.write(f"**Name:** {org_data['name']}")
                    st.write(f"**Description:** {org_data['description']}")
                with details_col2:
                    st.write(f"**Website:** {org_data['website_url']}")
                
                if 'categories' in org_data and org_data['categories']:
                    st.write("**Categories:**")
                    for category in org_data['categories']:
                        st.write(f"- {category['name']}")
                
                if 'locations' in org_data and org_data['locations']:
                    st.write("**Locations:**")
                    for location in org_data['locations']:
                        st.write(f"- {location['city']}, {location['state']} {location['zip_code']}")
            
            # Organization actions
            action_col1, action_col2 = st.columns(2)
            with action_col1:
                if st.button("Edit Organization", type='primary', use_container_width=True):
                    st.session_state.edit_org_id = org_id
                    st.switch_page("pages/49_Edit_Organization.py")
            with action_col2:
                if st.button("Delete Organization", type='secondary', use_container_width=True):
                    try:
                        response = requests.delete(f"http://api:4000/api/v1/organizations/{org_id}")
                        if response.status_code == 200:
                            st.success("Organization deleted successfully")
                            st.session_state.selected_org = None
                            st.session_state.all_organizations = []
                            st.session_state.page = 1
                            st.rerun()
                        else:
                            st.error("Failed to delete organization")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
else:
    st.info("No organizations found")

# Add New Organization Section
st.markdown("### Add New Organization")
with st.form("add_org_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Organization Name", help="Required")
    with col2:
        website_url = st.text_input("Website URL", help="Required")
    
    description = st.text_area("Description", help="Required")
    is_verified = st.checkbox("Verified Organization", value=False)
    
    submitted = st.form_submit_button("Create Organization")

if submitted:
    # Validate required fields
    if not name or not description or not website_url:
        st.error("Please fill in all required fields")
    else:
        # Prepare the payload
        payload = {
            "name": name,
            "description": description,
            "website_url": website_url,
            "is_verified": is_verified
        }
        
        try:
            response = requests.post("http://api:4000/api/v1/organizations", json=payload)
            if response.status_code == 201:
                st.success("Organization created successfully!")
                st.session_state.all_organizations = []
                st.session_state.page = 1
                st.rerun()
            else:
                st.error(f"Failed to create organization. Status code: {response.status_code}\nResponse: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}") 