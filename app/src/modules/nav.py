# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")

#### ------------------------ User Role ------------------------
def UserHomeNav():
    st.sidebar.page_link("pages/01_Organizations.py", label="Browse Organizations", icon="📋")
    st.sidebar.page_link("pages/02_Programs.py", label="Browse Programs", icon="📋")
    st.sidebar.page_link("pages/03_User_Applications.py", label="My Applications", icon="📝")
    st.sidebar.page_link("pages/04_Profile.py", label="My Profile", icon="👤")

#### ------------------------ Analyst Role ------------------------
def AnalystHomeNav():
    st.sidebar.page_link("pages/13_Program_Analytics.py", label="Program Analytics", icon="📊")
    st.sidebar.page_link("pages/14_Platform_Analytics.py", label="Platform Analytics", icon="⚙️")


#### ------------------------ Admin Role ------------------------
# Pages:
# User Management
# Program Management (reused from organization persona possibly?)
# Organization Management
# Categories Management 
# Application Management 
# Feedback Management
def AdminHomeNav():
    st.sidebar.page_link("pages/21_User_Management.py", label="User Management", icon="👥")
    st.sidebar.page_link("pages/22_Program_Management.py", label="Program Management", icon="⚙️")
    st.sidebar.page_link("pages/23_Org_Management.py", label="Organization Management", icon="🏢")
    st.sidebar.page_link("pages/24_Category_Management.py", label="Category Management", icon="⚙️")
    st.sidebar.page_link("pages/25_Application_Management.py", label="Application Management", icon="🏢")
    st.sidebar.page_link("pages/26_Feedback_Management.py", label="Feedback Management", icon="⚙️")

#### ------------------------ Organization Role ------------------------
def OrganizationHomeNav():
    st.sidebar.page_link("pages/31_Org_Programs.py", label="Manage Programs", icon="📋")
    st.sidebar.page_link("pages/32_Org_Applications.py", label="View Applications", icon="📝")
    st.sidebar.page_link("pages/33_Org_Settings.py", label="Organization Settings", icon="⚙️")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role.
    """
    # If there is no logged in user, redirect to the Role Selection page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("pages/00_Role_Selection.py")

    if show_home:
        st.sidebar.page_link("pages/00_Role_Selection.py", label="Role Selection", icon="👥")

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:
        if st.session_state["role"] == "user":
            st.sidebar.page_link("pages/01_Organizations.py", label="Browse Organizations", icon="📋")
            st.sidebar.page_link("pages/02_Programs.py", label="Browse Programs", icon="📋")
            st.sidebar.page_link("pages/03_User_Applications.py", label="My Applications", icon="📝")
            st.sidebar.page_link("pages/04_Profile.py", label="My Profile", icon="👤")
        elif st.session_state["role"] == "analyst":
            st.sidebar.page_link("pages/13_Program_Analytics.py", label="Program Analytics", icon="📈")
            st.sidebar.page_link("pages/14_Platform_Analytics.py", label="Platform Analytics", icon="⚙️")
        elif st.session_state["role"] == "administrator":
            st.sidebar.page_link("pages/21_User_Management.py", label="User Management", icon="👥")
            st.sidebar.page_link("pages/22_Program_Management.py", label="Program Management", icon="⚙️")
            st.sidebar.page_link("pages/23_Org_Management.py", label="Organization Management", icon="🏢")
            st.sidebar.page_link("pages/24_Category_Management.py", label="Category Management", icon="⚙️")
            st.sidebar.page_link("pages/25_Application_Management.py", label="Application Management", icon="🏢")
            st.sidebar.page_link("pages/26_Feedback_Management.py", label="Feedback Management", icon="⚙️")
        elif st.session_state["role"] == "organization":
            st.sidebar.page_link("pages/31_Org_Programs.py", label="Manage Programs", icon="📋")
            st.sidebar.page_link("pages/32_Org_Applications.py", label="View Applications", icon="📝")
            st.sidebar.page_link("pages/33_Org_Settings.py", label="Organization Settings", icon="⚙️")

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("pages/00_Role_Selection.py")
