import streamlit as st
import pymongo
import os
from PIL import Image
from app.utils import test_mongo_connection  # Import test_mongo_connection

# Global CSS for styling
st.markdown(
    """
    <style>
        .main-container {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 8px;
        }
        .sub-section {
            background-color: #ffffff;
            padding: 1rem;
            margin-bottom: 1.5rem;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .section-title {
            color: #34495e;
            font-size: 1.5rem;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Helper Function for Logo and Title
def logo_and_title(logo_path, title):
    col_logo, col_title = st.columns([1, 5])
    try:
        with col_logo:
            logo = Image.open(logo_path)
            st.image(logo, width=60)
        with col_title:
            st.markdown(f"<h3 style='margin-top: 5px;'>{title}</h3>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Image for {title} not found.")

# MongoDB Configuration
mongo_uri = os.getenv('MONGO_URI')
client = pymongo.MongoClient(mongo_uri)
db = client.mydatabase
collection = db.programs

# Verify MongoDB connection
if not test_mongo_connection():
    st.error("Failed to connect to MongoDB. Please check the database connection and restart the app.")
else:
    st.success("MongoDB connection verified!")

# Initialize Session States
if 'login_page' not in st.session_state:
    st.session_state.login_page = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True  # Change to `False` for testing
if 'is_staff' not in st.session_state:
    st.session_state.is_staff = False

# Sidebar Navigation
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Home", "Applicant", "Faculty", "Admin"])

    if page == "Home":
        display_home()
    elif page == "Applicant":
        from app.pages import Candidate_Application_Page
        Candidate_Application_Page.run()
    elif page == "Faculty":
        from app.pages import Faculty_Review_Page
        Faculty_Review_Page.run()
    elif page == "Admin":
        from app.pages import Admin_Page
        Admin_Page.run()

# Home Page Content with Tabs
def display_home():
    # Navigation Tabs
    tabs = st.tabs(["Home", "Overview", "Structure", "Certification", "Management", "Cost", "Faculties"])

    # Tab: Home
    with tabs[0]:
        st.markdown(
            """
            <div class="sub-section">
                <h2 class="section-title">Welcome to the Enterprise Engineer Programme</h2>
                <p>
                    This is a flagship technical talent programme designed to cultivate an enterprise mindset and 
                    develop engineers' technical and leadership skills required to achieve Vision '27.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Tab: Overview
    with tabs[1]:
        with st.container():
            logo_and_title("images/overview.jpg", "Programme Overview")
            st.markdown(
                """
                <div class="sub-section">
                    <p>The programme accelerates your technical career path, develops leadership capabilities, 
                    and fosters collaboration to deliver significant business and technical strategies.</p>
                    <ul>
                        <li>Enhance technical leadership skills.</li>
                        <li>Build a community of technical experts.</li>
                        <li>Collaborate to add value.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Tab: Structure
    with tabs[2]:
        with st.container():
            logo_and_title("images/Structure.jpg", "Programme Structure")
            st.markdown(
                """
                <div class="sub-section">
                    <p>
                        The technical training will cover key technologies such as:
                    </p>
                    <ul>
                        <li>Cloud Computing</li>
                        <li>AI/Machine Learning</li>
                        <li>Cybersecurity</li>
                        <li>Data Engineering</li>
                        <li>Blockchain</li>
                    </ul>
                    <p>
                        High-Performance Behaviors training includes 12 competencies that enhance high-performance skills.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Tab: Certification
    with tabs[3]:
        with st.container():
            logo_and_title("images/certification.jpg", "Business Assignment and Certification")
            st.markdown(
                """
                <div class="sub-section">
                    <h3>Business Assignment Project</h3>
                    <p>
                        Work in teams to complete a real business assignment project over four months. 
                        Get sign-off from business sponsors to ensure project success.
                    </p>
                    <h3>Industry Certification</h3>
                    <p>
                        Participants are required to complete one recommended industry certification to become a 
                        "Certified Enterprise Engineer."
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Tab: Management
    with tabs[4]:
        with st.container():
            logo_and_title("images/management.jpg", "Programme Management")
            st.markdown(
                """
                <div class="sub-section">
                    <p>
                        Detailed information on Programme Management will be provided here. This includes
                        faculty management, course scheduling, and operational tasks.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Tab: Cost
    with tabs[5]:
        with st.container():
            logo_and_title("images/cost.jpg", "Programme Cost")
            st.markdown(
                """
                <div class="sub-section">
                    <p>
                        The cost per candidate is around USD 9105. Costs are proportionately re-charged 
                        to the participant's GB/GFs by the COO team.
                    </p>
                    <p>
                        If a participant leaves early or does not join, their cost center absorbs the programme cost.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Tab: Faculties
    with tabs[6]:
        with st.container():
            logo_and_title("images/faculty.jpg", "Programme Faculties")
            st.markdown(
                """
                <div class="sub-section">
                    <p>
                        Details about the programme faculties will be listed here. This includes profiles of 
                        subject matter experts and their specializations.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

if __name__ == "__main__":
    main()
