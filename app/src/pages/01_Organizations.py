import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Browse Organizations",
    page_icon="📋",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📋 Available Organizations")

# Search and filter section
col1, col2 = st.columns(2)
with col1:
    search_query = st.text_input("Search organizations")
with col2:
    category = st.selectbox("Filter by category", ["All", "Education", "Housing", "Healthcare", "Employment"])

# Programs list
st.markdown("""
## Organizations
""")

# Example program cards
for i in range(3):
    with st.expander(f"Organization {i+1}"):
        st.write("**Organization:** Example Organization")
        st.write("**Description:** This is a sample organization description.")
        st.write("**Eligibility:** Open to all qualified applicants")
        if st.button("Apply Now", key=f"apply_{i}"):
            st.switch_page("pages/03_Applications.py") 