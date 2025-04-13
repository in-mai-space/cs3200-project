import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="My Applications",
    page_icon="📝",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📝 My Applications")

# Application status tabs
tab1, tab2, tab3 = st.tabs(["Pending", "Approved", "Rejected"])

with tab1:
    st.markdown("### Pending Applications")
    for i in range(2):
        with st.expander(f"Application {i+1}"):
            st.write("**Program:** Example Program")
            st.write("**Submitted:** 2024-01-01")
            st.write("**Status:** Under Review")
            if st.button("View Details", key=f"pending_{i}"):
                st.write("Application details would be shown here")

with tab2:
    st.markdown("### Approved Applications")
    for i in range(1):
        with st.expander(f"Application {i+1}"):
            st.write("**Program:** Example Program")
            st.write("**Approved:** 2024-01-15")
            st.write("**Next Steps:** Contact the organization for further instructions")

with tab3:
    st.markdown("### Rejected Applications")
    st.write("No rejected applications") 