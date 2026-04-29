import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Automático",
    page_icon="📈",
    layout="wide"
)

from data_auto import get_auto_data

@st.cache_data(ttl=30)
def load_data():
    return get_auto_data()

st.title("📊 Dashboard Automático - WDO, DXY e 6L")

if st.button("🔄 Atualizar Dados Manualmente", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

data = load_data()

col1, col2, col3 = st.columns(3)

def display_card(asset, asset_data):
    price = asset_data['price']
    change_pct = asset_data['change_pct']
    price_str = f"{price:.4f}" if not pd.isna(price) else "N/A"
    delta_str = f"{change_pct:.2f}%" if not pd.isna(change_pct) else "N/A"
    st.metric(
        label=f"{asset.upper()}",
        value=price_str,
        delta=delta_str
    )
    if asset_data['status'] != 'success':
        st.warning("❌ Dados não disponíveis no momento. Tente atualizar.")
    if 'dataframe' in asset_data:
        with st.expander(f"📉 Últimos 5 candles de {asset.upper()}"):
            st.dataframe(asset_data['dataframe'], use_container_width=True)

with col1:
    display_card("WDO", data['WDO'])
with col2:
    display_card("DXY", data['DXY'])
with col3:
    display_card("6L", data['6L'])

st.markdown("---")

st.subheader("📋 Tabela Consolidada")

cons_data = []
for asset in ['WDO', 'DXY', '6L']:
    d = data[asset].copy()
    d['Ativo'] = asset.upper()
    if 'dataframe' in d:
        del d['dataframe']
    cons_data.append(d)

df_cons = pd.DataFrame(cons_data)
cols_order = ['Ativo', 'symbol_used', 'status', 'price', 'open', 'previous_close', 'change_abs', 'change_pct', 'source']
df_cons = df_cons[[c for c in cols_order if c in df_cons.columns]]

st.dataframe(df_cons, use_container_width=True, hide_index=True)
