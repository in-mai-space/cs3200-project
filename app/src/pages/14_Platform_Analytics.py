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
