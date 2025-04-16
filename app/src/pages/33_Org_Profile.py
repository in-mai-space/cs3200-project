import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Organization Profile",
    page_icon="⚙️",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("⚙️ Organization Profile")

# Organization profile
st.markdown("### Organization Profile")
with st.form("org_profile"):
    col1, col2 = st.columns(2)


    org_url = f"http://api:4000/api/v1/organizations/b2f4a96d-9618-4f5f-8687-0519b20fbb4c"
    org_response = requests.get(org_url)
    if org_response.status_code == 200 : org_data = org_response.json()
    
    contact_response = requests.get("http://api:4000/api/v1/organizations/b2f4a96d-9618-4f5f-8687-0519b20fbb4c/53259585-6553-6258-9581-28a3a0a1a6a5")
    if contact_response.status_code == 200 : contact_data = contact_response.json() 
    
    with col1:
        org_name = st.text_input("Organization Name", value=org_data['name'])
        website = st.text_input("Website", value=org_data['website_url'])
        description = st.text_area("Description", value=org_data['description'])
    
    with col2:
        email = st.text_input("Contact Email", value=contact_data['email'])
        phone = st.text_input("Phone Number", value=contact_data['phone_number'])
        address = st.text_area("Address", value="123 Organization Street")
    
    submitted = st.form_submit_button("Update Profile")

    if submitted:
        payload = { "is_verified": org_data.get("is_verified", False) } 
        if org_name:
            payload["name"] = org_name
        if website: 
            payload["website_url"] = website
        if description:
            payload["description"] = description

        try:
            response = requests.put(org_url, json=payload)
            if response.status_code == 200:
                st.success("Organization profile updated successfully!")
            else:
                st.error(f"Failed to update profile. (Status code: {response.status_code})\nResponse: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")



