import streamlit as st
from app.utils import test_mongo_connection

if not test_mongo_connection():
    st.error("Failed to connect to MongoDB. Please check the database connection and restart the app.")
else:
    st.success("MongoDB connection verified!")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Applicant", "Faculty", "Admin"])

    if page == "Applicant":
        from app.pages import Candidate_Application_Page  # Import inside the function to avoid circular import
        Candidate_Application_Page.run()
    elif page == "Faculty":
        from app.pages import Faculty_Review_Page
        Faculty_Review_Page.run()
    elif page == "Admin":
        from app.pages import Admin_Page
        Admin_Page.run()

if __name__ == "__main__":
    main()



