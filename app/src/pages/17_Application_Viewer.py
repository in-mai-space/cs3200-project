import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("View / Edit Application")

application_id = st.text_input("Enter Application ID")

if st.button("Fetch Application"):
    response = requests.get(f"http://localhost:4000/api/v1/applications/{application_id}")

    if response.status_code == 200:
        app_data = response.json()

        st.subheader("Current Application Info")
        st.json(app_data)

        # Editable fields
        new_status = st.selectbox("Update Status", ["pending", "approved", "rejected"], index=["pending", "approved", "rejected"].index(app_data["status"]))
        new_notes = st.text_area("Update Notes", value=app_data["notes"])

        if st.button("Update Application"):
            update_payload = {
                "status": new_status,
                "notes": new_notes
            }

            update_response = requests.put(
                f"http://localhost:4000/api/v1/applications/{application_id}",
                json=update_payload
            )

            if update_response.status_code == 200:
                st.success("Application updated successfully!")
            else:
                st.error("Failed to update application.")

    else:
        st.error("Application not found.")
