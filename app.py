import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="PadelYa - Gestión", page_icon="🎾", layout="wide")

# Estilo Visual Mejorado
st.markdown("""
    <style>
    .stApp { background-color: #0b1e1e; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #0b1e1e; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #1a2e2e;
        border-radius: 10px 10px 0px 0px;
        color: white;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #2ecc71 !important; 
        color: black !important;
    }
    .stButton>button {
        background-color: #f1c40f !important;
        color: black !important;
        font-weight: bold;
        border-radius: 15px;
    }
    .fc-event-main { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 1. Base de datos de horarios (Actualizada a 2026)
if 'horarios' not in st.session_state:
    st.session_state.horarios = [
        {"id": 1, "title": "LIBRE", "start": "2026-01-04T18:00:00", "end": "2026-01-04T20:00:00", "backgroundColor": "#2ecc71", "status": "libre"},
        {"id": 2, "title": "LIBRE", "start": "2026-01-04T20:00:00", "end": "2026-01-04T22:00:00", "backgroundColor": "#2ecc71", "status": "libre"},
    ]

st.title("🎾 PadelYa Posadas")

tab_jugador, tab_dueno = st.tabs(["🎾 BUSCAR CANCHA", "🔐 PANEL DUEÑO"])

# --- VISTA JUGADOR ---
with tab_jugador:
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.subheader("📝 Tu Reserva")
        complejo = st.selectbox("Complejo:", ["World Padel Center", "La Terraza", "Padel Pro"])
        nombre = st.text_input("Nombre del Capitán:")
        
        # Filtrar solo los horarios que siguen LIBRES
        libres = [h for h in st.session_state.horarios if h["status"] == "libre"]
        opciones_dict = {f"{h['start'][11:16]} a {h['end'][11:16]}": h["id"] for h in libres}
        
        if libres:
            horario_texto = st.selectbox("Elegí un horario:", opciones_dict.keys())
            id_elegido = opciones_dict[horario_texto]
            
            if st.button("RESERVAR AHORA"):
                if nombre:
                    # Actualizar estado en el session_state
                    for h in st.session_state.horarios:
                        if h["id"] == id_elegido:
                            h["status"] = "reservado"
                            h["title"] = f"OCUPADO - {nombre}"
                            h["backgroundColor"] = "#e74c3c" # Rojo
                    
                    st.success(f"¡Reserva procesada! Procedé al pago.")
                    st.link_button("💳 PAGAR SEÑA ($3.600)", "https://www.mercadopago.com.ar")
                    st.rerun()
                else:
                    st.error("Ingresá tu nombre para reservar.")
        else:
            st.warning("No hay turnos disponibles por el momento.")

    with col_b:
        st.subheader("Disponibilidad hoy")
        cal_options = {
            "initialView": "timeGridDay",
            "initialDate": "2026-01-04", # Forzamos la vista al día de hoy
            "locale": "es",
            "slotMinTime": "08:00:00",
            "slotMaxTime": "24:00:00",
            "allDaySlot": False,
        }
        calendar(events=st.session_state.horarios, options=cal_options, key="cal_jugador")
