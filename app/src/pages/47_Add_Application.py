import streamlit as st
import requests

st.set_page_config(
    page_title="Add New Application",
    page_icon="➕",
    layout="wide"
)

st.title("Add New Application")
st.write("Fill in the details below to create a new application.")

# Creates a form for inputting application details
with st.form("add_application_form"):
    program_id = st.text_input("Program ID", placeholder="Enter the Program ID")
    user_id = st.text_input("User ID", placeholder="Enter the User ID")
    
    status = st.selectbox(
        "Application Status",
        options=[
            "draft", "submitted", "under_review", 
            "additional_info_needed", "approved", 
            "rejected", "waitlisted", "withdrawn"
        ],
        index=0
    )
    
    submitted = st.form_submit_button("Create Application")

# When the form is submitted, process and call the API
if submitted:
    if not program_id:
        st.error("Program ID is required.")
    elif not user_id:
        st.error("User ID is required.")
    else:
        # Builds the JSON payload .
        payload = {
            "user_id": user_id,
            "status": status
        }
        
        api_url = f"http://api:4000/api/v1/programs/{program_id}/applications/"
        
        # Validation
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 201:
                st.success("Application created successfully!")
            else:
                st.error(f"Failed to create application. (Status code: {response.status_code})\nResponse: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
