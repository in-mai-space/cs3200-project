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
    st.sidebar.page_link("pages/04_Feedback.py", label="My Feedback", icon="👤")
    st.sidebar.page_link("pages/05_Profile.py", label="My Profile", icon="👤")

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
    st.sidebar.page_link("pages/43_Add_Program.py", label="Add Program", icon="⚙️")
    st.sidebar.page_link("pages/44_Edit_Program.py", label="Edit Program", icon="⚙️")

#### ------------------------ Organization Role ------------------------
def OrganizationHomeNav():
    st.sidebar.page_link("pages/31_Org_Programs.py", label="Manage Programs", icon="📋")
    st.sidebar.page_link("pages/33_Org_Profile.py", label="Organization Profile", icon="⚙️")
    st.sidebar.page_link("pages/36_Create_Program.py", label="Create Program", icon="📋")
    st.sidebar.page_link("pages/35_Org_Edit_Program.py", label="Edit Program", icon="📝")
    
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
            st.sidebar.page_link("pages/05_Profile.py", label="My Profile", icon="👤")
        elif st.session_state["role"] == "data_analyst":
            st.sidebar.page_link("pages/13_Program_Analytics.py", label="Program Analytics", icon="📈")
            st.sidebar.page_link("pages/14_Platform_Analytics.py", label="Platform Analytics", icon="⚙️")
        elif st.session_state["role"] == "admin":
            st.sidebar.page_link("pages/21_User_Management.py", label="User Management", icon="👥")
            st.sidebar.page_link("pages/22_Program_Management.py", label="Program Management", icon="⚙️")
            st.sidebar.page_link("pages/23_Org_Management.py", label="Organization Management", icon="🏢")
            st.sidebar.page_link("pages/24_Category_Management.py", label="Category Management", icon="⚙️")
            st.sidebar.page_link("pages/25_Application_Management.py", label="Application Management", icon="🏢")
            st.sidebar.page_link("pages/26_Feedback_Management.py", label="Feedback Management", icon="⚙️")
        elif st.session_state["role"] == "organization_admin":
            st.sidebar.page_link("pages/31_Org_Programs.py", label="Manage Programs", icon="📋")
            st.sidebar.page_link("pages/33_Org_Profile.py", label="Organization Profile", icon="⚙️")

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("pages/00_Role_Selection.py")
