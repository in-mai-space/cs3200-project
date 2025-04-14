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
    if st.button("Delete User", type='secondary', use_container_width=True):
        st.warning("Are you sure you want to delete this user?")

# User details
with st.expander("User Details"):
    st.write("**Username:** user1")
    st.write("**Role:** User")
    st.write("**Email:** user1@example.com")
    st.write("**Status:** Active")
    st.write("**Created:** 2024-01-01")
    st.write("**Last Login:** 2024-01-01") 