from utils import (
    save_record, get_records, add_appointment,
    is_access_granted, log_access, get_access_logs,
    get_health_trends, grant_access
)
import datetime

def upload_record(patient_id, uploaded_file, record_type):
    if uploaded_file.type not in ["application/pdf", "image/png", "image/jpeg", "text/plain"]:
        return "Invalid file type"

    content = uploaded_file.read()
    summary = f"{uploaded_file.name}: {len(content)} bytes"
    record = {
        "Type": record_type,
        "Summary": summary,
        "Access Granted To": []
    }
    save_record(patient_id, record)
    return f"{record_type} record saved successfully."

def book_appointment(patient_id, doctor_name, date):
    if not is_access_granted(patient_id, doctor_name):
        return "Access not granted by patient."

    appointment = {
        "Doctor": doctor_name,
        "Date": date,
        "Status": "Confirmed"
    }
    add_appointment(patient_id, appointment)
    return "Appointment booked successfully."

def get_patient_data(requester_id, patient_id=None, role="Patient"):
    target_id = patient_id if patient_id else requester_id
    data = get_records(target_id)
    if not data:
        return {"message": "No records found."}

    if role == "Doctor":
        if not is_access_granted(target_id, requester_id):
            return {"message": "Access denied."}
        log_access(requester_id, target_id)

    return data
