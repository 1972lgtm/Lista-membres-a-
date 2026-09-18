import streamlit as st
import pandas as pd

# 1. Configuracion principal de la pagina
st.set_page_config(page_title="Membresias", layout="wide")
st.title("Registro de Membresias Interactivo")

# 2. Base de datos interna temporal
if "miembros" not in st.session_state:
    st.session_state.miembros = pd.DataFrame(columns=[
        "Nombre Completo", "Cédula", "Correo", "Edad", "Sexo", 
        "Teléfono", "Dirección", "Barrio", "Tiempo de Conversión"
    ])

# 3. Muestra de la cifra numerica con la cantidad total
total_miembros = len(st.session_state.miembros)
st.metric(label="Cantidad Total de Miembros Registrados", value=total_miembros)

# 4. Organizacion del sitio en Pestañas
tab1, tab2, tab3 = st.tabs(["➕ Registrar Miembro", "🔄 Actualizar Datos", "📋 Ver Lista Completa"])

# --- PESTAÑA 1: FORMULARIO DE REGISTRO ---
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
        f_conversion = st.text_input("Tiempo de Conversión:", key="alta_conversion")
        
        btn_registrar = st.form_submit_button("Registrar mis datos")
        
        if btn_registrar:
            if f_nombre and f_cedula:
                if f_cedula in st.session_state.miembros["Cédula"].values:
                    st.error("Esta cédula ya se encuentra registrada.")
                else:
                    nuevo = {
                        "Nombre Completo": f_nombre, "Cédula": f_cedula, "Correo": f_correo,
                        "Edad": int(f_edad), "Sexo": f_sexo, "Teléfono": f_telefono,
                        "Dirección": f_direccion, "Barrio": f_barrio, "Tiempo de Conversión": f_conversion
                    }
                    st.session_state.miembros = pd.concat([st.session_state.miembros, pd.DataFrame([nuevo])], ignore_index=True)
                    st.success("¡Datos registrados exitosamente!")
                    st.rerun()
            else:
                st.error("El Nombre Completo y la Cédula son obligatorios.")

# --- PESTAÑA 2: ACTUALIZAR DATOS ---
with tab2:
    st.subheader("Actualizar Datos de un Miembro")
    if not st.session_state.miembros.empty:
        cedulas_disponibles = st.session_state.miembros["Cédula"].unique()
        cedula_sel = st.selectbox("Seleccione la Cédula del miembro a modificar:", cedulas_disponibles, key="sel_cedula")
        
        # Localizar el registro actual de forma segura
        fila_filtrada = st.session_state.miembros[st.session_state.miembros["Cédula"] == cedula_sel]
        
        if not fila_filtrada.empty:
            idx_real = fila_filtrada.index[0]  # Obtener el indice numérico entero exacto
            datos_act = fila_filtrada.iloc[0]
            
            # Campos con valores precargados
            u_nombre = st.text_input("Actualizar Nombre Completo:", value=str(datos_act["Nombre Completo"]), key="u_nom")
            u_correo = st.text_input("Actualizar Correo:", value=str(datos_act["Correo"]), key="u_corr")
            u_edad = st.number_input("Actualizar Edad:", min_value=0, max_value=120, value=int(datos_act["Edad"]), key="u_ed")
            u_sexo = st.radio("Actualizar Sexo:", ["Masculino", "Femenino"], index=0 if datos_act["Sexo"] == "Masculino" else 1, horizontal=True, key="u_sex")
            u_telefono = st.text_input("Actualizar Teléfono:", value=str(datos_act["Teléfono"]), key="u_tel")
            u_direccion = st.text_input("Actualizar Dirección:", value=str(datos_act["Dirección"]), key="u_dir")
            u_barrio = st.text_input("Actualizar Barrio:", value=str(datos_act["Barrio"]), key="u_bar")
            u_conversion = st.text_input("Actualizar Tiempo de Conversión:", value=str(datos_act["Tiempo de Conversión"]), key="u_conv")
            
            if st.button("Guardar Cambios", key="btn_guardar_cambios"):
                # Asignación directa usando la posición indexada limpia
                st.session_state.miembros.loc[idx_real, "Nombre Completo"] = u_nombre
                st.session_state.miembros.loc[idx_real, "Correo"] = u_correo
                st.session_state.miembros.loc[idx_real, "Edad"] = int(u_edad)
                st.session_state.miembros.loc[idx_real, "Sexo"] = u_sexo
                st.session_state.miembros.loc[idx_real, "Teléfono"] = u_telefono
                st.session_state.miembros.loc[idx_real, "Dirección"] = u_direccion
                st.session_state.miembros.loc[idx_real, "Barrio"] = u_barrio
                st.session_state.miembros.loc[idx_real, "Tiempo de Conversión"] = u_conversion
                
                st.success("¡Datos actualizados correctamente!")
                st.rerun()
    else:
        st.info("No hay miembros registrados para modificar.")

# --- PESTAÑA 3: VER LISTA COMPLETA ---
with tab3:
    st.subheader("Lista General de Miembros")
    st.dataframe(st.session_state.miembros, use_container_width=True)
