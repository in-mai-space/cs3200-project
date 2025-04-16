import streamlit as st
import requests

st.set_page_config(
    page_title="Add New User",
    page_icon="➕",
    layout="wide"
)

st.title("Add New User")
st.write("Fill out the form below to create a new user.")

with st.form("new_user_form"):
    # Fields corresponding to the UserSchema:
    first_name = st.text_input("First Name", placeholder="Enter first name")
    last_name = st.text_input("Last Name", placeholder="Enter last name")
    user_type = st.selectbox(
        "User Type",
        options=['admin', 'user', 'data_analyst', 'organization_admin'],
        help="Select the user role"
    )
    
    # Submit button of the form
    submitted = st.form_submit_button("Create User")

# When the form is submitted:
if submitted:
    # Builds the payload as specified by schema
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "type": user_type
    }
    
    api_url = "http://api:4000/api/v1/users/"

    # Error handling
    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 201:
            st.success("User created successfully!")
        else:
            st.error(f"Failed to create user. (Status code: {response.status_code})\nResponse: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
