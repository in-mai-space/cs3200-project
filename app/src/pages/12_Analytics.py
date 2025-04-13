import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📈 Analytics Dashboard")

# Date range selector
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date")
with col2:
    end_date = st.date_input("End Date")

# Metrics
st.markdown("### Key Metrics")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
with metric_col1:
    st.metric("Total Programs", "150", "+5%")
with metric_col2:
    st.metric("Active Applications", "1,234", "+12%")
with metric_col3:
    st.metric("Approval Rate", "78%", "+3%")
with metric_col4:
    st.metric("Average Processing Time", "3.2 days", "-0.5 days")

# Charts
st.markdown("### Program Statistics")
tab1, tab2, tab3 = st.tabs(["Applications by Program", "Approval Rates", "Processing Times"])

with tab1:
    st.bar_chart({"Applications": [100, 150, 200, 250, 300]})

with tab2:
    st.line_chart({"Approval Rate": [70, 75, 80, 85, 90]})

with tab3:
    st.area_chart({"Processing Time (days)": [5, 4, 3, 2, 1]}) 