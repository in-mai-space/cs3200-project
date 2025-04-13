import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Reports",
    page_icon="📊",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📊 Reports")

# Report type selector
report_type = st.selectbox(
    "Select Report Type",
    ["Program Performance", "Application Statistics", "User Activity", "System Usage"]
)

# Date range
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date")
with col2:
    end_date = st.date_input("End Date")

# Generate report button
if st.button("Generate Report"):
    st.success("Report generated successfully!")
    
    # Report content
    st.markdown("### Report Summary")
    st.write("""
    This report covers the selected period and provides insights into:
    - Program performance metrics
    - Application processing statistics
    - User engagement patterns
    - System utilization rates
    """)
    
    # Sample data
    st.markdown("### Key Findings")
    st.dataframe({
        "Metric": ["Total Programs", "Active Applications", "Approval Rate", "Processing Time"],
        "Value": [150, 1234, "78%", "3.2 days"],
        "Change": ["+5%", "+12%", "+3%", "-0.5 days"]
    })
    
    # Export options
    st.markdown("### Export Report")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button("Download PDF", "report.pdf", "application/pdf")
    with col2:
        st.download_button("Download CSV", "report.csv", "text/csv")
    with col3:
        st.download_button("Download Excel", "report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") 