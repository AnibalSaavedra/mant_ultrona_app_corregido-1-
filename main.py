
import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO

st.set_page_config(page_title="Mantenimiento ULTRONA", page_icon="🛠️", layout="centered")
st.title("🛠️ Registro de Mantenimiento Mensual - ULTRONA")

EXCEL_FILE = "registro_mant_ultrona.xlsx"
BACKUP_FOLDER = "backups_ultrona"
os.makedirs(BACKUP_FOLDER, exist_ok=True)

# Cargar o crear DataFrame
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=["Fecha y Hora", "Mantenimiento Realizado", "Operador"])

# Función para exportar Excel en memoria
def to_excel_memory(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False)
    return output.getvalue()

# Función de respaldo automático
def hacer_respaldo():
    fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    respaldo_path = os.path.join(BACKUP_FOLDER, f"respaldo_ultrona_{fecha_actual}.xlsx")
    df.to_excel(respaldo_path, index=False)

# Formulario
with st.form("form_mant_ultrona"):
    fecha_hora = st.text_input("📅 Fecha y Hora", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    mantenimiento = st.selectbox("🔧 Mantenimiento Realizado", [
        "Remover y limpiar el deposito de basura",
        "Limpiar la plataforma de la tira y del deposito de residuos",
        "Limpieza del transportador de tira",
        "Limpieza y desinfección externa",
        "Calibración",
        "Cambio de papel",
        "Cambio de fusibles"
    ])
    operador = st.selectbox("👨‍🔬 Operador", [
        "Anibal Saavedra", "Juan Ramos", "Nycole Farias", "Stefanie Maureira",
        "Maria J.Vera", "Felipe Fernandez", "Paula Gutierrez", "Paola Araya",
        "Maria Rodriguez", "Pamela Montenegro"
    ])

    submit = st.form_submit_button("✅ Guardar Mantenimiento")

    if submit:
        nueva_fila = {
            "Fecha y Hora": fecha_hora,
            "Mantenimiento Realizado": mantenimiento,
            "Operador": operador
        }
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        hacer_respaldo()
        st.success("✅ Mantenimiento registrado correctamente.")

# Visualización por mes
df["Fecha y Hora"] = pd.to_datetime(df["Fecha y Hora"], errors="coerce")
df["Mes-Año"] = df["Fecha y Hora"].dt.strftime("%Y-%m")
meses_disponibles = df["Mes-Año"].dropna().unique()

st.markdown("### 🔍 Buscar registros por mes")
mes_seleccionado = st.selectbox("📆 Mes", options=sorted(meses_disponibles, reverse=True))

if mes_seleccionado:
    df_filtrado = df[df["Mes-Año"] == mes_seleccionado]
    st.dataframe(df_filtrado, use_container_width=True)

    st.download_button(
        label="📥 Descargar Registros del Mes",
        data=to_excel_memory(df_filtrado),
        file_name=f"mantenciones_ultrona_{mes_seleccionado}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Descargar todos
excel_bytes = to_excel_memory(df)
st.download_button(
    label="📥 Descargar Todos los Registros",
    data=excel_bytes,
    file_name="registro_mant_ultrona.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Footer
st.markdown("---")
st.markdown("🛠️ **Equipo**: ULTRONA | 🏢 **Empresa**: Inmunodiagnóstico")
st.markdown("📧 **Contacto**: anibalsaavedra@crb.clinicasdelcobre.cl")
