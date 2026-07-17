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

nombre_p1 = "García de León"
nombre_p2 = "Anda Aguirre"

# ---- Encabezado ----
st.title("💧 Sistema Logístico BIOZONE O3")
st.markdown("Calculadora de rutas óptimas para minimizar costos de distribución.")

# ---- Panel lateral: configuración de capacidad por planta ----
st.sidebar.header("⚙️ Capacidad de Plantas")
st.sidebar.caption("Ajusta la capacidad de cada motorizado según la producción actual.")

st.sidebar.markdown(f"**🛵 {nombre_p1}**")
oferta_p1_max = st.sidebar.number_input(
    "Capacidad (botellones)", min_value=0, value=20, step=1, key="cap_p1"
)

st.sidebar.markdown(f"**🛵 {nombre_p2}**")
oferta_p2_max = st.sidebar.number_input(
    "Capacidad (botellones)", min_value=0, value=30, step=1, key="cap_p2"
)

capacidad_total = oferta_p1_max + oferta_p2_max
st.sidebar.divider()
st.sidebar.metric("Capacidad total del día", f"{capacidad_total} bot.")

# ---- Formulario de pedidos ----
st.header("📝 Ingreso de Pedidos del Día")

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

# ---- Lógica de optimización ----
if submitted:
    total_demandado = sum(demandas.values())

    if total_demandado == 0:
        st.warning("⚠️ No hay botellones para distribuir. Ingresa al menos un pedido.")
    elif total_demandado > capacidad_total:
        st.error(f"🚨 ¡ALERTA LOGÍSTICA! La demanda ({total_demandado} bot.) supera la capacidad total disponible ({capacidad_total} bot.).")
    else:
        ahorros = []
        for i, cliente in enumerate(clientes):
            ahorro = costos_p2[i] - costos_p1[i]
            ahorros.append((ahorro, i, cliente))

        ahorros.sort(reverse=True, key=lambda x: x[0])

        oferta_p1 = oferta_p1_max
        oferta_p2 = oferta_p2_max
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

        total_p1 = sum(envios_p1)
        total_p2 = sum(envios_p2)

        st.divider()
        st.subheader("📊 Resumen del Despacho")

        # Tarjetas tipo dashboard
        m1, m2, m3 = st.columns(3)
        m1.metric("💰 Costo Mínimo Total", f"$ {costo_total:.2f}")
        m2.metric(f"🛵 {nombre_p1}", f"{total_p1} / {oferta_p1_max} bot.")
        m3.metric(f"🛵 {nombre_p2}", f"{total_p2} / {oferta_p2_max} bot.")

        # Gráfico de barras: comparación de carga por planta
        df_carga = pd.DataFrame({
            "Planta": [nombre_p1, nombre_p2],
            "Botellones asignados": [total_p1, total_p2],
        }).set_index("Planta")
        st.bar_chart(df_carga)

        st.divider()

        # Detalle por motorizado
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(f"### 🛵 {nombre_p1}")
            st.caption(f"Capacidad: {oferta_p1_max} bot.")
            resultados_p1 = [{"Cliente": clientes[i], "Botellones": env} for i, env in enumerate(envios_p1) if env > 0]
            if resultados_p1:
                st.table(pd.DataFrame(resultados_p1))
            else:
                st.info("Sin despachos.")
            st.progress(min(total_p1 / oferta_p1_max, 1.0) if oferta_p1_max > 0 else 0)
            st.write(f"**Ocupación:** {total_p1} / {oferta_p1_max} botellones")

        with col_b:
            st.markdown(f"### 🛵 {nombre_p2}")
            st.caption(f"Capacidad: {oferta_p2_max} bot.")
            resultados_p2 = [{"Cliente": clientes[i], "Botellones": env} for i, env in enumerate(envios_p2) if env > 0]
            if resultados_p2:
                st.table(pd.DataFrame(resultados_p2))
            else:
                st.info("Sin despachos.")
            st.progress(min(total_p2 / oferta_p2_max, 1.0) if oferta_p2_max > 0 else 0)
            st.write(f"**Ocupación:** {total_p2} / {oferta_p2_max} botellones")
