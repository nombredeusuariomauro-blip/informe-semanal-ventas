import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF

# 1. Configuración de la página web
st.set_page_config(page_title="Panel de Reportes Jira", layout="wide")

st.title("📊 Automatización de Informes Semanales de Jira")
st.markdown("Carga el archivo exportado de Jira para automatizar tus reportes y métricas de desarrolladores.")
st.markdown("---")

# 2. BOTÓN COMERCIAL: Subir archivo CSV de Jira
st.sidebar.header("📁 Carga de Datos")
archivo_subido = st.sidebar.file_uploader("Sube tu planilla de Jira (CSV o Excel)", type=["xlsx", "csv"])

# 3. Lógica de datos: Si sube archivo usa ese, si no, genera simulación de Jira
if archivo_subido is not None:
    try:
        if archivo_subido.name.endswith('.csv'):
            datos = pd.read_csv(archivo_subido)
        else:
            datos = pd.read_excel(archivo_subido)
        st.sidebar.success("¡Datos de Jira cargados con éxito!")
    except Exception as e:
        st.sidebar.error("Error al leer el archivo. Asegúrate de que sea un formato válido.")
else:
    st.sidebar.info("🤖 Mostrando datos de demostración de Jira. Sube un archivo para ver tus métricas reales.")
    # Simulamos las métricas exactas que pide el cliente en Freelancer
    np.random.seed(42)
    desarrolladores = ['Mauro', 'Ana', 'Juan', 'Lucas']
    datos = pd.DataFrame({
        'Desarrollador': np.random.choice(desarrolladores, size=20),
        'Estado': np.random.choice(['Completada', 'En Progreso', 'Por Hacer'], size=20, p=[0.5, 0.3, 0.2]),
        'Tiempo Dedicado (Horas)': np.random.randint(2, 12, size=20),
        'Sprint': np.random.choice(['Sprint 1', 'Sprint 2'], size=20)
    })

# --- PROCESAMIENTO DE MÉTRICAS PARA JIRA ---
tareas_completadas = int((datos['Estado'] == 'Completada').sum())
horas_totales = int(datos['Tiempo Dedicado (Horas)'].sum())
total_tareas = len(datos)
progreso_sprint = int((tareas_completadas / total_tareas) * 100) if total_tareas > 0 else 0

# Mostrar indicadores principales
col1, col2, col3 = st.columns(3)
col1.metric("✅ Tareas Completadas", f"{tareas_completadas} / {total_tareas}")
col2.metric("⏱️ Horas Totales Invertidas", f"{horas_totales} hrs")
col3.metric("📈 Progreso del Sprint", f"{progreso_sprint}%")

st.markdown("---")

# --- GRÁFICOS VISUALES EXIGIDOS POR EL CLIENTE ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("⏱️ Horas Dedicadas por Desarrollador")
    horas_por_dev = datos.groupby('Desarrollador')['Tiempo Dedicado (Horas)'].sum()
    st.bar_chart(horas_por_dev)

with col_graf2:
    st.subheader("📋 Estado Actual de las Tareas")
    estado_tareas = datos['Estado'].value_counts()
    st.bar_chart(estado_tareas)

st.markdown("---")
st.subheader("📄 Vista de la Base de Datos de Jira")
st.dataframe(datos)

# --- AUTOMATIZACIÓN DEL REPORTE PDF ---
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Exportar Reporte")

if st.sidebar.button("Descargar Reporte PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    
    # Título principal
    pdf.cell(200, 15, "JIRA WEEKLY ACTIVITY REPORT", ln=True, align="C")
    pdf.ln(10)
    
    # Subtítulo descriptivo
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, "Reporte automatizado de rendimiento de desarrolladores y métricas clave.", ln=True)
    pdf.ln(5)
    
    # Resumen Ejecutivo
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Resumen Ejecutivo de la Semana:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 8, f"- Tareas con Estado 'Completada': {tareas_completadas} de {total_tareas}", ln=True)
    pdf.cell(200, 8, f"- Tiempo Dedicado en Tareas: {horas_totales} Horas totales", ln=True)
    pdf.cell(200, 8, f"- Progreso general del Sprint actual: {progreso_sprint}%", ln=True)
    
    pdf.ln(15)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(200, 10, "Reporte generado automaticamente mediante integracion de Python y Streamlit.", ln=True, align="C")
    
    # Guardar y permitir descarga
    pdf_output = pdf.output(dest='S').encode('latin1')
    st.sidebar.download_button(
        label="Confirmar Descarga PDF",
        data=pdf_output,
        file_name="Jira_Weekly_Report.pdf",
        mime="application/pdf"
    )
