import requests
import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Category Management",
    page_icon="👥",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("🏢 Category Management")

# Search bar for a specific category (by UUID)
search_query = st.text_input("Search category by ID (UUID)")

# Retrieve categories based on the search input or get all categories when empty
if search_query:
    # Search for a specific category using its ID
    api_url = f"http://api:4000/api/v1/categories/{search_query}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            # Wrap the single category in a list for consistency
            categories = [response.json()]
        else:
            st.error(f"Category not found (Status code: {response.status_code}).")
            categories = []
    except Exception as e:
        st.error(f"Error retrieving category: {str(e)}")
        categories = []
else:
    # Get all categories with pagination (for example, page=1 and limit=50)
    api_url = "http://api:4000/api/v1/categories?page=1&limit=50"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            # Assume the response is a list of category objects
            categories = response.json()
        else:
            st.error(f"Failed to retrieve categories (Status code: {response.status_code}).")
            categories = []
    except Exception as e:
        st.error(f"Error retrieving categories: {str(e)}")
        categories = []

# Display the category list in a dataframe if categories exist
st.markdown("### Category List")
if categories:
    df = pd.DataFrame([{
        "Category ID": cat.get("id", ""),
        "Category Name": cat.get("name", "")
    } for cat in categories])
    st.dataframe(df)
else:
    st.info("No categories to display.")

# Category actions
st.markdown("### Category Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Add New Category", type='primary', use_container_width=True):
        st.switch_page("pages/45_Add_Category.py")

with col2:
    if st.button("Edit Category", type='primary', use_container_width=True):
        st.switch_page("pages/46_Edit_Category.py")

with col3:
    if st.button("Delete Category", type='secondary', use_container_width=True):
        st.session_state.delete_mode = True

# If deletion mode is active, display a warning and input for category ID
if st.session_state.get("delete_mode", False):
    st.warning("Are you sure you want to delete this category?")
    category_id_to_delete = st.text_input("Enter the Category ID to delete")
    
    if st.button("Confirm", use_container_width=True):
        if category_id_to_delete:
            delete_url = f"http://api:4000/api/v1/categories/{category_id_to_delete}"
            try:
                del_response = requests.delete(delete_url)
                if del_response.status_code == 200:
                    st.success("Category deleted successfully!")
                    st.session_state.delete_mode = False
                else:
                    st.error(f"Failed to delete category (Status code: {del_response.status_code}).\nResponse: {del_response.text}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("Please enter a valid Category ID.")

# Static category details (optional)
with st.expander("Category Details"):
    st.write("**Category Name:** Category 1")
