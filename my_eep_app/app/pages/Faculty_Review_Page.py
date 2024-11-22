import streamlit as st
from app.utils import fetch_from_mongodb, fetch_reviews_from_mongodb, update_review_in_mongodb

def run():
    st.title("Faculty Review System")

    # Fetch applications from the database
    applications = fetch_from_mongodb("applications")
    reviews = fetch_reviews_from_mongodb("reviews")

    # Filter applications with status "submitted"
    submitted_applications = [app for app in applications if app["status"] == "Submitted"]

    # Display list of submitted applications
    for app in submitted_applications:
        with st.expander(f"{app['psid']} - {app['name']} {app['last_name']}"):
            st.write("### Review Details")
            review = next((rev for rev in reviews if rev["psid"] == app["psid"]), None)
            if review:
                reviewer = st.text_input("Reviewer", value=review['reviewer'], key=f"reviewer_{app['psid']}")
                comments = st.text_area("Comments", value=review['comments'], key=f"comments_{app['psid']}")
                rating = st.selectbox("Rating", [1, 2, 3, 4, 5], index=review['rating'] - 1, key=f"rating_{app['psid']}")
                status = st.selectbox("Status", ["Under Review", "Approved", "Rejected"], index=["Under Review", "Approved", "Rejected"].index(review['status']), key=f"status_{app['psid']}")
            else:
                reviewer = st.text_input("Reviewer", key=f"reviewer_{app['psid']}")
                comments = st.text_area("Comments", key=f"comments_{app['psid']}")
                rating = st.selectbox("Rating", [1, 2, 3, 4, 5], key=f"rating_{app['psid']}")
                status = st.selectbox("Status", ["Under Review", "Approved", "Rejected"], key=f"status_{app['psid']}")

            if st.button("Save Review", key=f"save_{app['psid']}"):
                update_review_in_mongodb(app["psid"], reviewer, comments, rating, status)
                st.success("Review updated successfully!")

            st.write("### Application Details")
            st.write(f"PSID: {app['psid']}")
            st.write(f"Name: {app['name']}")
            st.write(f"Last Name: {app['last_name']}")
            st.write(f"Email: {app['email']}")
            st.write(f"Gender: {app['gender']}")
            st.write(f"Email Functional Manager: {app['email_functional_manager']}")
            st.write(f"Tech Only Role: {app['tech_only_role']}")
            st.write(f"Individual or Manager: {app['individual_or_manager']}")
            st.write(f"Personal Statement: {app['personal_statement']}")
            st.write(f"Technologies: {', '.join(app['technologies'])}")
            st.write(f"Other Technologies: {app['technologies_other']}")
            st.write(f"Which Cohort: {', '.join(app['which_cohort'])}")
            st.write(f"Status: {app['status']}")
            if app["resume"]:
                st.download_button("Download CV", app["resume"], file_name=f"{app['name']}_resume.pdf")
            if app["certificate"]:
                st.download_button("Download Certificate", app["certificate"], file_name=f"{app['name']}_certificate.pdf")

if __name__ == "__main__":
    run()