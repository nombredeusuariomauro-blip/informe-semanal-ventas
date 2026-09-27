import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF

# 1. Web page configuration
st.set_page_config(page_title="Jira Reporting Dashboard", layout="wide")

st.title("📊 Jira Weekly Report Automation")
st.markdown("Upload the file exported from Jira to automate your developer metrics and reporting workflow.")
st.markdown("---")

# 2. Sidebar: Upload Jira CSV/Excel file
st.sidebar.header("📁 Data Ingestion")
archivo_subido = st.sidebar.file_uploader("Upload your Jira spreadsheet (CSV or Excel)", type=["xlsx", "csv"])

# 3. Data logic: File processing or automated simulation
if archivo_subido is not None:
    try:
        if archivo_subido.name.endswith('.csv'):
            datos = pd.read_csv(archivo_subido)
        else:
            datos = pd.read_excel(archivo_subido)
        st.sidebar.success("Jira metrics loaded successfully!")
    except Exception as e:
        st.sidebar.error("Error reading file. Please ensure it is a valid format.")
else:
    st.sidebar.info("🤖 Displaying Jira mock data. Upload a file to view your real commercial metrics.")
    # Mocking exact metrics required by the Freelancer client
    np.random.seed(42)
    desarrolladores = ['Mauro', 'Ana', 'Juan', 'Lucas']
    datos = pd.DataFrame({
        'Developer': np.random.choice(desarrolladores, size=20),
        'Status': np.random.choice(['Completed', 'In Progress', 'To Do'], size=20, p=[0.5, 0.3, 0.2]),
        'Time Spent (Hours)': np.random.randint(2, 12, size=20),
        'Sprint': np.random.choice(['Sprint 1', 'Sprint 2'], size=20)
    })

# --- JIRA DATA PROCESSING & METRICS ---
tareas_completadas = int((datos['Status'] == 'Completed').sum())
horas_totales = int(datos['Time Spent (Hours)'].sum())
total_tareas = len(datos)
progreso_sprint = int((tareas_completadas / total_tareas) * 100) if total_tareas > 0 else 0

# Display Key Performance Indicators (KPIs)
col1, col2, col3 = st.columns(3)
col1.metric("✅ Completed Tasks", f"{tareas_completadas} / {total_tareas}")
col2.metric("⏱️ Total Time Spent", f"{horas_totales} hrs")
col3.metric("📈 Sprint Progress", f"{progreso_sprint}%")

st.markdown("---")

# --- VISUAL CHARTS REQUIRED BY CLIENT ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("⏱️ Hours Logged per Developer")
    horas_por_dev = datos.groupby('Developer')['Time Spent (Hours)'].sum()
    st.bar_chart(horas_por_dev)

with col_graf2:
    st.subheader("📋 Task Status Overview")
    estado_tareas = datos['Status'].value_counts()
    st.bar_chart(estado_tareas)

st.markdown("---")
st.subheader("📄 Jira Database Preview")
st.dataframe(datos)

# --- REPORT AUTOMATION (PDF) ---
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Export Report")

if st.sidebar.button("Generate PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    
    # Main Header
    pdf.cell(200, 15, "JIRA WEEKLY ACTIVITY REPORT", ln=True, align="C")
    pdf.ln(10)
    
    # Description Subheader
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, "Automated performance report for developers and key metrics tracking.", ln=True)
    pdf.ln(5)
    
    # Executive Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Executive Weekly Summary:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 8, f"- Tasks with Status 'Completed': {tareas_completadas} out of {total_tareas}", ln=True)
    pdf.cell(200, 8, f"- Total Time Spent on Tasks: {horas_totales} Hours", ln=True)
    pdf.cell(200, 8, f"- Overall Sprint Progress: {progreso_sprint}%", ln=True)
    
    pdf.ln(15)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(200, 10, "Report generated automatically using Python and Streamlit integration.", ln=True, align="C")
    
    # File Encoding and Output Stream
    pdf_output = pdf.output()
    st.sidebar.download_button(
        label="Confirm PDF Download",
        data=pdf_output,
        file_name="Jira_Weekly_Report.pdf",
        mime="application/pdf"
    )
