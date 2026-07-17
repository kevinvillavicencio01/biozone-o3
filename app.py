import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Biozone O3 - Logística", page_icon="💧", layout="centered")

# Datos estáticos
clientes = ["Condominio Olimpos", "Evelyn Tinaco", "Alison Fuentes", "Metro Ecuador", 
            "Espinoza Stalin", "Andino Travel", "Diego Freire", "Cristian Mera", 
            "Fevernt", "Verónica Albiar", "Toyo Servicios", "Carla Cuenca", 
            "Rosa Vargas", "Lauris Peluquería", "Shirley Lema", "Noxfitt", 
            "Atelier Peluquería", "Mishel Vela", "Xairo Cárdenas", "Catuisca Iturralde"]

costos_p1 = [0.4972, 0.4294, 0.5537, 0.2712, 0.2825, 0.0113, 0.2373, 0.1356, 0.1356, 0.09605, 0.0565, 0.03277, 0.03277, 0.113, 0.113, 0.1356, 0.1469, 0.1356, 0.1582, 0.113]
costos_p2 = [0.4407, 0.3729, 0.7684, 0.339, 0.2825, 0.09605, 0.2373, 0.02034, 0.1469, 0.2034, 0.1808, 0.113, 0.113, 0.0791, 0.0904, 0.08475, 0.2486, 0.2373, 0.2599, 0.1808]

# Encabezado
st.title("💧 Sistema Logístico BIOZONE O3")
st.markdown("Calculadora de rutas óptimas para minimizar costos de distribución.")

st.header("📝 Ingreso de Pedidos del Día")

# Diseño en dos columnas
col1, col2 = st.columns(2)
demandas = {}
with st.form("formulario_pedidos"):
    for i, cliente in enumerate(clientes):
        if i % 2 == 0:
            with col1:
                demandas[cliente] = st.number_input(f"{cliente}", min_value=0, value=0, step=1)
        else:
            with col2:
                demandas[cliente] = st.number_input(f"{cliente}", min_value=0, value=0, step=1)

    submitted = st.form_submit_button("🚀 Calcular Ruta Óptima")

# Lógica de optimización
if submitted:
    total_demandado = sum(demandas.values())

    if total_demandado == 0:
        st.warning("⚠️ No hay botellones para distribuir. Ingresa al menos un pedido.")
    elif total_demandado > 50:
        st.error(f"🚨 ¡ALERTA LOGÍSTICA! La demanda ({total_demandado} bot.) supera la oferta máxima de las plantas (50 bot.).")
    else:
        ahorros = []
        for i, cliente in enumerate(clientes):
            ahorro = costos_p2[i] - costos_p1[i]
            ahorros.append((ahorro, i, cliente))

        ahorros.sort(reverse=True, key=lambda x: x[0])

        oferta_p1 = 20
        oferta_p2 = 30
        envios_p1 = [0] * 20
        envios_p2 = [0] * 20
        costo_total = 0.0

        for ahorro, i, cliente in ahorros:
            demanda = demandas[cliente]
            if demanda > 0 and oferta_p1 > 0:
                asignar = min(demanda, oferta_p1)
                envios_p1[i] = asignar
                oferta_p1 -= asignar
                demanda -= asignar
                costo_total += asignar * costos_p1[i]

            if demanda > 0 and oferta_p2 > 0:
                asignar = min(demanda, oferta_p2)
                envios_p2[i] = asignar
                oferta_p2 -= asignar
                demanda -= asignar
                costo_total += asignar * costos_p2[i]

        st.success(f"🏆 COSTO MÍNIMO TOTAL OBTENIDO: **{costo_total:.2f} USD**")

        st.subheader("📍 Despachos desde García de León (Límite: 20)")
        resultados_p1 = [{"Cliente": clientes[i], "Botellones": env} for i, env in enumerate(envios_p1) if env > 0]
        if resultados_p1:
            st.table(pd.DataFrame(resultados_p1))
        else:
            st.info("No hay despachos desde esta planta.")
        st.write(f"**Total ocupado:** {sum(envios_p1)} / 20 botellones")

        st.subheader("📍 Despachos desde Anda Aguirre (Límite: 30)")
        resultados_p2 = [{"Cliente": clientes[i], "Botellones": env} for i, env in enumerate(envios_p2) if env > 0]
        if resultados_p2:
            st.table(pd.DataFrame(resultados_p2))
        else:
            st.info("No hay despachos desde esta planta.")
        st.write(f"**Total ocupado:** {sum(envios_p2)} / 30 botellones")
