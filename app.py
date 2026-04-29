import streamlit as st

# 1. OBRIGATÓRIO: Primeiro comando do Streamlit
st.set_page_config(
    page_title="Dashboard WDO/DXY/6L",
    layout="wide",
    page_icon="📈"
)

import pandas as pd
import numpy as np
from data_auto import get_auto_data

# 2. Cache de 30 segundos para não sobrecarregar o Yahoo
@st.cache_data(ttl=30)
def load_market_data():
    return get_auto_data()

st.title("📊 Monitor de Mercado em Tempo Real")

# Botão de atualização manual
if st.button("🔄 Forçar Atualização"):
    st.cache_data.clear()
    st.rerun()

# 3. Carregamento dos dados
with st.spinner("Buscando dados no Yahoo Finance..."):
    data = load_market_data()

# 4. Exibição em Colunas (Cards)
col1, col2, col3 = st.columns(3)

for i, asset in enumerate(['WDO', 'DXY', '6L']):
    info = data[asset]
    with [col1, col2, col3][i]:
        if info['status'] == 'success':
            st.metric(
                label=f"{asset} ({info['symbol']})",
                value=f"{info['price']:.4f}",
                delta=f"{info['change_pct']:.2f}%"
            )
        else:
            st.metric(label=asset, value="Indisponível", delta=None)
            st.error(f"Erro ao carregar {asset}")

st.divider()

# 5. Tabela Consolidada (Garante que a tela não fique vazia)
st.subheader("📋 Resumo Técnico")
df_rows = []
for asset, info in data.items():
    df_rows.append({
        "Ativo": asset,
        "Ticker": info['symbol'],
        "Preço": info['price'],
        "Variação %": info['change_pct'],
        "Status": "✅ OK" if info['status'] == 'success' else "❌ FALHA"
    })

df = pd.DataFrame(df_rows)
st.dataframe(df, use_container_width=True, hide_index=True)

st.caption("Fonte: Yahoo Finance | Atualização: Automática (30s)")
