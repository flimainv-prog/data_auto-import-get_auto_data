import streamlit as st
import pandas as pd
from data_auto import get_auto_data

st.set_page_config(
    page_title="Dashboard Auto Data",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Dashboard WDO, DXY e 6L")

# Botão de atualização manual
col_btn_left, col_btn_right = st.columns([4, 1])
with col_btn_right:
    if st.button("🔄 Atualizar Dados", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown("Última atualização: cache TTL=30s")

# Carrega dados (usa cache do data_auto.py)
data = get_auto_data()

# Exibição em colunas
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🇧🇷 WDO")
    if not data.get('WDO', pd.DataFrame()).empty:
        latest = data['WDO'].iloc[-1]
        st.metric("Close", f"{latest['Close']:.4f}")
        st.caption(f"Volume: {latest['Volume']:.0f}")
    else:
        st.error("❌ Sem dados")

with col2:
    st.subheader("💵 DXY")
    if not data.get('DXY', pd.DataFrame()).empty:
        latest = data['DXY'].iloc[-1]
        st.metric("Close", f"{latest['Close']:.2f}")
        st.caption(f"Volume: {latest['Volume']:.0f}")
    else:
        st.error("❌ Sem dados")

with col3:
    st.subheader("🔸 6L")
    if '6L' in data and not data['6L'].empty:
        latest = data['6L'].iloc[-1]
        st.metric("Close", f"{latest['Close']:.4f}")
        st.caption(f"Volume: {latest['Volume']:.0f}")
    else:
        status = data.get('6L_status', 'Indisponível')
        st.warning(f"⚠️ {status}")

# Gráficos opcionais
if st.checkbox("Mostrar gráficos recentes"):
    st.markdown("---")
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        if not data.get('WDO', pd.DataFrame()).empty:
            st.line_chart(data['WDO']['Close'])
    with col_g2:
        if not data.get('DXY', pd.DataFrame()).empty:
            st.line_chart(data['DXY']['Close'])
    with col_g3:
        if '6L' in data and not data['6L'].empty:
            st.line_chart(data['6L']['Close'])

st.markdown("---")
st.caption("Fonte: Yahoo Finance. App estável, sem crashes mesmo sem 6L.")
