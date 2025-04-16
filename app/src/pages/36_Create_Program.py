import datetime
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Create Program",
    page_icon="⚙️",
    layout="wide"
)

# Add navigation
SideBarLinks()

# Organization profile
st.markdown("### Create Program")
with st.form("create_program"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Program Name", value='')
        description = st.text_area("Description", value='')
        status = st.text_input("Status", value='')
    
    with col2:
        today = datetime.date.today()
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        deadline = st.date_input("Application Deadline")
                
    
    submitted = st.form_submit_button("Create Program")

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
            program_url = f"http://api:4000/api/v1/organizations/b2f4a96d-9618-4f5f-8687-0519b20fbb4c/programs"
            response = requests.post(program_url, json=payload)
            if response.status_code == 200 or response.status_code == 201:
                st.success("Program successfully created!")
            else:
                st.error(f"Failed to create new program. (Status code: {response.status_code})\nResponse: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")