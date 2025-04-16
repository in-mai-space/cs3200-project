import datetime
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Edit Program",
    page_icon="⚙️",
    layout="wide"
)

# Add navigation
SideBarLinks()

# Check if program ID is set
if 'edit_program_id' not in st.session_state:
    st.error("No program selected. Please select a program to edit.")
    st.stop()

# Load program data
try:
    program_url = f"http://api:4000/api/v1/programs/{st.session_state.edit_program_id}"
    response = requests.get(program_url)
    if response.status_code != 200:
        st.error(f"Failed to load program data. (Status code: {response.status_code})")
        st.stop()
    program_data = response.json()
except Exception as e:
    st.error(f"Error loading program data: {str(e)}")
    st.stop()

# Organization profile
st.markdown("### Edit Program")
with st.form("edit_program"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Program Name", value=program_data['name'])
        description = st.text_area("Description", value=program_data['description'])
        # Map API status values to display values
        status_map = {'open': 'OPEN', 'close': 'CLOSE'}
        status = st.selectbox(
            "Status",
            options=['OPEN', 'CLOSE'],
            index=['OPEN', 'CLOSE'].index(status_map.get(program_data['status'].lower(), 'OPEN'))
        )
    
    with col2:
        today = datetime.date.today()
        # Parse dates from API format
        try:
            start_date = st.date_input(
                "Start Date",
                value=datetime.datetime.strptime(program_data['start_date'], '%a, %d %b %Y %H:%M:%S %Z').date()
            )
            end_date = st.date_input(
                "End Date",
                value=datetime.datetime.strptime(program_data['end_date'], '%a, %d %b %Y %H:%M:%S %Z').date()
            )
            deadline = st.date_input(
                "Application Deadline",
                value=datetime.datetime.strptime(program_data['deadline'], '%a, %d %b %Y %H:%M:%S %Z').date()
            )
        except ValueError as e:
            st.error(f"Error parsing dates: {str(e)}")
            st.stop()
    
    # Add a centered submit button with proper styling
    st.markdown("---")
    submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
    with submit_col2:
        submitted = st.form_submit_button("Save Changes", type="primary", use_container_width=True)

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
            program_url = f"http://api:4000/api/v1/programs/{st.session_state.edit_program_id}"
            response = requests.put(program_url, json=payload)
            if response.status_code == 200:
                st.success("Successfully saved changes!")
                # Set flag to indicate we're returning from edit page
                st.session_state.from_edit_page = True
                st.switch_page("pages/31_Org_Programs.py")
            else:
                st.error(f"Failed to update program. (Status code: {response.status_code})\nResponse: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")