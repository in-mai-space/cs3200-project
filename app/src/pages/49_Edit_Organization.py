import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Edit Organization",
    page_icon="✏️",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("✏️ Edit Organization")

# Get organization ID from session state
org_id = st.session_state.get('edit_org_id')
if not org_id:
    st.error("No organization selected for editing")
    st.stop()

# Load organization data
try:
    response = requests.get(f"http://api:4000/api/v1/organizations/{org_id}")
    if response.status_code == 200:
        org_data = response.json()
    else:
        st.error(f"Failed to load organization data: {response.text}")
        st.stop()
except Exception as e:
    st.error(f"Error loading organization data: {str(e)}")
    st.stop()

# Edit Organization Form
with st.form("edit_org_form"):
    edit_col1, edit_col2 = st.columns(2)
    with edit_col1:
        edit_name = st.text_input("Organization Name", value=org_data['name'], help="Required")
    with edit_col2:
        edit_website_url = st.text_input("Website URL", value=org_data['website_url'], help="Required")
    
    edit_description = st.text_area("Description", value=org_data['description'], help="Required")
    edit_is_verified = st.checkbox("Verified Organization", value=org_data.get('is_verified', False))
    
    edit_submitted = st.form_submit_button("Update Organization")

if edit_submitted:
    # Validate required fields
    if not edit_name or not edit_description or not edit_website_url:
        st.error("Please fill in all required fields")
    else:
        # Prepare the payload
        payload = {
            "name": edit_name,
            "description": edit_description,
            "website_url": edit_website_url,
            "is_verified": edit_is_verified
        }
        
        try:
            response = requests.put(f"http://api:4000/api/v1/organizations/{org_id}", json=payload)
            if response.status_code == 200:
                st.markdown("""
                    <div style='background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; text-align: center;'>
                        <i class='fas fa-check-circle'></i> Organization updated successfully!
                    </div>
                """, unsafe_allow_html=True)
                st.session_state.edit_org_id = None
                st.session_state.returning_from_edit = True
                st.switch_page("pages/23_Org_Management.py")
            else:
                st.error(f"Failed to update organization. Status code: {response.status_code}\nResponse: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Back button
if st.button("Back to Organization Management"):
    st.session_state.edit_org_id = None
    st.switch_page("pages/23_Org_Management.py")
