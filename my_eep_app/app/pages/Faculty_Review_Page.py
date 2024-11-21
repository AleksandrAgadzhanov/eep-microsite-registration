import streamlit as st
from app.utils import fetch_from_mongodb, update_application_status

def run():
    st.title("Faculty Review System")
    
    # Fetch applications from the database
    applications = fetch_from_mongodb("applications")
    
    # Loop through applications to display each one
    for app in applications:
        with st.expander(f"{app['name']} ({app['email']})"):
            st.write(f"Status: {app['status']}")
            
            # Download buttons for files
            if app["resume"]:
                st.download_button(
                    "Download CV", app["resume"], file_name=f"{app['name']}_resume.pdf"
                )
            if app["certificate"]:
                st.download_button(
                    "Download Certificate", app["certificate"], file_name=f"{app['name']}_certificate.pdf"
                )
            
            # Unique key for each selectbox and button
            new_status = st.selectbox(
                "Change Status", 
                ["Draft","Under Review", "Approved", "Rejected"], 
                index=["Under Review", "Approved", "Rejected"].index(app["status"]), 
                key=f"status_{app['_id']}"  # Unique key based on application ID
            )
            if st.button("Update Status", key=f"update_{app['_id']}"):
                update_application_status(app["_id"], new_status)
                st.success(f"Status updated for {app['name']}!")
