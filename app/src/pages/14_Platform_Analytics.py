import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Platform Analytics",
    page_icon="📈",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("📈 Platform Analytics")


# Initialize session state for pagination
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'page_size' not in st.session_state:
    st.session_state.page_size = 10

# Tabs for different analytics
tab1, tab2 = st.tabs(["User Retention", "Program Trends"])

with tab1:
    st.markdown("### User Retention Analytics")
    try:
        response = requests.get(
            "http://api:4000/api/v1/programs/retentions",
            params={
                'page': st.session_state.page,
                'limit': st.session_state.page_size
            }
        )
        
        if response.status_code == 200:
            retention_data = response.json()
            
            if retention_data:
                # Convert to DataFrame
                df = pd.DataFrame(retention_data)
                
                # Display retention metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("User Type", df['user_type'].iloc[0])
                with col2:
                    st.metric("Avg Effectiveness", str(round(float(df['avg_effectiveness_rating'].iloc[0]), 1)))
                with col3:
                    st.metric("Avg Experience", str(round(float(df['avg_experience_rating'].iloc[0]), 1)))
                with col4:
                    st.metric("User Count", str(df['user_count'].iloc[0]))
                
                # Display retention data
                st.markdown("### User Retention Data")
                st.dataframe(df, use_container_width=True)
                
                # Create retention visualization
                st.markdown("### Retention Visualization")
                fig = px.bar(df, x='user_type', y='user_count',
                           title='User Distribution by Type',
                           labels={'user_type': 'User Type', 'user_count': 'Number of Users'})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No retention data available")
        else:
            st.error("Failed to fetch retention data")
    except Exception as e:
        st.error(f"Error: {str(e)}")

with tab2:
    st.markdown("### Program Trends")
    try:
        response = requests.get(
            "http://api:4000/api/v1/programs/trends",
            params={
                'page': st.session_state.page,
                'limit': st.session_state.page_size
            }
        )
        
        if response.status_code == 200:
            trends_data = response.json()
            
            if trends_data:
                # Convert to DataFrame
                df = pd.DataFrame(trends_data)
                
                # Convert numeric columns
                df['application_count'] = pd.to_numeric(df['application_count'])
                df['approved_count'] = pd.to_numeric(df['approved_count'])
                
                # Display trend metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Program Name", df['program_name'].iloc[0])
                with col2:
                    st.metric("Category", df['category_name'].iloc[0])
                with col3:
                    st.metric("Applications", str(df['application_count'].iloc[0]))
                with col4:
                    approval_rate = (df['approved_count'].iloc[0] / df['application_count'].iloc[0] * 100) if df['application_count'].iloc[0] > 0 else 0
                    st.metric("Approval Rate", f"{approval_rate:.1f}%")
                
                # Display trends data
                st.markdown("### Program Trends Data")
                st.dataframe(df, use_container_width=True)
                
                # Create trends visualization
                st.markdown("### Trends Visualization")
                fig = px.bar(df, x='program_name', y='application_count',
                            title='Applications by Program',
                            labels={'program_name': 'Program', 'application_count': 'Number of Applications'})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No trends data available")
        else:
            st.error("Failed to fetch trends data")
    except Exception as e:
        st.error(f"Error: {str(e)}")
