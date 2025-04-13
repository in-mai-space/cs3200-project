import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Admin",
    page_icon="👤",
    layout="wide"
)

# Add navigation
SideBarLinks()

st.title("👤 Admin")

with st.form("admin_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name", value=st.session_state.get('first_name', ''))
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
    
    with col2:
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        city = st.text_input("City")
        state = st.text_input("State")
        zip_code = st.text_input("ZIP Code")
    
    submitted = st.form_submit_button("Update Profile")
    if submitted:
        st.success("Profile updated successfully!")

# List view of tasks
st.header("Tasks")

# Mocks for now to get an idea of layout
tasks = [
    {
        "id": 1,
        "description": "Review new user registrations and verify email addresses.",
        "actions": ["Approve", "Reject"]
    },
    {
        "id": 2,
        "description": "Update system security patch on all servers.",
        "actions": ["Deploy", "Delay", "Cancel"]
    },
    {
        "id": 3,
        "description": "Monitor server performance and report anomalies.",
        "actions": ["View Report", "Acknowledge"]
    }
]

# Display each task in its own container
for task in tasks:
    with st.container():
        st.subheader(f"Task {task['id']}")
        st.write(task["description"])
        action_cols = st.columns(len(task["actions"]))

        for i, action in enumerate(task["actions"]):
            if action_cols[i].button(action, key=f"task{task['id']}_action{i}"):
                st.info(f"Action '{action}' taken on Task {task['id']}.")