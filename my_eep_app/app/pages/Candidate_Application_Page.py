import streamlit as st
from app.utils import upload_to_mongodb

def run():
    st.title("Candidate Application Form")
    with st.form("application_form"):
        # Input fields
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        resume = st.file_uploader("Upload CV (PDF/Word)", type=["pdf", "docx"])
        certificate = st.file_uploader("Upload Certificates (PDF/Word)", type=["pdf", "docx"])
        
        # Submit button
        if st.form_submit_button("Submit"):
            # Collect data (handle optional file uploads)
            data = {
                "name": name,
                "email": email,
                "resume": resume.getvalue() if resume else None,  # Optional
                "certificate": certificate.getvalue() if certificate else None,  # Optional
                "status": "Under Review"
            }
            
            # Upload data to MongoDB
            upload_to_mongodb(data, "applications")
            st.success("Application submitted successfully!")
