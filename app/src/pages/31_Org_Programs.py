import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Organization Programs",
    page_icon="📋",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📋 Organization Programs")

# Search and filter
col1, col2 = st.columns(2)
with col1:
    search_query = st.text_input("Search programs")
with col2:
    status_filter = st.selectbox("Filter by status", ["All", "Active", "Draft", "Closed"])

# Program list
st.markdown("### Program List")
st.dataframe({
    "Program Name": ["Program A", "Program B", "Program C"],
    "Status": ["Active", "Draft", "Closed"],
    "Applications": [100, 50, 200],
    "Created": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "Last Updated": ["2024-01-15", "2024-01-16", "2024-01-17"]
})

# Program actions
st.markdown("### Program Actions")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Create New Program", type='primary', use_container_width=True):
        st.switch_page("36_Create_Program")
with col2:
    if st.button("Edit Program", type='primary', use_container_width=True):
        st.switch_page("35_Edit_Program")
with col3:
    if st.button("Delete Program", type='secondary', use_container_width=True):
        st.warning("Are you sure you want to delete this program?")

# Program details
with st.expander("Program Details"):
    st.write("**Program Name:** Program A")
    st.write("**Description:** This is a sample program description.")
    st.write("**Status:** Active")
    st.write("**Eligibility Criteria:** Open to all qualified applicants")
    st.write("**Application Deadline:** 2024-12-31")
    st.write("**Created:** 2024-01-01")
    st.write("**Last Updated:** 2024-01-15")

# Program statistics
st.markdown("### Program Statistics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Applications", "100", "+5%")
with col2:
    st.metric("Approved", "80", "+10%")
with col3:
    st.metric("Pending", "15", "-2%")
with col4:
    st.metric("Rejected", "5", "-3%") 