import streamlit as st

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

with col1:
    # User Role
    st.markdown("### 👤 Regular User")
    st.markdown("**Cornelius the Fifth**")
    st.markdown("Browse and apply for programs")
    if st.button("Act as Cornelius the Fifth", key="user", use_container_width=True):
        st.session_state["role"] = "user"
        st.session_state["authenticated"] = True
        st.session_state["first_name"] = "Cornelius the Fifth"
        st.switch_page("pages/02_Programs.py")

    st.markdown("---")

    # Analyst Role
    st.markdown("### 📊 Data Analyst")
    st.markdown("**Ernest**")
    st.markdown("Access analytics and reporting tools")
    if st.button("Act as Ernest", key="analyst", use_container_width=True):
        st.session_state["role"] = "analyst"
        st.session_state["authenticated"] = True
        st.session_state["first_name"] = "Ernest"
        st.switch_page("pages/13_Program_Analytics.py")

with col2:
    # Admin Role
    st.markdown("### 🔑 System Administrator")
    st.markdown("**Garrett Ladley**")
    st.markdown("Manage system settings and users")
    if st.button("Act as Garrett Ladley", key="admin", use_container_width=True):
        st.session_state["role"] = "administrator"
        st.session_state["authenticated"] = True
        st.session_state["first_name"] = "Garrett Ladley"
        st.switch_page("pages/21_User_Management.py")

    st.markdown("---")

    # Organization Role
    st.markdown("### 🏢 Organization")
    st.markdown("**Bob**")
    st.markdown("Manage programs and applications")
    if st.button("Act as Bob", key="org", use_container_width=True):
        st.session_state["role"] = "organization"
        st.session_state["authenticated"] = True
        st.session_state["first_name"] = "Bob"
        st.switch_page("pages/31_Org_Programs.py")