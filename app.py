import streamlit as st

# CONFIGURAÇÃO DEVE SER O PRIMEIRO COMANDO
st.set_page_config(
    page_title="Dashboard WDO/DXY/6L",
    layout="wide",
    page_icon="📈"
)

import pandas as pd
from data_auto import get_auto_data

# Cache de 30 segundos para evitar bloqueios do Yahoo
@st.cache_data(ttl=30)
def load_market_data():
    return get_auto_data()

st.title("📊 Monitor de Mercado - WDO, DXY e 6L")

# Botão para limpar o cache e atualizar
if st.button("🔄 Forçar Atualização"):
    st.cache_data.clear()
    st.rerun()

with st.spinner("Buscando cotações atualizadas..."):
    data = load_market_data()

# Exibição em Cards
col1, col2, col3 = st.columns(3)

for i, asset in enumerate(['WDO', 'DXY', '6L']):
    info = data[asset]
    with [col1, col2, col3][i]:
        if info['status'] == 'success':
            st.metric(
                label=f"{asset} ({info['symbol_used']})",
                value=f"{info['price']:.4f}",
                delta=f"{info['change_pct']:.2f}%"
            )
            st.caption(f"Abertura: {info['open']:.4f}")
        else:
            st.metric(label=asset, value="Indisponível", delta=None)
            st.error(f"Erro ao carregar {asset}")

st.divider()

# Tabela de Resumo para garantir que a tela nunca fique vazia
st.subheader("📋 Detalhes Técnicos")
df_rows = []
for asset, info in data.items():
    df_rows.append({
        "Ativo": asset,
        "Ticker": info['symbol_used'],
        "Preço": info['price'],
        "Variação %": f"{info['change_pct']:.2f}%" if info['status'] == 'success' else "N/A",
        "Status": "✅ Ativo" if info['status'] == 'success' else "❌ Falha"
    })

st.table(pd.DataFrame(df_rows))

st.caption("Dados processados via yfinance. Atualização automática a cada 30s.")
