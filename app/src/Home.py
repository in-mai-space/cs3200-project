##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports regular and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(
    page_title="Program Management System",
    page_icon="📋",
    layout="wide"
)

# If a user is at this page, we assume they are not 
# authenticated. So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Redirect to role selection page
st.switch_page("pages/00_Role_Selection.py")

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title("Welcome to the Program Management System")

# If user is not authenticated, show role selection
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.switch_page("pages/00_Role_Selection.py")

# If user is authenticated, redirect to their role-specific page
if st.session_state["authenticated"]:
    if st.session_state["role"] == "user":
        st.switch_page("pages/02_Programs.py")
    elif st.session_state["role"] == "analyst":
        st.switch_page("pages/13_Program_Analytics.py")
    elif st.session_state["role"] == "administrator":
        st.switch_page("pages/21_User_Management.py")
    elif st.session_state["role"] == "organization":
        st.switch_page("pages/31_Org_Programs.py")

# Add footer
st.markdown("""
---
*Need help? Contact support at support@uplift.org*
""")



