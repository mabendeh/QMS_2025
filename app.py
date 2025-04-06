import streamlit as st
import pandas as pd
import uuid
import os
from datetime import datetime

# Configuration Constants
UPLOAD_DIR = "uploaded_documents"
DB_FILE = "nc_log.csv"
COLUMNS = [
    "timestamp", "mrb_date", "shift", "ccsa_item", "prod_date", "odd_even", "held_by",
    "defect", "location_found", "disposition", "filename"
]
ROLE = "admin"  # for now, assume admin to unlock all fields

# Ensure folders exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Streamlit page configuration
st.set_page_config(page_title="🛠 NC Reporting", layout="wide")

def load_nc_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=COLUMNS)

def save_nc_data(df):
    df.to_csv(DB_FILE, index=False)

def upload_file(file):
    if file:
        ext = file.name.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
            f.write(file.read())
        return filename
    return ""

def create_new_report(mrb_date, shift, ccsa_item, prod_date, odd_even, held_by, defect, location_found, disposition, filename):
    return pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mrb_date": mrb_date,
        "shift": shift,
        "ccsa_item": ccsa_item,
        "prod_date": prod_date,
        "odd_even": odd_even,
        "held_by": held_by,
        "defect": defect,
        "location_found": location_found,
        "disposition": disposition,
        "filename": filename
    }])

# Page Layout
st.markdown("## 🚨 Non-Conformance Report")
st.markdown("Fill out the form completely. Fields marked with 🔒 are for leads/admin only.")

with st.form("nc_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mrb_date = st.date_input("🗓️ MRB Date")
        shift = st.selectbox("🕒 Shift", ["A", "B", "C"])
        odd_even = st.radio("🔄 Odd / Even", ["Odd", "Even"], horizontal=True)
    
    with col2:
        ccsa_item = st.text_input("🧾 CCSA Item (Scan)")
        prod_date = st.date_input("🏭 Production Date")
        held_by = st.text_input("🧑 Placed on Hold By")
    
    with col3:
        defect = st.text_input("❌ Defect Description")
        location_found = st.selectbox("📍 Location Found", ["Incoming", "In-Process", "Final", "Customer"])
        disposition = st.selectbox("🔒 Disposition (Leads Only)", ["", "Scrap", "Rework", "Use As-Is", "Hold"]) if ROLE == "admin" else "Pending"
    
    file = st.file_uploader("📎 Upload File (image/pdf, optional)", type=["png", "jpg", "jpeg", "pdf"])
    
    submitted = st.form_submit_button("✅ Submit Report")
    
    if submitted:
        filename = upload_file(file)
        new_report = create_new_report(mrb_date, shift, ccsa_item, prod_date, odd_even, held_by, defect, location_found, disposition, filename)
        db = load_nc_data()
        db = pd.concat([db, new_report], ignore_index=True)
        save_nc_data(db)
        st.success("🎉 Report submitted successfully!")

# Display log below
st.markdown("---")
st.markdown("### 📋 Submitted Reports")
df = load_nc_data()

if df.empty:
    st.info("No reports submitted yet.")
else:
    with st.expander("🔎 View & Filter Reports"):
        col1, col2 = st.columns(2)
        
        with col1:
            filter_shift = st.multiselect("Filter by Shift", options=["A", "B", "C"])
        
        with col2:
            filter_location = st.multiselect("Filter by Location", options=["Incoming", "In-Process", "Final", "Customer"])
        
        if filter_shift:
            df = df[df["shift"].isin(filter_shift)]
        if filter_location:
            df = df[df["location_found"].isin(filter_location)]
    
    st.dataframe(df, use_container_width=True)
