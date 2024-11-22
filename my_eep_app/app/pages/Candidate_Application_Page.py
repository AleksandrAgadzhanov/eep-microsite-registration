import streamlit as st
from app.utils import fetch_from_mongodb_by_id, update_application, create_new_application

def run():
    st.title("Candidate Application Form")
    with st.form("application_form"):
        # Input fields
        userid = st.text_input("Please enter your PSID")
        #load_button = st.form_submit_button("Load Application")

    #if load_button:
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
            which_cohort = st.selectbox("Which Cohort", ["Cohort 1", "Cohort 2", "Cohort 3", "Cohort 4"], index=["Cohort 1", "Cohort 2", "Cohort 3", "Cohort 4"].index(app.get("which_cohort", ["Cohort 1"])[0]))
            resume = st.file_uploader("Upload Resume")
            certificate = st.file_uploader("Upload Certificate")
            status = st.selectbox("Status", ["Draft", "Submitted", "Withdrawn"], index=["Draft", "Submitted", "Withdrawn"].index(app.get("status", "Draft")))

            update_button = st.form_submit_button("Update Application")
            if update_button:
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
                    "which_cohort": [which_cohort],
                    "resume": resume,
                    "certificate": certificate,
                    "status": status
                }
                update_application(app["_id"], updated_application)
                st.success("Application updated successfully!")
        else:
            # Load an empty form to be populated
            st.write("No existing application found. Please fill out the form to create a new application.")
            name = st.text_input("Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            email_functional_manager = st.text_input("Email Functional Manager")
            tech_only_role = st.selectbox("Tech Only Role", ["Yes", "No"])
            individual_or_manager = st.selectbox("Individual or Manager", ["Individual", "Manager"])
            personal_statement = st.text_area("Personal Statement")
            technologies = st.multiselect("Technologies", ["Python", "Java", "C++", "C#", "JavaScript", "SQL", "NoSQL", "HTML", "CSS", "Other"])
            which_cohort = st.selectbox("Which Cohort", ["Cohort 1", "Cohort 2", "Cohort 3", "Cohort 4"])
            resume = st.file_uploader("Upload Resume")
            certificate = st.file_uploader("Upload Certificate")
            status = st.selectbox("Status", ["Draft", "Submitted", "Withdrawn"])

            create_button = st.form_submit_button("Create Application")
            if create_button:
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
                    "which_cohort": [which_cohort],
                    "resume": resume,
                    "certificate": certificate,
                    "status": status
                }
                create_new_application(new_application)
                st.success("Application created successfully!")

if __name__ == "__main__":
    run()