import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF

# 1. Configuración de la página web
st.set_page_config(page_title="Panel de Control Comercial", layout="wide")

st.title("📊 Panel de Control Inteligente")
st.markdown("Carga el archivo Excel de tu negocio para automatizar tus reportes y gráficos interactivos.")

st.markdown("---")

# 2. BOTÓN COMERCIAL: Subir archivo Excel o CSV
st.sidebar.header("📂 Carga de Datos")
archivo_subido = st.sidebar.file_uploader("Sube tu planilla de ventas (Excel o CSV)", type=["xlsx", "csv"])

# 3. Lógica de datos: Si sube archivo usa ese, si no, genera datos de demostración
if archivo_subido is not None:
    try:
        if archivo_subido.name.endswith('.csv'):
            datos = pd.read_csv(archivo_subido)
        else:
            datos = pd.read_excel(archivo_subido)
        st.sidebar.success("¡Archivo cargado con éxito!")
    except Exception as e:
        st.sidebar.error("Error al leer el archivo. Asegúrate de que sea un Excel válido.")
else:
    st.sidebar.info("💡 Mostrando datos de demostración. Sube un archivo para ver tus métricas reales.")
    np.random.seed(42)
    datos = pd.DataFrame({
        'Mes': np.random.randint(1, 5, 100),
        'Ventas ($)': np.random.randint(1000, 5000, 100),
        'Visitas Web': np.random.randint(200, 1500, 100),
        'Categoría': np.random.choice(["Tecnología", "Indumentaria", "Hogar"], 100)
    })

# Asegurar que existan las columnas mínimas para trabajar
if 'Ventas ($)' in datos.columns and 'Visitas Web' in datos.columns:
    
    # Calcular métricas para usarlas en las tarjetas y en el PDF
    total_ingresos = datos['Ventas ($)'].sum()
    promedio_venta = int(datos['Ventas ($)'].mean())
    total_visitas = datos['Visitas Web'].sum()

    # 4. Tarjetas con métricas destacadas (KPIs)
    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos Totales", f"${total_ingresos:,}")
    col2.metric("Promedio por Venta", f"${promedio_venta:,}")
    col3.metric("Total Visitas Web", f"{total_visitas:,}")

    # --- BOTÓN PARA GENERAR EL REPORTE PDF COMPLETO (LO QUE PIDE EL CLIENTE) ---
    st.sidebar.markdown("---")
    st.sidebar.header("🖨️ Exportar Reporte")
    
    # Función para armar el PDF internamente
    def generar_pdf(ingresos, promedio, visitas):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 20)
        pdf.cell(190, 15, "INFORME SEMANAL DE RENDIMIENTO", ln=True, align="C")
        pdf.ln(10)
        
        pdf.set_font("Arial", "", 12)
        pdf.cell(190, 10, "Este reporte automatizado detalla las metricas clave del negocio.", ln=True)
        pdf.ln(5)
        
        # Tabla de métricas en el PDF
        pdf.set_font("Arial", "B", 14)
        pdf.cell(190, 10, "Resumen Ejecutivo:", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(90, 10, f"- Ingresos Totales: ${ingresos:,}", ln=True)
        pdf.cell(90, 10, f"- Promedio por Venta: ${promedio:,}", ln=True)
        pdf.cell(90, 10, f"- Total Visitas Web: {visitas:,}", ln=True)
        pdf.ln(10)
        
        pdf.set_font("Arial", "I", 10)
        pdf.cell(190, 10, "Reporte generado automaticamente con Python y Streamlit.", align="C")
        return pdf.output()

    # Crear el botón físico de descarga en la web
    pdf_bytes = generar_pdf(total_ingresos, promedio_venta, total_visitas)
    st.sidebar.download_button(
        label="📥 Descargar Reporte PDF",
        data=bytes(pdf_bytes),
        file_name="informe_semanal_ventas.pdf",
        mime="application/pdf"
    )

    st.markdown("---")

    # 5. Gráficos interactivos en pantalla
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("📈 Tendencia de Ventas por Mes")
        if 'Mes' in datos.columns:
            st.line_chart(datos.groupby('Mes')['Ventas ($)'].sum())
        else:
            st.line_chart(datos['Ventas ($)'])

    with col_der:
        st.subheader("🎯 Rendimiento por Categoría")
        if 'Categoría' in datos.columns:
            st.bar_chart(datos.groupby('Categoría')['Visitas Web'].sum())
        else:
            st.bar_chart(datos['Visitas Web'].head(10))

# 6. Tabla de datos al final
st.subheader("📋 Vista de la Base de Datos")
st.dataframe(datos, use_container_width=True)
