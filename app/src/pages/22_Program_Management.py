import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Program Management",
    page_icon="�",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("👥 Program Management")

# Search and filter
col1, col2 = st.columns(2)
with col1:
    search_query = st.text_input("Search programs")
with col2:
    status_filter = st.selectbox("Filter by status", ["All", "Active", "Inactive"])

# User list
st.markdown("### User List")
st.dataframe({
    "Program Name": ["Program 1", "Program 2", "Program 3", "Program 4"],
    "Status": ["Active", "Active", "Active", "Inactive"],
    "Last Login": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
})

# User actions
st.markdown("### User Actions")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Add New Program", type='primary', use_container_width=True):
        st.switch_page("pages/22_Add_Program.py")
with col2:
    if st.button("Edit Program", type='primary', use_container_width=True):
        st.switch_page("pages/22_Edit_User.py")
with col3:
    if st.button("Delete Program", type='secondary', use_container_width=True):
        st.warning("Are you sure you want to delete this program?")

# User details
with st.expander("Program Details"):
    st.write("**Program Name:** Program 1")
    st.write("**Status:** Active")
    st.write("**Created:** 2024-01-01")
    st.write("**Last Login:** 2024-01-01") 