from cryptography.fernet import Fernet
import datetime

# Demo: fixed key (in production, securely store)
key = Fernet.generate_key()
cipher = Fernet(key)

# Simulated in-memory database
data_store = {}
access_logs = {}

def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data: str) -> str:
    return cipher.decrypt(data.encode()).decode()

def save_record(patient_id, record):
    encrypted_summary = encrypt_data(record["Summary"])
    record["Summary"] = encrypted_summary
    record["Date"] = str(datetime.date.today())

    if patient_id not in data_store:
        data_store[patient_id] = {"Records": [], "Appointments": [], "Access Granted": []}
    data_store[patient_id]["Records"].append(record)

def get_records(patient_id):
    patient_data = data_store.get(patient_id, {})
    if not patient_data:
        return {}

    # Decrypt record summaries
    for record in patient_data.get("Records", []):
        try:
            record["Summary"] = decrypt_data(record["Summary"])
        except Exception:
            pass

    return patient_data

def add_appointment(patient_id, appointment):
    if patient_id in data_store:
        data_store[patient_id]["Appointments"].append(appointment)

def grant_access(patient_id, doctor_name):
    if patient_id in data_store:
        if doctor_name not in data_store[patient_id]["Access Granted"]:
            data_store[patient_id]["Access Granted"].append(doctor_name)

def is_access_granted(patient_id, doctor_name):
    return doctor_name in data_store.get(patient_id, {}).get("Access Granted", [])

def log_access(doctor_name, patient_id):
    log_entry = f"{doctor_name} viewed record on {str(datetime.date.today())}"
    access_logs.setdefault(patient_id, []).append(log_entry)

def get_access_logs(patient_id):
    return access_logs.get(patient_id, [])

def get_health_trends(patient_id):
    records = get_records(patient_id).get("Records", [])
    trends = {"Lab Reports": 0, "Prescriptions": 0, "Other": 0}
    for r in records:
        r_type = r.get("Type", "Other")
        trends[r_type] = trends.get(r_type, 0) + 1
    return trends
