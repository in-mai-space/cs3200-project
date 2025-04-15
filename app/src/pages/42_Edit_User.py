import streamlit as st
import requests

# Configure the page
st.set_page_config(
    page_title="Edit User",
    page_icon="✏️",
    layout="wide"
)

st.title("Edit User")
st.write("Update the user details below by providing the User ID and the fields you want to change.")

# Creates the edit user form
with st.form("edit_user_form"):
    # Field for the user's ID (UUID)
    user_id = st.text_input("User ID", placeholder="Enter the user UUID")

    # Fields that can be updated
    first_name = st.text_input("First Name", placeholder="Enter new first name")
    last_name = st.text_input("Last Name", placeholder="Enter new last name")
    user_type = st.selectbox(
        "User Type",
        options=["", "admin", "user", "data_analyst", "organization_admin"],
        help="Select the new user role (leave blank to keep unchanged)"
    )
    
    # Submit button for the form
    submitted = st.form_submit_button("Update User")

if submitted:
    # Builds the payload only with fields that have been provided
    payload = {}
    if first_name:
        payload["first_name"] = first_name
    if last_name:
        payload["last_name"] = last_name
    if user_type:
        payload["type"] = user_type

    if not user_id:
        st.error("User ID is required to update a user.")
    else:

        api_url = f"http://api:4000/api/v1/users/{user_id}"

        try:
            response = requests.put(api_url, json=payload)
            if response.status_code == 200:
                st.success("User updated successfully!")
            else:
                st.error(f"Failed to update user. (Status code: {response.status_code})\nResponse: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
