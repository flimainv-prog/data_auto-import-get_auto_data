# data_auto.py
import yfinance as yf
import pandas as pd
import numpy as np

def get_assets_data():
    tickers_map = {
        'WDO': 'USDBRL=X',
        'DXY': 'DX=F',
        '6L': 'GBPUSD=X'
    }
    data = {}
    for name, symbol in tickers_map.items():
        asset_data = fetch_asset(symbol)
        data[name] = asset_data
    return data

def fetch_asset(symbol):
    result = {'status': 'ERRO', 'price': np.nan, 'change_pct': np.nan, 'symbol': symbol}

    # Tentativa 1: history(5d)
    try:
        hist = yf.Ticker(symbol).history(period='5d')
        if not hist.empty and len(hist) >= 2:
            latest_close = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2]
            change_pct = ((latest_close - prev_close) / prev_close) * 100
            result = {'status': 'OK', 'price': float(latest_close), 'change_pct': float(change_pct), 'symbol': symbol}
            return result
    except Exception:
        pass

    # Tentativa 2: download(5d)
    try:
        dl = yf.download(symbol, period='5d', progress=False)
        if not dl.empty and len(dl) >= 2:
            latest_close = dl['Close'].iloc[-1]
            prev_close = dl['Close'].iloc[-2]
            change_pct = ((latest_close - prev_close) / prev_close) * 100
            result = {'status': 'OK', 'price': float(latest_close), 'change_pct': float(change_pct), 'symbol': symbol}
            return result
    except Exception:
        pass

    # Tentativa 3: info
    try:
        info = yf.Ticker(symbol).info
        price = (info.get('regularMarketPrice') or
                 info.get('currentPrice') or
                 info.get('bid') or
                 info.get('ask'))
        if price:
            change_pct = info.get('regularMarketChangePercent', np.nan)
            result = {'status': 'OK', 'price': float(price), 'change_pct': float(change_pct) if not np.isnan(change_pct) else np.nan, 'symbol': symbol}
            return result
    except Exception:
        pass

    return result


# app.py
import streamlit as st
import pandas as pd
import numpy as np
import data_auto

from streamlit import cache_data

st.set_page_config(page_title="Dashboard Ativos", layout="wide")

@cache_data(ttl=300)
def load_data():
    return data_auto.get_assets_data()

st.title("🪙 Dashboard de Ativos")

col1, col2, col3 = st.columns(3)

data = load_data()

with col1:
    wdo = data['WDO']
    price_str = f"{wdo['price']:.4f}" if not np.isnan(wdo['price']) else "N/A"
    delta_str = f"{wdo['change_pct']:.2f}%" if not np.isnan(wdo['change_pct']) else None
    st.metric("WDO", price_str, delta=delta_str)

with col2:
    dxy = data['DXY']
    price_str = f"{dxy['price']:.4f}" if not np.isnan(dxy['price']) else "N/A"
    delta_str = f"{dxy['change_pct']:.2f}%" if not np.isnan(dxy['change_pct']) else None
    st.metric("DXY", price_str, delta=delta_str)

with col3:
    l6 = data['6L']
    price_str = f"{l6['price']:.4f}" if not np.isnan(l6['price']) else "N/A"
    delta_str = f"{l6['change_pct']:.2f}%" if not np.isnan(l6['change_pct']) else None
    st.metric("6L", price_str, delta=delta_str)

if st.button("🔄 Atualizar Dados", type="primary"):
    cache_data.clear()
    st.rerun()

st.subheader("📊 Tabela Consolidada")
df_data = []
for key, asset in data.items():
    df_data.append({
        'Ativo': key,
        'Símbolo': asset['symbol'],
        'Status': asset['status'],
        'Preço': f"{asset['price']:.4f}" if not np.isnan(asset['price']) else "N/A",
        'Variação %': f"{asset['change_pct']:.2f}%" if not np.isnan(asset['change_pct']) else "N/A"
    })

df = pd.DataFrame(df_data)
st.table(df)
