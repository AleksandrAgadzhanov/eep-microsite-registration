import streamlit as st
from app.utils import upload_to_mongodb, fetch_from_mongodb_by_id
import logging

def run():
    st.title("Candidate Application Form")
    with st.form("application_form"):
        # Input fields
        userid = st.text_input("Please enter your PSID")
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

        # TODO: Additional input fields for submission
        name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email Address")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        email_functional_manager = st.text_input("Email Address of Your Functional Manager")
        tech_only_role = st.selectbox("Tech Only Role", ["Yes", "No"])
        individual_or_manager = st.selectbox("Are you an Individual contributor or a People Manager", ["Individual", "Manager"])
        personal_statement = st.text_area("Personal Statement")
        technologies_checkbox = st.multiselect("Technologies", ["Python", "Java", "C++", "C#", "JavaScript", "SQL", "NoSQL", "HTML", "CSS", "Other"])
        which_cohort = st.multiselect("Which Cohort", ["Cohort 1", "Cohort 2", "Cohort 3", "Cohort 4"])
        resume = st.file_uploader("Upload CV (PDF/Word)", type=["pdf", "docx"])
        certificate = st.file_uploader("Upload Certificates (PDF/Word)", type=["pdf", "docx"])
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Log the data to the console
            logging.info(f"User ID: {userid}")
            logging.info(f"Name: {name}")
            logging.info(f"Last Name: {last_name}")
            logging.info(f"Email: {email}")
            logging.info(f"Gender: {gender}")
            logging.info(f"Email Functional Manager: {email_functional_manager}")
            logging.info(f"Tech Only Role: {tech_only_role}")
            logging.info(f"Individual or Manager: {individual_or_manager}")
            logging.info(f"Personal Statement: {personal_statement}")
            logging.info(f"Technologies: {technologies_checkbox}")
            logging.info(f"Which Cohort: {which_cohort}")
            logging.info(f"Resume: {resume}")
            logging.info(f"Certificate: {certificate}")

            # Collect data (handle optional file uploads)
            data = {
                "userid": userid,
                "name": name,
                "last_name": last_name,
                "email": email,
                "gender": gender,
                "email_functional_manager": email_functional_manager,
                "tech_only_role": tech_only_role,
                "individual_or_manager": individual_or_manager,
                "personal_statement": personal_statement,
                "technologies": technologies_checkbox,
                "which_cohort": which_cohort,
                "resume": resume.getvalue() if resume else None,  # Optional
                "certificate": certificate.getvalue() if certificate else None,  # Optional
                "status": "Under Review" # draft, submitted, withdrawn
            }

            # Upload data to MongoDB
            upload_to_mongodb(data, "applications")
            st.success("Application submitted successfully!")