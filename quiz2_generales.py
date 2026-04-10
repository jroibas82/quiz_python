import streamlit as st
import pandas as pd
import random

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Quiz de Cultura General", page_icon="🧠")

st.title("🧠 Cuestionario de Cultura General")
st.write("Demuestra tu polivalencia respondiendo a estas preguntas.")

# 1. CARGAR DATOS
# Usamos un decorador para que no lea el excel cada vez que pulsas un botón
@st.cache_data
def cargar_datos():
    archivo = "Generación de Cuestionario de Cultura General.xlsx"
    return pd.read_excel(archivo)

try:
    df = cargar_datos()
except FileNotFoundError:
    st.error(f"No se encuentra el archivo: Generación de Cuestionario de Cultura General.xlsx")
    st.stop()

# 2. INICIALIZAR ESTADO (El "baúl" de .NET)
if 'indice_pregunta' not in st.session_state:
    st.session_state.indice_pregunta = 0
    st.session_state.puntos = 0
    st.session_state.finalizado = False

# 3. LÓGICA DE JUEGO
if not st.session_state.finalizado:
    fila = df.iloc[st.session_state.indice_pregunta]
    
    pregunta = fila.iloc[0]
    correcta = fila.iloc[1]
    opciones = [fila.iloc[1], fila.iloc[2], fila.iloc[3], fila.iloc[4]]
    
    # Mezclamos las opciones solo una vez por pregunta
    if 'opciones_mezcladas' not in st.session_state:
        random.shuffle(opciones)
        st.session_state.opciones_mezcladas = opciones

    st.subheader(f"Pregunta {st.session_state.indice_pregunta + 1}:")
    st.info(pregunta)

    # Creamos los botones de respuesta
    for opcion in st.session_state.opciones_mezcladas:
        if st.button(str(opcion), use_container_width=True):
            if opcion == correcta:
                st.success("¡Correcto!")
                st.session_state.puntos += 1
            else:
                st.error(f"Incorrecto. La respuesta era: {correcta}")
            
            # Preparar la siguiente pregunta
            st.session_state.indice_pregunta += 1
            del st.session_state.opciones_mezcladas # Forzamos nueva mezcla
            
            if st.session_state.indice_pregunta >= len(df):
                st.session_state.finalizado = True
            
            st.rerun()

# 4. PANTALLA FINAL
else:
    st.balloons()
    st.header("¡Has terminado!")
    st.metric("Puntuación Final", f"{st.session_state.puntos} / {len(df)}")
    
    if st.button("Reiniciar Quiz"):
        st.session_state.indice_pregunta = 0
        st.session_state.puntos = 0
        st.session_state.finalizado = False
        st.rerun()