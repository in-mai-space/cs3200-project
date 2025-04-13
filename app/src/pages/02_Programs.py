import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Browse Programs",
    page_icon="📋",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📋 Available Programs")

# Search and filter section
col1, col2 = st.columns(2)
with col1:
    search_query = st.text_input("Search programs")
with col2:
    category = st.selectbox("Filter by category", ["All", "Education", "Housing", "Healthcare", "Employment"])

# Programs list
st.markdown("""
## Programs
""")

# Example program cards
for i in range(3):
    with st.expander(f"Program {i+1}"):
        st.write("**Organization:** Example Organization")
        st.write("**Description:** This is a sample program description.")
        st.write("**Eligibility:** Open to all qualified applicants")
        if st.button("Apply Now", key=f"apply_{i}"):
            st.switch_page("pages/03_Applications.py") 