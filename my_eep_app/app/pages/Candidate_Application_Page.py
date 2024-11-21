import streamlit as st
from app.utils import upload_to_mongodb, fetch_from_mongodb_by_id
import logging

def run():
    st.title("Candidate Application Form")
    with st.form("application_form"):
        # Input fields
        userid = st.text_input("Please enter your User ID")
        lookup_button = st.form_submit_button("Lookup")

        if lookup_button:
            # Retrieve list of applications based on user id
            applications = fetch_from_mongodb_by_id("applications", userid)

            # If applications is not empty, display the list
            if applications:
                # Display list of existing applications
                for app in applications:
                    if isinstance(app, dict):
                        with st.expander(f"{app['name']} ({app['email']})"):
                            st.write(f"Status: {app['status']}")

                            # Download buttons for files
                            if app.get("resume"):
                                st.download_button(
                                    "Download CV", app["resume"], file_name=f"{app['name']}_resume.pdf"
                                )
                            if app.get("certificate"):
                                st.download_button(
                                    "Download Certificate", app["certificate"],
                                    file_name=f"{app['name']}_certificate.pdf"
                                )
                    else:
                        st.error("Invalid application data format.")

        # Additional input fields for submission
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        resume = st.file_uploader("Upload CV (PDF/Word)", type=["pdf", "docx"])
        certificate = st.file_uploader("Upload Certificates (PDF/Word)", type=["pdf", "docx"])
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Log the data to the console
            logging.info(f"User ID: {userid}")
            logging.info(f"Name: {name}")
            logging.info(f"Email: {email}")
            logging.info(f"Resume: {resume}")

            # Collect data (handle optional file uploads)
            data = {
                "userid": userid,
                "name": name,
                "email": email,
                "resume": resume.getvalue() if resume else None,  # Optional
                "certificate": certificate.getvalue() if certificate else None,  # Optional
                "status": "Under Review"
            }

            # Upload data to MongoDB
            upload_to_mongodb(data, "applications")
            st.success("Application submitted successfully!")