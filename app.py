import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dados Automáticos - WDO, DXY, 6L",
    page_icon="📊",
    layout="wide"
)

from data_auto import get_auto_data

@st.cache_data(ttl=30)
def load_data():
    return get_auto_data()

st.title("📈 Dados em Tempo Real: WDO, DXY e 6L")

col_btn, col_space = st.columns([1, 4])
with col_btn:
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

data = load_data()

cols = st.columns(3)
for i, asset in enumerate(['WDO', 'DXY', '6L']):
    d = data[asset]
    with cols[i]:
        if d['status'] == 'available':
            price_val = d['price']
            delta_val = d['change_pct'] / 100 if not pd.isna(d['change_pct']) else None
            st.metric(
                label=asset,
                value=price_val,
                delta=delta_val
            )
            st.caption(f"📊 {d['symbol_used']} ({d['source']})")
        else:
            st.metric(label=asset, value="N/D", delta=None)
            st.error(f"❌ {asset}: {d['status']} ({d['symbol_used']})")

st.subheader("📋 Tabela Consolidada")
table_data = []
for asset in ['WDO', 'DXY', '6L']:
    d = data[asset]
    table_data.append({
        'Ativo': asset,
        'Preço': f"{d['price']:.4f}" if not pd.isna(d['price']) else 'N/D',
        'Abertura': f"{d['open']:.4f}" if not pd.isna(d['open']) else 'N/D',
        'Fech. Ant.': f"{d['previous_close']:.4f}" if not pd.isna(d['previous_close']) else 'N/D',
        'Var. Abs': f"{d['change_abs']:.4f}" if not pd.isna(d['change_abs']) else 'N/D',
        'Var. %': f"{d['change_pct']:.2f}%" if not pd.isna(d['change_pct']) else 'N/D',
        'Status': d['status'],
        'Símbolo': d['symbol_used'],
        'Fonte': d['source']
    })

df_table = pd.DataFrame(table_data)
st.dataframe(df_table, use_container_width=True, hide_index=True)
