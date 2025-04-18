import streamlit as st
import requests

# Set page configuration
st.set_page_config(
    page_title="Role Selection",
    page_icon="👥",
    layout="wide"
)

# Main content
st.title("👋 Welcome to Uplift, a platform for connecting people to free and beneficial programs.")
st.markdown("### Select your role to continue")

# Create two rows of two columns each
col1, col2 = st.columns(2)

def load_users():
    try:
        response = requests.get("http://api:4000/api/v1/users?type=user")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to load users: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error loading users: {str(e)}")
        return []

with col1:
    # User Role
    st.markdown("### 👤 Regular User")
    st.markdown("Browse and apply for programs")
    
    users = load_users()
    if users:
        user_options = {f"{user['first_name']} {user['last_name']}": user for user in users}
        selected_user_name = st.selectbox(
            "Select User",
            options=list(user_options.keys()),
            index=0,
            key="user_select"
        )
        
        if st.button("Act as Selected User", key="user", use_container_width=True):
            selected_user = user_options[selected_user_name]
            st.session_state["role"] = "user"
            st.session_state["authenticated"] = True
            st.session_state["first_name"] = selected_user["first_name"]
            st.session_state["user_id"] = selected_user["id"]
            st.switch_page("pages/01_Organizations.py")
    else:
        st.error("No users available")

    st.markdown("---")

    # Analyst Role
    st.markdown("### 📊 Data Analyst")
    st.markdown("**Ernest**")
    st.markdown("Access analytics and reporting tools")
    if st.button("Act as Ernest", key="analyst", use_container_width=True):
        st.session_state["role"] = "data_analyst"
        st.session_state["authenticated"] = True
        st.session_state["first_name"] = "Ernest"
        st.switch_page("pages/13_Program_Analytics.py")

with col2:
    # Admin Role
    st.markdown("### 🔑 System Administrator")
    st.markdown("**Garrett Ladley**")
    st.markdown("Manage system settings and users")
    if st.button("Act as Garrett Ladley", key="admin", use_container_width=True):
        st.session_state["role"] = "admin"
        st.session_state["authenticated"] = True
        st.session_state["first_name"] = "Garrett Ladley"
        st.switch_page("pages/21_User_Management.py")

    st.markdown("---")

    # Organization Role
    st.markdown("### 🏢 Organization")
    st.markdown("**Bob**")
    st.markdown("Manage programs and applications")
    
    # Load organizations if not already loaded
    if 'organizations' not in st.session_state:
        try:
            response = requests.get("http://api:4000/api/v1/organizations")
            if response.status_code == 200:
                st.session_state.organizations = response.json()
            else:
                st.session_state.organizations = []
        except Exception as e:
            st.error(f"Error loading organizations: {str(e)}")
            st.session_state.organizations = []
    
    # Organization selection
    if st.session_state.organizations:
        organization_options = {f"{org['name']}": org['id'] for org in st.session_state.organizations}
        selected_org_name = st.selectbox(
            "Select Organization",
            options=list(organization_options.keys()),
            index=0
        )
        
        if st.button("Act as Bob", key="org", use_container_width=True):
            st.session_state["role"] = "organization_admin"
            st.session_state["authenticated"] = True
            st.session_state["first_name"] = "Bob"
            st.session_state["selected_organization_id"] = organization_options[selected_org_name]
            st.switch_page("pages/31_Org_Programs.py")
    else:
        st.error("No organizations available")