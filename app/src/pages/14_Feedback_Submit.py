import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("Submit Feedback")

program_id = st.text_input("Program ID")
user_id = st.text_input("Your User ID")
rating = st.slider("Rating", 1, 5)
comment = st.text_area("Comments")

if st.button("Submit Feedback"):
    data = {
        "user_id": user_id,
        "rating": rating,
        "comment": comment
    }

    response = requests.post(
        f"http://localhost:5000/programs/{program_id}/feedbacks",
        json=data
    )

    if response.status_code == 201:
        st.success("Feedback submitted successfully!")
    else:
        st.error(f"Error: {response.json().get('error', 'Unknown error')}")
