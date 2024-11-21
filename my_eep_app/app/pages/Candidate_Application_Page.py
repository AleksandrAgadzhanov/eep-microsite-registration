import streamlit as st
from app.utils import upload_to_mongodb, fetch_from_mongodb_by_id
import logging

def run():
    st.title("Candidate Application Form")

    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    default_name = ""
    if "selected_app" not in st.session_state:
        st.session_state.selected_app = {}
    selected_app = st.session_state.get("selected_app", {})

    with st.form("application_form"):
        # Input fields
        userid = st.text_input("Please enter your PSID")
        lookup_button = st.form_submit_button("Lookup")

        if lookup_button:
            # Retrieve list of applications based on user id
            applications = fetch_from_mongodb_by_id("applications", userid)

            # If applications is not empty, display the list
            if applications:
                # Create a dropdown list of applications
                app_options = ["Not Selected", "New Application"] + [f"{app['name']} ({app['email']})" for app in applications]
                selected_app_label = st.selectbox("Select an application to view details", app_options, key="selected_app")

                # Find the selected application object and store the selected key
                if selected_app_label not in ["Not Selected", "New Application"]:
                    selected_app = next(app for app in applications if f"{app['name']} ({app['email']})" == selected_app_label)
                    st.session_state.selected_app = selected_app
                    st.session_state.selected_key = selected_app_label
            else:
                st.warning("No applications found for this user. Please proceed with the application form.")

        continue_button = st.form_submit_button("Continue")

    with st.form("application_form2"):

        if continue_button and selected_app != "Not Selected":
            st.info("Please fill out the application form below.")

            # Retrieve the name from the selected application
            default_name = selected_app.get('name', "")

            name = st.text_input("First Name", value=default_name, key="name")
            last_name = st.text_input("Last Name", key="last_name")
            email = st.text_input("Email Address", key="email")
            gender = st.selectbox("Gender", ["Not Selected", "Male", "Female", "Other"], key="gender")
            email_functional_manager = st.text_input("Email Address of Your Functional Manager", key="email_functional_manager")
            tech_only_role = st.selectbox("Tech Only Role", ["Not Selected","Yes", "No"], key="tech_only_role")
            individual_or_manager = st.selectbox("Are you an Individual contributor or a People Manager", ["Not Selected","Individual", "Manager"], key="individual_or_manager")
            personal_statement = st.text_area("Personal Statement", key="personal_statement")
            technologies_checkbox = st.multiselect("Technologies", ["Python", "Java", "C++", "C#", "JavaScript", "SQL", "NoSQL", "HTML", "CSS", "Other"], key="technologies_checkbox")
            if st.form_submit_button("Other Technologies"):
                other_technology = st.text_input("Please specify the other technologies", key="other_technology")

            which_cohort = st.multiselect("Which Cohort", ["Not Selected","Cohort 1", "Cohort 2", "Cohort 3", "Cohort 4", "Cohort 5"], help="See the program details for cohort information", key="which_cohort")
            resume = st.file_uploader("Upload CV (PDF/Word)", type=["pdf", "docx"], key="resume")
            certificate = st.file_uploader("Upload Certificates (PDF/Word)", type=["pdf", "docx"], key="certificate")
            submit_button = st.form_submit_button("Submit")

            # Log the data to the console
            logging.debug(f"User ID: {userid}")
            logging.debug(f"Name: {name}")
            logging.debug(f"Last Name: {last_name}")
            logging.debug(f"Email: {email}")
            logging.debug(f"Gender: {gender}")
            logging.debug(f"Email Functional Manager: {email_functional_manager}")
            logging.debug(f"Tech Only Role: {tech_only_role}")
            logging.debug(f"Individual or Manager: {individual_or_manager}")
            logging.debug(f"Personal Statement: {personal_statement}")
            logging.debug(f"Technologies: {technologies_checkbox}")
            logging.debug(f"Which Cohort: {which_cohort}")
            logging.debug(f"Resume: {resume}")
            logging.debug(f"Certificate: {certificate}")

            # Submit button
            if submit_button:
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
                    "other_technology": other_technology,
                    "which_cohort": which_cohort,
                    "resume": resume.getvalue() if resume else None,  # Optional
                    "certificate": certificate.getvalue() if certificate else None,  # Optional,
                    "status": "Under Review"  # draft, submitted, withdrawn
                }

                # Upload data to MongoDB
                upload_to_mongodb(data, "applications")
                st.success("Application submitted successfully!")