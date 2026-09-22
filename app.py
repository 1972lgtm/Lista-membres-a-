import streamlit as st
import pandas as pd
import os

# Nombre del archivo donde se guardaran TODOS los registros centralizados
ARCHIVO_DATOS = "base_miembros.csv"

# Contrasena secreta para administradores
CONTRASENA_ADMIN = "admin123"

# Funciones para leer y escribir el archivo central
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        try:
            return pd.read_csv(ARCHIVO_DATOS, dtype={"Cédula": str, "Teléfono": str})
        except:
            pass
    return pd.DataFrame(columns=[
        "Nombre Completo", "Cédula", "Correo", "Edad", "Sexo", 
        "Teléfono", "Dirección", "Barrio", "Tiempo de Conversión"
    ])

def guardar_datos(df):
    df.to_csv(ARCHIVO_DATOS, index=False)

if "df_miembros" not in st.session_state:
    st.session_state["df_miembros"] = cargar_datos()

df_miembros = st.session_state["df_miembros"]



# Configuracion de la pagina
st.set_page_config(page_title="Membresias", layout="wide")
st.title("Registro de Membresias Interactivo")

# --- BARRA LATERAL (Panel de Administracion Seguro) ---
st.sidebar.title("🔐 Acceso Administrador")
password_ingresado = st.sidebar.text_input("Ingrese la contrasenia:", type="password")

# Verificar si es administrador
es_admin = (password_ingresado == CONTRASENA_ADMIN)

if es_admin:
    st.sidebar.success("Sesion autorizada")
    
    # Muestra de la cifra numerica compartida en tiempo real
    total_miembros = len(df_miembros)
    st.metric(label="Cantidad Total de Miembros Registrados", value=total_miembros)
    
    # Organizacion en pestanias solo para admins
    tab1, tab2, tab3 = st.tabs(["➕ Registrar Miembro", "🔄 Actualizar Datos", "📋 Ver Lista Completa"])
else:
    st.sidebar.info("Area de registro para miembros activos.")
    tab1 = st.container()

# --- FORMULARIO DE REGISTRO (Visible para todos) ---
with tab1:
    st.subheader("Formulario de Registro")
    with st.form("form_alta", clear_on_submit=True):
        f_nombre = st.text_input("Nombre Completo:")
        f_cedula = st.text_input("Cédula:")
        f_correo = st.text_input("Correo electrónico:")
        f_edad = st.number_input("Edad:", min_value=0, max_value=120, step=1, value=18)
        f_sexo = st.radio("Sexo:", ["Masculino", "Femenino"], horizontal=True)
        f_telefono = st.text_input("Teléfono:")
        f_direccion = st.text_input("Dirección:")
        f_barrio = st.text_input("Barrio:")
        f_conversion = st.text_input("Tiempo de Conversión:")
        
        btn_registrar = st.form_submit_button("Registrar mis datos")
        
        if btn_registrar:
            if f_nombre and f_cedula:
                df_miembros = cargar_datos()
                if f_cedula in df_miembros["Cédula"].values:
                    st.error("Esta cédula ya se encuentra registrada.")
                else:
                    nuevo = {
                        "Nombre Completo": f_nombre, "Cédula": f_cedula, "Correo": f_correo,
                        "Edad": int(f_edad), "Sexo": f_sexo, "Teléfono": f_telefono,
                        "Dirección": f_direccion, "Barrio": f_barrio, "Tiempo de Conversión": f_conversion
                    }
                    df_miembros = pd.concat([df_miembros, pd.DataFrame([nuevo])], ignore_index=True)
                    guardar_datos(df_miembros)
                    st.success("¡Datos registrados exitosamente!")
                    st.rerun()
            else:
                st.error("El Nombre Completo y la Cédula son obligatorios.")

# --- SECCIONES EXCLUSIVAS PARA ADMINISTRADORES ---
if es_admin:
    # --- PESTANIA 2: ACTUALIZAR DATOS ---
    with tab2:
        st.subheader("Actualizar Datos de un Miembro")
        if not df_miembros.empty:
            cedulas_disponibles = df_miembros["Cédula"].unique()
            cedula_sel = st.selectbox("Seleccione la Cédula del miembro a modificar:", cedulas_disponibles, key="sel_cedula")
            
            fila_filtrada = df_miembros[df_miembros["Cédula"] == cedula_sel]
            
            if not fila_filtrada.empty:
                # Extraemos los datos de la fila de forma segura usando .iloc[0]
                datos_act = fila_filtrada.iloc[0]
                
                u_nombre = st.text_input("Actualizar Nombre Completo:", value=str(datos_act["Nombre Completo"]))
                u_correo = st.text_input("Actualizar Correo:", value=str(datos_act["Correo"]))
                u_edad = st.number_input("Actualizar Edad:", min_value=0, max_value=120, value=int(datos_act["Edad"]))
                u_sexo = st.radio("Actualizar Sexo:", ["Masculino", "Femenino"], index=0 if datos_act["Sexo"] == "Masculino" else 1, horizontal=True)
                u_telefono = st.text_input("Actualizar Teléfono:", value=str(datos_act["Teléfono"]))
                u_direccion = st.text_input("Actualizar Dirección:", value=str(datos_act["Dirección"]))
                u_barrio = st.text_input("Actualizar Barrio:", value=str(datos_act["Barrio"]))
                u_conversion = st.text_input("Actualizar Tiempo de Conversión:", value=str(datos_act["Tiempo de Conversión"]))
                
                if st.button("Guardar Cambios"):
                    df_miembros = cargar_datos()
                    df_miembros.loc[df_miembros["Cédula"] == cedula_sel, "Nombre Completo"] = u_nombre
                    df_miembros.loc[df_miembros["Cédula"] == cedula_sel, "Correo"] = u_correo
                    df_miembros.loc[df_miembros["Cédula"] == cedula_sel, "Edad"] = int(u_edad)
                    df_miembros.loc[df_miembros["Cédula"] == cedula_sel, "Sexo"] = u_sexo
                    df_miembros.loc[df_miembros["Cédula"] == cedula_sel, "Teléfono"] = u_telefono
                    df_miembros.loc[df_miembros["Cédula"] == cedula_sel, "Dirección"] = u_direccion
                    df_miembros.loc[df_miembros["Cédula"] == cedula_sel, "Barrio"] = u_barrio
                    df_miembros.loc[df_miembros["Cédula"] == cedula_sel, "Tiempo de Conversión"] = u_conversion
                    
                    guardar_datos(df_miembros)
                    st.success("¡Datos actualizados correctamente!")
                    st.rerun()
        else:
            st.info("No hay miembros registrados para modificar.")

    # --- PESTANIA 3: VER LISTA COMPLETA ---
    with tab3:
        st.subheader("Lista General de Miembros")
        st.dataframe(df_miembros, use_container_width=True)
