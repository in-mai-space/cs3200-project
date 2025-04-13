import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="User Management",
    page_icon="👥",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("🏢 Organization Management")

# Search and filter
col1, col2 = st.columns(2)
with col1:
    search_query = st.text_input("Search organizations")
with col2:
    status_filter = st.selectbox("Filter by status", ["All", "Active", "Inactive"])

# Organization list
st.markdown("### Organization List")
st.dataframe({
    "Organization Name": ["Organization 1", "Organization 2", "Organization 3", "Organization 4"],
    "Status": ["Active", "Active", "Active", "Inactive"],
    "Last Login": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
})

# User actions
st.markdown("### User Actions")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Add New Organization", type='primary', use_container_width=True):
        st.switch_page("pages/22_Add_Organization.py")
with col2:
    if st.button("Edit Organization", type='primary', use_container_width=True):
        st.switch_page("pages/22_Edit_Organization.py")
with col3:
    if st.button("Delete Organization", type='secondary', use_container_width=True):
        st.warning("Are you sure you want to delete this organization?")

# User details
with st.expander("Organization Details"):
    st.write("**Organization Name:** Organization 1")
    st.write("**Status:** Active")
    st.write("**Created:** 2024-01-01")
    st.write("**Last Login:** 2024-01-01") 