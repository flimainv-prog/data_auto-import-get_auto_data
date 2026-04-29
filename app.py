import streamlit as st
import pandas as pd
from data_auto import get_auto_data


st.set_page_config(page_title="Dashboard WDO, DXY e 6L", layout="wide")

st.title("📊 Dashboard Financeiro: WDO, DXY e 6L")

@st.cache_data(ttl=30)
def load_data():
    return get_auto_data()

data = load_data()

# Cards métricos
st.subheader("Resumo dos Ativos")
col1, col2, col3 = st.columns(3)
assets = ['WDO', 'DXY', '6L']

for i, asset in enumerate(assets):
    cols = [col1, col2, col3]
    with cols[i]:
        d = data[asset]
        if d['status'] == 'available':
            st.metric(
                label=f"{asset} ({d['symbol_used']})",
                value=f"{d['price']:.4f}",
                delta=f"{d['change_pct']:.2f}%"
            )
            st.caption(f"Abertura: {d['open']:.4f} | Fech. Ant: {d['previous_close']:.4f}")
        else:
            st.warning(f"⚠️ {asset} indisponível no momento.")
            st.caption("Sem dados recentes disponíveis. Tentando symbols alternativos...")

# Tabela consolidada
st.subheader("Tabela Consolidada")
table_data = []
for asset in assets:
    d = data[asset]
    table_data.append({
        'Ativo': asset,
        'Símbolo': d['symbol_used'] or 'N/A',
        'Status': d['status'].upper(),
        'Preço Atual': d.get('price', 'N/A'),
        'Variação %': f"{d.get('change_pct', 0):.2f}%" if d.get('change_pct') is not None else 'N/A',
        'Variação Abs': f"{d.get('change_abs', 0):.4f}" if d.get('change_abs') is not None else 'N/A',
        'Fonte': d['source']
    })

df_table = pd.DataFrame(table_data)
st.dataframe(df_table, use_container_width=True, hide_index=True)

st.caption("* Dados atualizados a cada 30 segundos via cache. Fonte: yfinance.")
