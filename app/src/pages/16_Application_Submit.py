import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("Submit Application")

program_id = st.text_input("Program ID")
user_id = st.text_input("User ID")
status = st.selectbox("Application Status", ["pending", "approved", "rejected"])
notes = st.text_area("Notes")

if st.button("Submit Application"):
    data = {
        "user_id": user_id,
        "status": status,
        "notes": notes
    }

    response = requests.post(
        f"http://localhost:4000/api/v1/programs/{program_id}/applications",
        json=data
    )

    if response.status_code == 201:
        st.success("Application submitted successfully!")
    else:
        st.error(f"Error: {response.json().get('error', 'Unknown error')}")
