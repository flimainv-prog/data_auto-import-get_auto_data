# data_auto.py

import yfinance as yf
import pandas as pd
import numpy as np


def get_data_for_asset(asset_name, ticker_candidates):
    for ticker in ticker_candidates:
        try:
            data = yf.download(ticker, period="5d", interval="1d", progress=False, group_by=None)
            if not data.empty:
                closes = data['Close'].dropna()
                if len(closes) >= 2:
                    latest_close = closes.iloc[-1]
                    prev_close = closes.iloc[-2]
                    variation = ((latest_close - prev_close) / prev_close) * 100
                    return {
                        'price': float(latest_close),
                        'var': float(variation),
                        'status': 'ok'
                    }
                elif len(closes) == 1:
                    return {
                        'price': float(closes.iloc[-1]),
                        'var': np.nan,
                        'status': 'partial'
                    }
        except Exception:
            continue
    return {
        'price': np.nan,
        'var': np.nan,
        'status': f'{asset_name} indisponível'
    }


def get_auto_data():
    wdo_data = get_data_for_asset('WDO', ['WDOZ24.SA', 'WDOY24.SA', 'WDOV24.SA', 'WDOU24.SA', 'USDBRL=X'])
    dxy_data = get_data_for_asset('DXY', ['DX-Y.NYB', 'DXY'])
    sixl_data = get_data_for_asset('6L', ['6LZ24.SA', '6LY24.SA', '6LV24.SA', '6LU24.SA'])
    return {
        'WDO': wdo_data,
        'DXY': dxy_data,
        '6L': sixl_data
    }


# app.py

import streamlit as st
import pandas as pd
import numpy as np
from data_auto import get_auto_data


st.set_page_config(page_title="Dados Auto", page_icon="📈", layout="wide")

st.title("📈 Dados de Mercado Automatizados")

@st.cache_data(ttl=30)
def fetch_data():
    return get_auto_data()

data = fetch_data()

# Botão de atualização manual
col_btn, col_spacer, col_spacer2 = st.columns([1, 2, 2])
with col_btn:
    if st.button("🔄 Atualizar Dados", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Métricas rápidas
col1, col2, col3 = st.columns(3)

with col1:
    wdo = data['WDO']
    wdo_price = f"R$ {wdo['price']:.4f}" if not np.isnan(wdo['price']) else "Indisponível"
    wdo_delta = f"{wdo['var']:+.2f}%" if not np.isnan(wdo['var']) else "--"
    st.metric("WDO", wdo_price, wdo_delta)

with col2:
    dxy = data['DXY']
    dxy_price = f"{dxy['price']:.2f}" if not np.isnan(dxy['price']) else "Indisponível"
    dxy_delta = f"{dxy['var']:+.2f}%" if not np.isnan(dxy['var']) else "--"
    st.metric("DXY", dxy_price, dxy_delta)

with col3:
    sixl = data['6L']
    if np.isnan(sixl['price']):
        st.warning("⚠️ 6L indisponível no momento.")
    else:
        sixl_price = f"{sixl['price']:.4f}"
        sixl_delta = f"{sixl['var']:+.2f}%"
        st.metric("6L", sixl_price, sixl_delta)

# Tabela completa
st.subheader("📊 Tabela de Dados")
df_dict = []
for asset, info in data.items():
    price_str = f"{info['price']:.4f}" if not np.isnan(info['price']) else "N/A"
    var_str = f"{info['var']:+.2f}%" if not np.isnan(info['var']) else "N/A"
    df_dict.append({
        'Ativo': asset,
        'Preço': price_str,
        'Variação (%)': var_str,
        'Status': info['status']
    })
df = pd.DataFrame(df_dict)
st.dataframe(df, use_container_width=True, hide_index=True)
