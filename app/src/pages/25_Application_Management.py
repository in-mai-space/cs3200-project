import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Application Management",
    page_icon="👥",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("🏢 Application Management")

# Search and filter
col1, col2 = st.columns(2)
with col1:
    search_query = st.text_input("Search applications")

# Category list
st.markdown("### Application List")
st.dataframe({
    "Application Name": ["Application 1", "Application 2", "Application 3", "Application 4"],
    "Status": ["Active", "Active", "Active", "Inactive"],
    "Last Login": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
})

# User actions
st.markdown("### User Actions")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Add New Application", type='primary', use_container_width=True):
        st.switch_page("pages/47_Add_Application.py")
with col2:
    if st.button("Edit Application", type='primary', use_container_width=True):
        st.switch_page("pages/48_Edit_Application.py")
with col3:
    if not st.session_state.delete_mode:
        if st.button("Delete Application", type="secondary", use_container_width=True):
            st.session_state.delete_mode = True
    else:
        # confirm UI
        st.warning("Are you sure you want to delete this application?")
        app_id = st.text_input(
            "Application ID to delete",
            placeholder="Enter the application’s UUID",
            key="delete_app_id"
        )
        if st.button("Confirm Delete", type="primary", use_container_width=True):
            if not app_id:
                st.error("⚠️ Please enter a valid Application ID before confirming.")
            else:
                api_url = f"http://api:4000/api/v1/applications/{app_id}"
                try:
                    resp = requests.delete(api_url)
                    if resp.status_code == 200:
                        st.success("✅ Application deleted successfully!")
                    else:
                        st.error(
                            f"Failed to delete application.\n"
                            f"Status code: {resp.status_code}\n"
                            f"Response: {resp.text}"
                        )
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            # exit delete‑mode and clear the text box
            st.session_state.delete_mode = False
            st.session_state.delete_app_id = ""

# User details
with st.expander("Application Details"):
    st.write("**Application Name:** Application 1")