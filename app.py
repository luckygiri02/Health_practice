import streamlit as st
from utils import grant_access, get_access_logs, get_health_trends
from api import upload_record, book_appointment, get_patient_data

st.set_page_config(page_title="Health Records Management")
role = st.sidebar.selectbox("Login as", ["Patient", "Doctor"])

if role == "Patient":
    st.title("Patient Dashboard")

    patient_id = st.text_input("Patient ID")

    st.subheader("Upload Health Record")
    uploaded_file = st.file_uploader("Choose a file")
    record_type = st.selectbox("Record Type", ["Lab Report", "Prescription", "Other"])
    if st.button("Upload") and uploaded_file:
        result = upload_record(patient_id, uploaded_file, record_type)
        st.success(result)

    st.subheader("Grant Access to Doctor")
    doc_name = st.text_input("Doctor Name to Grant Access")
    if st.button("Grant Access"):
        grant_access(patient_id, doc_name)
        st.success(f"Access granted to Dr. {doc_name}")

    st.subheader("My Records")
    if patient_id:
        patient_data = get_patient_data(patient_id)
        st.json(patient_data)

        st.subheader("Access Logs")
        logs = get_access_logs(patient_id)
        st.json(logs)

elif role == "Doctor":
    st.title("Doctor Dashboard")

    search_id = st.text_input("Enter Patient ID")
    doctor_name = st.text_input("Your Name")

    if st.button("Search"):
        patient_data = get_patient_data(doctor_name, search_id, role="Doctor")
        if "message" in patient_data:
            st.error(patient_data["message"])
        else:
            st.json(patient_data)

            st.subheader("Book Appointment")
            date = st.date_input("Select Date")
            if st.button("Confirm Appointment"):
                result = book_appointment(search_id, doctor_name, str(date))
                st.success(result)

            st.subheader("Health Trends")
            trends = get_health_trends(search_id)
            st.json(trends)
