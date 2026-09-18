
import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la página
st.title("Registro de Membresias Interactivo")

# 2. Inicialización limpia de la base de datos en memoria
if "miembros" not in st.session_state:
    st.session_state.miembros = pd.DataFrame(columns=[
        "Nombre Completo", "Cédula", "Correo", "Edad", "Sexo", 
        "Teléfono", "Dirección", "Barrio", "Tiempo de Conversión"
    ])

# 3. Indicador numérico del total de miembros registrados
total_miembros = len(st.session_state.miembros)
st.metric(label="Cantidad Total de Miembros", value=total_miembros)

# 4. Formulario de registro para nuevos miembros
st.subheader("➕ Formulario de Registro de Miembros")

with st.form("formulario_registro", clear_on_submit=True):
    nombre = st.text_input("Nombre Completo:")
    cedula = st.text_input("Cédula:")
    correo = st.text_input("Correo electrónico:")
    edad = st.number_input("Edad:", min_value=0, max_value=120, step=1, value=18)
    sexo = st.radio("Sexo:", ["Masculino", "Femenino"], horizontal=True)
    telefono = st.text_input("Teléfono:")
    direccion = st.text_input("Dirección:")
    barrio = st.text_input("Barrio:")
    # Formato de fecha día/mes/año requerido
    conversion = st.date_input("Tiempo de Conversión:", format="DD/MM/YYYY")
    
    enviar = st.form_submit_button("Registrar mis datos")
    
    if enviar:
        if nombre and cedula:
            # Convertir la fecha a texto con formato legible para la tabla
            fecha_texto = conversion.strftime("%d/%m/%Y")
            
            nuevo_miembro = {
                "Nombre Completo": nombre, "Cédula": cedula, "Correo": correo,
                "Edad": int(edad), "Sexo": sexo, "Teléfono": telefono,
                "Dirección": direccion, "Barrio": barrio, "Tiempo de Conversión": fecha_texto
            }
            
            # Evitar duplicar miembros con la misma cédula
            if cedula in st.session_state.miembros["Cédula"].values:
                st.error("Esta cédula ya se encuentra registrada.")
            else:
                st.session_state.miembros = pd.concat([st.session_state.miembros, pd.DataFrame([nuevo_miembro])], ignore_index=True)
                st.success("¡Datos registrados exitosamente!")
                st.rerun()
        else:
            st.error("El Nombre Completo y la Cédula son obligatorios.")

# 5. Sección para Actualizar Datos de miembros existentes
st.subheader("🔄 Actualizar Datos de un Miembro")

# Validamos que la tabla no esté vacía y que tenga la columna Cédula
if not st.session_state.miembros.empty and "Cédula" in st.session_state.miembros.columns:
    cedulas_disponibles = st.session_state.miembros["Cédula"].unique()
    cedula_buscar = st.selectbox("Seleccione la Cédula del miembro a actualizar:", cedulas_disponibles)
    
    # Obtener el índice y la información actual del miembro
    idx = st.session_state.miembros[st.session_state.miembros["Cédula"] == cedula_buscar].index[0]
    datos_actuales = st.session_state.miembros.loc[idx]

   # Obtener el índice y la información actual del miembro de manera limpia
    idx = st.session_state.miembros[st.session_state.miembros["Cédula"] == cedula_buscar].index[0]
    datos_actuales = st.session_state.miembros.loc[idx]
    
    # Campos de edición precargados con la información actual de forma limpia
    act_nombre = st.text_input("Actualizar Nombre Completo:", value=str(datos_actuales["Nombre Completo"]))
    act_correo = st.text_input("Actualizar Correo:", value=str(datos_actuales["Correo"]))
    act_edad = st.number_input("Actualizar Edad:", min_value=0, max_value=120, value=int(datos_actuales["Edad"]))
    act_sexo = st.radio("Actualizar Sexo:", ["Masculino", "Femenino"], index=0 if datos_actuales["Sexo"] == "Masculino" else 1, horizontal=True)
    act_telefono = st.text_input("Actualizar Teléfono:", value=str(datos_actuales["Teléfono"]))
    act_direccion = st.text_input("Actualizar Dirección:", value=str(datos_actuales["Dirección"]))
    act_barrio = st.text_input("Actualizar Barrio:", value=str(datos_actuales["Barrio"]))
    
    # Convertir el texto guardado de vuelta a fecha para el componente visual
    fecha_actual_dt = datetime.strptime(str(datos_actuales["Tiempo de Conversión"]), "%d/%m/%Y")
    act_conversion = st.date_input("Actualizar Tiempo de Conversión:", value=fecha_actual_dt, format="DD/MM/YYYY") 
   
    # Convertir el texto guardado de vuelta a fecha para el componente visual
    fecha_actual_dt = datetime.strptime(datos_actuales["Tiempo de Conversión"], "%d/%m/%Y")
    act_conversion = st.date_input("Actualizar Tiempo de Conversión:", value=fecha_actual_dt, format="DD/MM/YYYY")
    
    if st.button("Guardar Cambios"):
        st.session_state.miembros.at[idx, "Nombre Completo"] = act_nombre
        st.session_state.miembros.at[idx, "Correo"] = act_correo
        st.session_state.miembros.at[idx, "Edad"] = int(act_edad)
        st.session_state.miembros.at[idx, "Sexo"] = act_sexo
        st.session_state.miembros.at[idx, "Teléfono"] = act_telefono
        st.session_state.miembros.at[idx, "Dirección"] = act_direccion
        st.session_state.miembros.at[idx, "Barrio"] = act_barrio
        st.session_state.miembros.at[idx, "Tiempo de Conversión"] = act_conversion.strftime("%d/%m/%Y")
        st.success("¡Datos actualizados correctamente!")
        st.rerun()
else:
    st.info("No hay miembros registrados para actualizar.")

# 6. Tabla con la Lista General de Miembros
st.subheader("📋 Lista General de Miembros")
st.dataframe(st.session_state.miembros, use_container_width=True)


