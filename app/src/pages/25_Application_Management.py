import requests
import streamlit as st
from modules.nav import SideBarLinks

if "delete_mode" not in st.session_state:
    st.session_state.delete_mode = False

st.set_page_config(
    page_title="Application Management",
    page_icon="👥",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("🏢 Application Management")

st.markdown("### Find Application by ID")
app_id = st.text_input("Application ID", placeholder="Enter the application’s UUID")
if st.button("Search"):
    if not app_id:
        st.error("⚠️ Please enter an Application ID to search.")
    else:
        api_url = f"http://api:4000/api/v1/applications/{app_id}"
        try:
            resp = requests.get(api_url)
            if resp.status_code == 200:
                app = resp.json()
                st.success("✅ Application found!")
                # Display key fields:
                st.write("**User ID:**", app.get("user_id"))
                st.write("**Program ID:**", app.get("program_id"))
                st.write("**Status:**", app.get("status"))
                st.write("**Qualification Status:**", app.get("qualification_status"))
                st.write("**Applied At:**", app.get("applied_at"))
                st.write("**Decision Date:**", app.get("decision_date"))
                st.write("**Decision Notes:**", app.get("decision_notes"))
                st.write("**Last Updated:**", app.get("last_updated"))
            else:
                st.error(f"❌ Not found (status {resp.status_code}): {resp.text}")
        except Exception as e:
            st.error(f"Error fetching application: {e}")

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