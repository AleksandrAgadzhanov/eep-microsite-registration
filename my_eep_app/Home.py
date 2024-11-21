import streamlit as st
from app.utils import test_mongo_connection

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

    # Create a placeholder at the bottom of the sidebar
    # Add custom CSS to style the sidebar
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .sidebar .sidebar-content > div:last-child {
            margin-top: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    status_placeholder = st.sidebar.empty()

    if not test_mongo_connection():
        status_placeholder.error("Failed to connect to MongoDB. Please check the database connection and restart the app.")
    else:
        status_placeholder.success("MongoDB connection verified!")


if __name__ == "__main__":
    main()
