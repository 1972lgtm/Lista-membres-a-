import streamlit as st
import pandas as pd

# 1. Configuracion principal de la pagina
st.set_page_config(page_title="Membresias", layout="wide")
st.title("Registro de Membresias Interactivo")

# 2. Base de datos interna temporal (se limpia al reiniciar el servidor en la nube)
if "miembros" not in st.session_state:
    st.session_state.miembros = pd.DataFrame(columns=[
        "Nombre Completo", "Cédula", "Correo", "Edad", "Sexo", 
        "Teléfono", "Dirección", "Barrio", "Tiempo de Conversión"
    ])

# 3. Muestra de la cifra numerica con la cantidad total
total_miembros = len(st.session_state.miembros)
st.metric(label="Cantidad Total de Miembros Registrados", value=total_miembros)

# 4. Organizacion del sitio en Pestanas
tab1, tab2, tab3, tab4 = st.tabs(["➕ Registrar Miembro", "🔄 Actualizar Datos", "📋 Ver Lista Completa", "📥 Cargar Excel"])

# --- PESTANA 1: FORMULARIO DE REGISTRO ---
with tab1:
    st.subheader("Formulario de Registro")
    with st.form("form_alta", clear_on_submit=True):
        f_nombre = st.text_input("Nombre Completo:", key="alta_nombre")
        f_cedula = st.text_input("Cédula:", key="alta_cedula")
        f_correo = st.text_input("Correo electrónico:", key="alta_correo")
        f_edad = st.number_input("Edad:", min_value=0, max_value=120, step=1, value=18, key="alta_edad")
        f_sexo = st.radio("Sexo:", ["Masculino", "Femenino"], horizontal=True, key="alta_sexo")
        f_telefono = st.text_input("Teléfono:", key="alta_telefono")
        f_direccion = st.text_input("Dirección:", key="alta_direccion")
        f_barrio = st.text_input("Barrio:", key="alta_barrio")
        
        # CAJA DE TEXTO LIBRE (ADIÓS AL CALENDARIO BLOQUEADO)
        f_conversion = st.text_area("Tiempo de Conversión (Ej: 12/06/1998 o 5 años):", key="alta_conversion")
        
        btn_registrar = st.form_submit_button("Registrar mis datos")
        
        if btn_registrar:
            if f_nombre.strip() and f_cedula.strip():
                cedula_str = str(f_cedula).strip()
                if cedula_str in st.session_state.miembros["Cédula"].astype(str).values:
                    st.error("Error: Esta cédula ya se encuentra registrada en el sistema.")
                else:
                    nuevo_registro = {
                        "Nombre Completo": f_nombre, "Cédula": cedula_str, "Correo": f_correo,
                        "Edad": int(f_edad), "Sexo": f_sexo, "Teléfono": f_telefono,
                        "Dirección": f_direccion, "Barrio": f_barrio, "Tiempo de Conversión": f_conversion
                    }
                    st.session_state.miembros = pd.concat([st.session_state.miembros, pd.DataFrame([nuevo_registro])], ignore_index=True)
                    st.success("¡Datos registrados exitosamente!")
                    st.rerun()
            else:
                st.error("Error: El Nombre Completo y la Cédula son campos obligatorios.")

# --- PESTANA 2: ACTUALIZACION DE REGISTROS ---
with tab2:
    st.subheader("Actualizar Registro Existente")
    if not st.session_state.miembros.empty:
        cedulas_disponibles = st.session_state.miembros["Cédula"].tolist()
        cedula_sel = st.selectbox("Seleccione la Cédula de la persona a actualizar:", cedulas_disponibles, key="select_cedula_act")
        
        idx_fila = st.session_state.miembros[st.session_state.miembros["Cédula"] == cedula_sel].index
        datos_fila = st.session_state.miembros.loc[idx_fila].iloc[0]
        
        with st.form("form_actualizar"):
            u_nombre = st.text_input("Nombre Completo:", value=str(datos_fila["Nombre Completo"]), key="act_nombre")
            u_correo = st.text_input("Correo:", value=str(datos_fila["Correo"]), key="act_correo")
            u_edad = st.number_input("Edad:", min_value=0, max_value=120, value=int(datos_fila["Edad"]), step=1, key="act_edad")
            idx_sexo = 0 if datos_fila["Sexo"] == "Masculino" else 1
            u_sexo = st.radio("Sexo:", ["Masculino", "Femenino"], index=idx_sexo, horizontal=True, key="act_sexo")
            u_telefono = st.text_input("Teléfono:", value=str(datos_fila["Teléfono"]), key="act_telefono")
            u_direccion = st.text_input("Dirección:", value=str(datos_fila["Dirección"]), key="act_direccion")
            u_barrio = st.text_input("Barrio:", value=str(datos_fila["Barrio"]), key="act_barrio")
            u_conversion = st.text_area("Tiempo de Conversión:", value=str(datos_fila["Tiempo de Conversión"]), key="act_conversion")
            
            btn_actualizar = st.form_submit_button("Guardar Cambios")
            
            if btn_actualizar:
                if u_nombre.strip():
                    st.session_state.miembros.at[idx_fila, "Nombre Completo"] = u_nombre
                    st.session_state.miembros.at[idx_fila, "Correo"] = u_correo
                    st.session_state.miembros.at[idx_fila, "Edad"] = int(u_edad)
                    st.session_state.miembros.at[idx_fila, "Sexo"] = u_sexo
                    st.session_state.miembros.at[idx_fila, "Teléfono"] = u_telefono
                    st.session_state.miembros.at[idx_fila, "Dirección"] = u_direccion
                    st.session_state.miembros.at[idx_fila, "Barrio"] = u_barrio
                    st.session_state.miembros.at[idx_fila, "Tiempo de Conversión"] = u_conversion
                    st.success("¡Datos actualizados con éxito!")
                    st.rerun()
                else:
                    st.error("El nombre no puede quedar vacío.")
    else:
        st.info("No hay miembros guardados en la lista actualmente.")

# --- PESTANA 3: VISTA DE LA TABLA ---
with tab3:
    st.subheader("Lista General de Miembros")
    st.dataframe(st.session_state.miembros, use_container_width=True)

# --- PESTANA 4: CARGAR DESDE EXCEL ---
with tab4:
    st.subheader("Importar Base de Datos desde Excel")
    st.info("Nota: Las columnas de tu Excel deben llamarse exactamente igual que los campos de registro.")
    
    archivo_subido = st.file_uploader("Elige tu archivo de Excel (.xlsx)", type=["xlsx"], key="excel_uploader")
    
    if archivo_subido is not None:
        try:
            df_excel = pd.read_excel(archivo_subido)
            if "Cédula" in df_excel.columns:
                df_excel["Cédula"] = df_excel["Cédula"].astype(str).str.strip()
            
            if st.button("Confirmar y Combinar Datos", key="btn_confirmar_excel"):
                columnas_fijas = st.session_state.miembros.columns
                df_excel_limpio = df_excel[[c for c in df_excel.columns if c in columnas_fijas]]
                
                cedulas_existentes = st.session_state.miembros["Cédula"].values
                nuevos_no_repetidos = df_excel_limpio[~df_excel_limpio["Cédula"].isin(cedulas_existentes)]
                
                st.session_state.miembros = pd.concat([st.session_state.miembros, nuevos_no_repetidos], ignore_index=True)
                st.success(f"¡Se han importado exitosamente {len(nuevos_no_repetidos)} miembros nuevos!")
                st.rerun()
        except Exception as e:
            st.error(f"Ocurrió un problema al leer el archivo: {e}")
