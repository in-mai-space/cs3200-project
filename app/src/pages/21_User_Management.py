import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="User Management",
    page_icon="👥",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("👥 User Management")

# Searche section that requires entering a User ID (UUID) to search for a user
user_id_search = st.text_input("Enter User ID (UUID) to search")

# Retrieves user data from the API
users_data = []
if user_id_search:
    # Constructs the endpoint URL using the provided User ID
    api_url = f"http://api:4000/api/v1/users/{user_id_search}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            # Assumes the endpoint returns a JSON object with user data
            user = response.json()
            users_data.append(user)
        else:
            st.error(f"Failed to retrieve user. (Status code: {response.status_code})")
    except Exception as e:
        st.error(f"Error retrieving user: {str(e)}")
else:
    st.info("Enter a User ID above to display user details from the database.")

# Displays the user list using the retrieved data
if users_data:
    # Prepares data for the DataFrame
    records = []
    for user in users_data:
        records.append({
            "Username": f"{user.get('first_name', '')} {user.get('last_name', '')}",
            "Role": user.get('type', ''),
            "Registered At": user.get('registered_at', '')
        })
    st.markdown("### User List")
    st.dataframe(records)
else:
    st.markdown("### User List")
    st.info("No user data to display. Please enter a valid User ID above.")
    
# User actions
st.markdown("### User Actions")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Add New User", type='primary', use_container_width=True):
        st.switch_page("pages/41_Add_User.py")
with col2:
    if st.button("Edit User", type='primary', use_container_width=True):
        st.switch_page("pages/42_Edit_User.py")
with col3:
    # When the Delete User button is clicked, set a flag in session state.
    if st.button("Delete User", type='secondary', use_container_width=True):
        st.session_state.delete_mode = True

# If the deletion mode is activated, show the confirmation warning and input
if st.session_state.get("delete_mode", False):
    st.warning("Are you sure you want to delete this user?")
    user_id_to_delete = st.text_input("Enter the User ID to delete")

    # When the Confirm Delete button is clicked, perform the deletion.
    if st.button("Confirm Delete", use_container_width=True):
        if user_id_to_delete:
            # Builds the DELETE endpoint URL
            api_url = f"http://api:4000/api/v1/users/{user_id_to_delete}"
            try:
                response = requests.delete(api_url)
                if response.status_code == 200:
                    st.success("User deleted successfully!")
                    # Optionally, reset the delete mode flag
                    st.session_state.delete_mode = False
                else:
                    st.error(f"Failed to delete user. (Status code: {response.status_code})\nResponse: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("Please enter a valid User ID.")

# User details
with st.expander("User Details"):
    st.write("**Username:** user1")
    st.write("**Role:** User")
    st.write("**Email:** user1@example.com")
    st.write("**Status:** Active")
    st.write("**Created:** 2024-01-01")
    st.write("**Last Login:** 2024-01-01") 