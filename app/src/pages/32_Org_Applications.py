import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Organization Applications",
    page_icon="📝",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📝 Organization Applications")

# Search and filter
col1, col2, col3 = st.columns(3)
with col1:
    search_query = st.text_input("Search applications")
with col2:
    program_filter = st.selectbox("Filter by program", ["All", "Program A", "Program B", "Program C"])
with col3:
    status_filter = st.selectbox("Filter by status", ["All", "Pending", "Approved", "Rejected"])

# Application list
st.markdown("### Application List")
st.dataframe({
    "Applicant": ["John Doe", "Jane Smith", "Bob Johnson"],
    "Program": ["Program A", "Program B", "Program C"],
    "Status": ["Pending", "Approved", "Rejected"],
    "Submitted": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "Last Updated": ["2024-01-15", "2024-01-16", "2024-01-17"]
})

# Application actions
st.markdown("### Application Actions")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Review Application", type='primary', use_container_width=True):
        st.switch_page("pages/33_Review_Application.py")
with col2:
    if st.button("Update Status", type='primary', use_container_width=True):
        st.switch_page("pages/33_Update_Status.py")
with col3:
    if st.button("Send Message", type='secondary', use_container_width=True):
        st.switch_page("pages/33_Send_Message.py")

# Application details
with st.expander("Application Details"):
    st.write("**Applicant:** John Doe")
    st.write("**Program:** Program A")
    st.write("**Status:** Pending")
    st.write("**Submitted:** 2024-01-01")
    st.write("**Last Updated:** 2024-01-15")
    st.write("**Eligibility Status:** Eligible")
    st.write("**Documents Submitted:** Yes")
    st.write("**Notes:** Application under review")

# Application statistics
st.markdown("### Application Statistics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Applications", "100", "+5%")
with col2:
    st.metric("Pending Review", "15", "+2%")
with col3:
    st.metric("Approved", "80", "+10%")
with col4:
    st.metric("Rejected", "5", "-3%") 