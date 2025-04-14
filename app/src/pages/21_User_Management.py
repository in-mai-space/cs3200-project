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

# Search and filter
col1, col2 = st.columns(2)
with col1:
    search_query = st.text_input("Search users")
with col2:
    role_filter = st.selectbox("Filter by role", ["All", "User", "Analyst", "Admin", "Organization"])

# User list
st.markdown("### User List")
st.dataframe({
    "Username": ["user1", "user2", "user3", "user4"],
    "Role": ["User", "Analyst", "Admin", "Organization"],
    "Status": ["Active", "Active", "Active", "Inactive"],
    "Last Login": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
})

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