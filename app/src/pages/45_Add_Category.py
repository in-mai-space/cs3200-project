import streamlit as st
import requests

# Page configuration for the Add Category page
st.set_page_config(
    page_title="Add New Category",
    page_icon="➕",
    layout="wide"
)

st.title("Add New Category")
st.write("Fill out the form below to create a new category.")

# Creates a form to input the new category details
with st.form("add_category_form"):
    category_name = st.text_input("Category Name", placeholder="Enter category name")
    submitted = st.form_submit_button("Create Category")

# When the form is submitted, build the payload and send the POST request
if submitted:
    # Builds the JSON payload according to your CategorySchema
    payload = {
        "name": category_name
    }
    
    # Sets the endpoint URL
    api_url = "http://api:4000/api/v1/categories"

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 201:
            st.success("Category created successfully!")
        else:
            st.error(f"Failed to create category. (Status code: {response.status_code})\nResponse: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
