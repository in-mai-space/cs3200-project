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

# Initialize session state for infinite scroll
if 'all_retention_data' not in st.session_state:
    st.session_state.all_retention_data = []
if 'all_trends_data' not in st.session_state:
    st.session_state.all_trends_data = []
if 'retention_page' not in st.session_state:
    st.session_state.retention_page = 1
if 'trends_page' not in st.session_state:
    st.session_state.trends_page = 1
if 'page_size' not in st.session_state:
    st.session_state.page_size = 20  # Increased page size
if 'has_more_retention' not in st.session_state:
    st.session_state.has_more_retention = True
if 'has_more_trends' not in st.session_state:
    st.session_state.has_more_trends = True

# Tabs for different analytics
tab1, tab2 = st.tabs(["User Retention", "Program Trends"])

with tab1:
    st.markdown("### User Retention Analytics")
    
    def load_more_retention():
        try:
            response = requests.get(
                "http://api:4000/api/v1/programs/retentions",
                params={
                    'page': st.session_state.retention_page,
                    'limit': st.session_state.page_size
                }
            )
            
            if response.status_code == 200:
                new_data = response.json()
                if new_data:
                    st.session_state.all_retention_data.extend(new_data)
                    st.session_state.retention_page += 1
                    st.session_state.has_more_retention = len(new_data) == st.session_state.page_size
                else:
                    st.session_state.has_more_retention = False
            else:
                st.error(f"Failed to fetch retention data: {response.status_code}")
        except Exception as e:
            st.error(f"Error loading more retention data: {str(e)}")
    
    # Load initial retention data if needed
    if not st.session_state.all_retention_data and st.session_state.has_more_retention:
        load_more_retention()
    
    if st.session_state.all_retention_data:
        # Convert to DataFrame
        df = pd.DataFrame(st.session_state.all_retention_data)
        
        # Convert string values to numeric, handling any invalid values
        numeric_columns = ['avg_effectiveness_rating', 'avg_experience_rating', 'avg_simplicity_rating', 'avg_recommendation_rating']
        for col in numeric_columns:
            if col in df.columns:
                # First try to convert to float, replacing any invalid values with NaN
                df[col] = pd.to_numeric(df[col], errors='coerce')
                # Then fill NaN values with 0
                df[col] = df[col].fillna(0)
        
        # Display retention metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total User Types", str(len(df)))
        with col2:
            st.metric("Avg Effectiveness", f"{df['avg_effectiveness_rating'].mean():.1f}")
        with col3:
            st.metric("Avg Experience", f"{df['avg_experience_rating'].mean():.1f}")
        with col4:
            st.metric("Total Users", str(df['user_count'].sum()))
        
        # Display retention data
        st.markdown("### User Retention Data")
        st.dataframe(df, use_container_width=True)
        
        # Create retention visualization
        st.markdown("### Retention Visualization")
        fig = px.bar(df, x='user_type', y='user_count',
                    title='User Distribution by Type',
                    labels={'user_type': 'User Type', 'user_count': 'Number of Users'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Load more button
        if st.session_state.has_more_retention:
            if st.button("Load More Retention Data"):
                load_more_retention()
                st.rerun()
    else:
        st.info("No retention data available")

with tab2:
    st.markdown("### Program Trends")
    
    def load_more_trends():
        try:
            response = requests.get(
                "http://api:4000/api/v1/programs/trends",
                params={
                    'page': st.session_state.trends_page,
                    'limit': st.session_state.page_size
                }
            )
            
            if response.status_code == 200:
                new_data = response.json()
                if new_data:
                    st.session_state.all_trends_data.extend(new_data)
                    st.session_state.trends_page += 1
                    st.session_state.has_more_trends = len(new_data) == st.session_state.page_size
                else:
                    st.session_state.has_more_trends = False
            else:
                st.error(f"Failed to fetch trends data: {response.status_code}")
        except Exception as e:
            st.error(f"Error loading more trends data: {str(e)}")
    
    # Load initial trends data if needed
    if not st.session_state.all_trends_data and st.session_state.has_more_trends:
        load_more_trends()
    
    if st.session_state.all_trends_data:
        # Convert to DataFrame
        df = pd.DataFrame(st.session_state.all_trends_data)
        
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
        
        # Load more button
        if st.session_state.has_more_trends:
            if st.button("Load More Trends Data"):
                load_more_trends()
                st.rerun()
    else:
        st.info("No trends data available")
