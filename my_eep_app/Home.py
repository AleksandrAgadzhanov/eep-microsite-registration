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
    tabs = st.tabs(["Home", "Overview", "Structure", "Certification", "Management", "Cost", "Faculties", "Target Audience"])

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
                    <p>Enterprise Engineer Programme is a flagship technical talent programme and part of the Dynamic, Rewarding Career initiative of the People Pillar of Vision '27 to cultivate an enterprise mindset and develop engineers' current and future technical skills required to achieve Vision '27</p>
                    <ul>
                        <li>To accelerate your technical career path and to get the best out of our technical talent.</li>
                        <li>To build technical leadership capabilities necessary to deliver on our most significant business and technical strategies and challenges.</li>
                        <li>To grow our community of technical experts who collaborate to add value.</li>
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
                        High Performance Behaviors training includes 12 competencies that help enhance the high-performance skills and enterprise mindset. This training is done by our vendor partner and leading training provider, "Davies - Group".
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
                        Participants will work in teams to complete a real business assignment project over 4 months of the programme and get sign-off from business sponsors.
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
                        The cost of the programme per candidate is around USD 9105. The programme costs are proportionately
                        re-charged to the participant's GB/GFs by the COO team.
                    </p>
                    <p>
                        If for any reason, any participant leaves the programme before completion or does not join after
                        seat confirmation and a replacement cannot be identified, the entire programme cost will be
                        absorbed by the participant's cost center.
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

        # Tab: Target Audience
        with tabs[7]:
            with st.container():
                logo_and_title("images/target_audience.jpg","Target Audience")
                st.subheader("Eligibility")
                st.markdown(
                    """
                    <div class="sub-section">
                        <p>
                            - Permanent employees of HSBC Technology across all GB/GFs globally <br>
                            - Active employees only (i.e. those who are not serving probation, notice period, performance 
                              improvement plan or on sabbatical/long sick leave <br>
                            - Completed at least 2 annual performance reviews
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.divider()
                st.subheader("Role Specification")
                st.markdown(
                    """
                    <div class="sub-section">
                        <p>
                            - GCB 5-6 <br>
                            - GCB 4 (promoted to GC 4 from within the last 2 years) <br>
                            - Performing in a purely technical role (e.g. developer/code, tester, product support,
                              application and infrastructure support, etc.)
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.divider()
                st.subheader("Aspirations")
                st.markdown(
                    """
                    <div class="sub-section">
                        <p>
                            - Take on new challenges in the current role <br>
                            - Explore technologies outside of the current work <br>
                            - Continue learning at all stages of the career development
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.divider()
                st.subheader("Meetup (Webinars)")
                st.markdown(
                    """
                    <div class="sub-section">
                        <p>
                            - Please register for on of the sessions on Meetup to know more about the EEP self-nomination process
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.divider()

if __name__ == "__main__":
    main()
