import datetime
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Create Program",
    page_icon="➕",
    layout="wide"
)

# Add navigation
SideBarLinks()

# Check if organization ID is set
if 'selected_organization_id' not in st.session_state:
    st.error("No organization selected. Please select an organization from the role selection page.")
    st.stop()

# Organization profile
st.markdown("### Create Program")
with st.form("create_program"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Program Name")
        description = st.text_area("Description")
        status = st.selectbox(
            "Status",
            options=['OPEN', 'CLOSE'],
            index=0
        )
    
    with col2:
        today = datetime.date.today()
        start_date = st.date_input("Start Date", value=today)
        end_date = st.date_input("End Date", value=today)
        deadline = st.date_input("Application Deadline", value=today)
    
    # Add a centered submit button with proper styling
    st.markdown("---")
    submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
    with submit_col2:
        submitted = st.form_submit_button("Create Program", type="primary", use_container_width=True)

    if submitted:
        payload = {
            "name": name,
            "description": description,
            "status": status,
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "deadline": deadline.strftime('%Y-%m-%dT00:00:00')
        }

        try:
            program_url = f"http://api:4000/api/v1/organizations/{st.session_state.selected_organization_id}/programs"
            response = requests.post(program_url, json=payload)
            if response.status_code == 201:
                st.success("Successfully created program!")
                st.session_state.from_create_page = True
                st.switch_page("pages/31_Org_Programs.py")
            else:
                st.error(f"Failed to create program. (Status code: {response.status_code})\nResponse: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}") 