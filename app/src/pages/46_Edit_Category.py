import streamlit as st
import requests

# Configures the page for editing a category
st.set_page_config(
    page_title="Edit Category",
    page_icon="✏️",
    layout="wide"
)

st.title("Edit Category")
st.write("Update the category details below. You need to provide the category ID (UUID) and the new name for the category.")

# Creates a form to enter the category update data
with st.form("edit_category_form"):
    # Input for the category ID (UUID)
    category_id = st.text_input("Category ID", placeholder="Enter the category UUID")
    # Input for the new category name
    new_name = st.text_input("New Category Name", placeholder="Enter the new category name")
    
    submitted = st.form_submit_button("Update Category")

if submitted:
    # Validates that the category ID was provided
    if not category_id:
        st.error("Category ID is required to update the category.")
    elif not new_name:
        st.error("Please enter a new category name.")
    else:
        # Builds the JSON payload 
        payload = {
            "name": new_name
        }
        
        # Constructs the API URL for updating the category
        api_url = f"http://api:4000/api/v1/categories/{category_id}"

        try:
            response = requests.put(api_url, json=payload)
            if response.status_code == 200:
                st.success("Category updated successfully!")
            else:
                st.error(f"Failed to update category. (Status code: {response.status_code})\nResponse: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
