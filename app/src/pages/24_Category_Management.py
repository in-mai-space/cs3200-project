import requests
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
        st.switch_page("pages/45_Add_Category.py")
with col2:
    if st.button("Edit Category", type='primary', use_container_width=True):
        st.switch_page("pages/46_Edit_Category.py")
with col3:
    # When clicking "Delete Category", set a flag in session state
    if st.button("Delete Category", type='secondary', use_container_width=True):
        st.session_state.delete_mode = True

# If deletion mode is active, show a warning and the input field
if st.session_state.get("delete_mode", False):
    st.warning("Are you sure you want to delete this category?")
    category_id_to_delete = st.text_input("Enter the Category ID to delete")
    
    # Change the button to 'Confirm'
    if st.button("Confirm", use_container_width=True):
        if category_id_to_delete:
            # Construct the DELETE endpoint URL.
            # For Docker Compose, using the container name "api" may be appropriate:
            api_url = f"http://api:4000/api/v1/categories/{category_id_to_delete}"
            try:
                response = requests.delete(api_url)
                if response.status_code == 200:
                    st.success("Category deleted successfully!")
                    # Optionally reset delete mode
                    st.session_state.delete_mode = False
                else:
                    st.error(f"Failed to delete category. (Status code: {response.status_code})\nResponse: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("Please enter a valid Category ID.")


# User details
with st.expander("Category Details"):
    st.write("**Category Name:** Category 1")