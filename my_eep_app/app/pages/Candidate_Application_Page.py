import re
import streamlit as st
from bson import Binary
from app.utils import fetch_from_mongodb_by_id, update_application, create_new_application

def run():
    st.title("Candidate Application Form")
    with st.form("application_form"):
        # Input fields
        userid = st.text_input("Please enter your PSID")

        # Retrieve list of applications based on user id
        applications = fetch_from_mongodb_by_id("applications", userid)

        if applications:
            # Load the first application found
            app = applications[0]
            name = st.text_input("Name", value=app.get("name", ""))
            last_name = st.text_input("Last Name", value=app.get("last_name", ""))
            email = st.text_input("Email", value=app.get("email", ""))
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(app.get("gender", "Male")))
            email_functional_manager = st.text_input("Email Functional Manager", value=app.get("email_functional_manager", ""))
            tech_only_role = st.selectbox("Tech Only Role", ["Yes", "No"], index=["Yes", "No"].index(app.get("tech_only_role", "Yes")))
            individual_or_manager = st.selectbox("Individual or Manager", ["Individual", "Manager"], index=["Individual", "Manager"].index(app.get("individual_or_manager", "Individual")))
            personal_statement = st.text_area("Personal Statement", value=app.get("personal_statement", ""))
            technologies = st.multiselect("Technologies", ["Python", "Java", "C++", "C#", "JavaScript", "SQL", "NoSQL", "HTML", "CSS", "Other"], default=app.get("technologies", []))
            # technologies_other = st.text_area("Other Technologies", value=app.get("technologies_other", ""))
            which_cohort = st.selectbox("Which Cohort", ["Cohort 5 (the best, of course)","Cohort 1", "Cohort 2", "Cohort 3", "Cohort 4"], index=["Cohort 5 (the best, of course)","Cohort 1", "Cohort 2", "Cohort 3", "Cohort 4"].index(app.get("which_cohort", ["Not Entered"])[0]))
            resume = st.file_uploader("Upload Resume", type=["pdf", "docx"])
            certificate = st.file_uploader("Upload Certificate", type=["pdf", "docx"])
            status = st.selectbox("Status", ["Draft", "Submitted", "Withdrawn"], index=["Draft", "Submitted", "Withdrawn"].index(app.get("status", "Draft")))

            update_button = st.form_submit_button("Update Application")
            if update_button:
                resume_data = resume.read() if resume is not None else app.get("resume")
                certificate_data = certificate.read() if certificate is not None else app.get("certificate")
                updated_application = {
                    "psid": userid,
                    "name": name,
                    "last_name": last_name,
                    "email": email,
                    "gender": gender,
                    "email_functional_manager": email_functional_manager,
                    "tech_only_role": tech_only_role,
                    "individual_or_manager": individual_or_manager,
                    "personal_statement": personal_statement,
                    "technologies": technologies,
                    # "technologies_other": technologies_other,
                    "which_cohort": [which_cohort],
                    "resume": Binary(resume_data) if resume_data else None,
                    "certificate": Binary(certificate_data) if certificate_data else None,
                    "status": status
                }
                update_application(app["_id"], updated_application)
                st.success("Application updated successfully!")
        else:
            # Load an empty form to be populated
            st.write("No existing application found. Please fill out the form to create a new application.")
            name = st.text_input("Name", max_chars=50)
            last_name = st.text_input("Last Name", max_chars=50)
            email = st.text_input("Email", value="", placeholder="Enter your email address")
            if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Please enter a valid email address.")
            gender = st.selectbox("Gender", ["Not Entered","Male", "Female", "Other"])
            email_functional_manager = st.text_input("Email Functional Manager",  placeholder="Enter your manager's email address")
            if email_functional_manager and not re.match(r"[^@]+@[^@]+\.[^@]+", email_functional_manager):
                st.error("Please enter a valid email address.")
            tech_only_role = st.selectbox("Tech Only Role", ["Not Selected","Yes", "No"])
            individual_or_manager = st.selectbox("Individual or Manager", ["Not Selected","Individual", "Manager"])
            personal_statement = st.text_area("Personal Statement", max_chars=8192)
            technologies = st.multiselect("Technologies", ["Python", "Java", "C++", "C#", "JavaScript", "SQL", "NoSQL", "HTML", "CSS", "Other"], help="Select all that apply")
            # technologies_other = st.text_area("Other Technologies", help="Please specify other technologies not listed above", max_chars=8192)
            which_cohort = st.selectbox("Which Cohort", ["Not Entered","Cohort 5 (the best, of course)","Cohort 1", "Cohort 2", "Cohort 3", "Cohort 4"])
            resume = st.file_uploader("Upload Resume", type=["pdf", "docx"], help="Please upload your resume in PDF or DOCX format")
            certificate = st.file_uploader("Upload Certificate", type=["pdf", "docx"], help="Please upload any certifications in PDF or DOCX format")
            status = st.selectbox("Status", ["Draft", "Submitted", "Withdrawn"], help="Draft: Application in progress, Submitted: Application submitted, Withdrawn: Application withdrawn")

            create_button = st.form_submit_button("Create Application")
            if create_button:
                resume_data = resume.read() if resume is not None else None
                certificate_data = certificate.read() if certificate is not None else None
                new_application = {
                    "psid": userid,
                    "name": name,
                    "last_name": last_name,
                    "email": email,
                    "gender": gender,
                    "email_functional_manager": email_functional_manager,
                    "tech_only_role": tech_only_role,
                    "individual_or_manager": individual_or_manager,
                    "personal_statement": personal_statement,
                    "technologies": technologies,
                    # "technologies_other": technologies_other.split("\n") if technologies_other else "",
                    "which_cohort": [which_cohort],
                    "resume": Binary(resume_data) if resume_data else None,
                    "certificate": Binary(certificate_data) if certificate_data else None,
                    "status": status
                }
                create_new_application(new_application)
                st.success("Application created successfully!")

if __name__ == "__main__":
    run()