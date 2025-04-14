import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Category Management",
    page_icon="👥",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("🏢 Category Management")

# Search and filter
col1, col2 = st.columns(2)
with col1:
    search_query = st.text_input("Search categories")

# Category list
st.markdown("### Category List")
st.dataframe({
    "Organization Name": ["Category 1", "Category 2", "Category 3", "Category 4"],
    "Status": ["Active", "Active", "Active", "Inactive"],
    "Last Login": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
})

# User actions
st.markdown("### User Actions")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Add New Category", type='primary', use_container_width=True):
        st.switch_page("pages/22_Add_Organization.py")
with col2:
    if st.button("Edit Category", type='primary', use_container_width=True):
        st.switch_page("pages/22_Edit_Organization.py")
with col3:
    if st.button("Delete Category", type='secondary', use_container_width=True):
        st.warning("Are you sure you want to delete this category?")

# User details
with st.expander("Category Details"):
    st.write("**Category Name:** Category 1")