import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📊 Admin Dashboard")

# Visualization type selector
viz_type = st.selectbox(
    "Select Visualization Type",
    ["Program Distribution", "Application Trends", "User Demographics", "Performance Metrics"]
)

# Date range
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date")
with col2:
    end_date = st.date_input("End Date")

# Visualization options
st.markdown("### Visualization Options")
col1, col2 = st.columns(2)
with col1:
    chart_type = st.selectbox(
        "Chart Type",
        ["Bar Chart", "Line Chart", "Pie Chart", "Area Chart"]
    )
with col2:
    aggregation = st.selectbox(
        "Aggregation",
        ["Daily", "Weekly", "Monthly", "Quarterly"]
    )

# Generate visualization
if st.button("Generate Visualization"):
    st.success("Visualization generated successfully!")
    
    # Sample visualizations
    st.markdown("### Program Distribution")
    st.bar_chart({
        "Program A": 100,
        "Program B": 150,
        "Program C": 200,
        "Program D": 250
    })
    
    st.markdown("### Application Trends")
    st.line_chart({
        "Applications": [100, 150, 200, 250, 300],
        "Approvals": [80, 120, 160, 200, 240]
    })
    
    st.markdown("### User Demographics")
    st.pie_chart({
        "Age 18-24": 25,
        "Age 25-34": 35,
        "Age 35-44": 20,
        "Age 45+": 20
    })
    
    st.markdown("### Performance Metrics")
    st.area_chart({
        "Processing Time": [5, 4, 3, 2, 1],
        "Approval Rate": [70, 75, 80, 85, 90]
    }) 