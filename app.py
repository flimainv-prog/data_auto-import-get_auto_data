import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Dashboard WDO, DXY e 6L",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from data_auto import get_auto_data

@st.cache_data(ttl=30)
def load_data():
    return get_auto_data()

st.title("📊 Dashboard Monitoramento: WDO, DXY e 6L")

# Botão de atualização manual
col_btn1, col_btn2 = st.columns([4, 1])
with col_btn2:
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Carrega dados
with st.spinner('Carregando dados financeiros...'):
    dashboard_data = load_data()

# Cards resumidos
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🪙 WDO")
    wdo = dashboard_data['WDO']
    if wdo['status'] == 'OK':
        st.metric(
            label=f"{wdo['symbol_used']}",
            value=f"{wdo['price']:.4f}",
            delta=f"{wdo['change_pct']:+.2f}%"
        )
        st.caption(f"Var. Abs: {wdo['change_abs']:+.4f} | Abertura: {wdo['open']:.4f}")
    else:
        st.warning(wdo['status'])

with col2:
    st.subheader("💵 DXY")
    dxy = dashboard_data['DXY']
    if dxy['status'] == 'OK':
        st.metric(
            label=f"{dxy['symbol_used']}",
            value=f"{dxy['price']:.2f}",
            delta=f"{dxy['change_pct']:+.2f}%"
        )
        st.caption(f"Var. Abs: {dxy['change_abs']:+.2f} | Abertura: {dxy['open']:.2f}")
    else:
        st.warning(dxy['status'])

with col3:
    st.subheader("🇬🇧 6L")
    sixl = dashboard_data['6L']
    if sixl['status'] == 'OK':
        st.metric(
            label=f"{sixl['symbol_used']}",
            value=f"{sixl['price']:.4f}",
            delta=f"{sixl['change_pct']:+.2f}%"
        )
        st.caption(f"Var. Abs: {sixl['change_abs']:+.4f} | Abertura: {sixl['open']:.4f}")
    else:
        st.warning(sixl['status'])

# Tabela consolidada
st.subheader("📋 Tabela Consolidada")
df_table = pd.DataFrame([dashboard_data['WDO'], dashboard_data['DXY'], dashboard_data['6L']])
df_display = df_table[['symbol_used', 'status', 'price', 'change_pct', 'source']].round(4)
st.dataframe(df_display, use_container_width=True, hide_index=True)

st.caption("* Dados atualizados a cada 30s automaticamente ou via botão manual. Fonte: Yahoo Finance.")
