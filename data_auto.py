# data_auto.py

import yfinance as yf
import pandas as pd
from datetime import datetime


def get_auto_data():
    data = {}

    # Função auxiliar para buscar dados de um ativo
    def fetch_asset_data(symbols, is_brazilian=False):
        df = pd.DataFrame()
        sym_used = None
        for sym in symbols:
            try:
                full_sym = sym + '.SA' if is_brazilian else sym
                temp_df = yf.download(full_sym, period='5d', progress=False)
                if not temp_df.empty and len(temp_df) >= 2:
                    df = temp_df
                    sym_used = full_sym
                    break
            except:
                continue
        return df, sym_used

    # WDO - gera símbolos automáticos para próximos meses
    wdo_symbols = []
    now = datetime.now()
    month_letters = 'FGHJKMNQUVXZ'
    for i in range(6):
        month_idx = (now.month - 1 + i) % 12
        year_suffix = str(now.year + ((now.month - 1 + i) // 12))[-2:]
        wdo_symbols.append(f'WDO{month_letters[month_idx]}{year_suffix}')
    wdo_df, wdo_sym = fetch_asset_data(wdo_symbols, is_brazilian=True)

    if wdo_sym and not wdo_df.empty:
        latest = wdo_df.iloc[-1]
        prev = wdo_df.iloc[-2]
        data['WDO'] = {
            'symbol_used': wdo_sym,
            'status': 'available',
            'price': float(latest['Close']),
            'open': float(latest['Open']),
            'previous_close': float(prev['Close']),
            'change_abs': float(latest['Close'] - prev['Close']),
            'change_pct': float((latest['Close'] - prev['Close']) / prev['Close'] * 100),
            'source': 'yfinance',
            'dataframe': wdo_df[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10).round(2).to_dict('records')
        }
    else:
        data['WDO'] = {
            'symbol_used': None,
            'status': 'unavailable',
            'price': None,
            'open': None,
            'previous_close': None,
            'change_abs': None,
            'change_pct': None,
            'source': 'yfinance'
        }

    # DXY
    dxy_symbols = ['DX=F', '^NYICDX', 'DXY']
    dxy_df, dxy_sym = fetch_asset_data(dxy_symbols)
    if dxy_sym and not dxy_df.empty:
        latest = dxy_df.iloc[-1]
        prev = dxy_df.iloc[-2]
        data['DXY'] = {
            'symbol_used': dxy_sym,
            'status': 'available',
            'price': float(latest['Close']),
            'open': float(latest['Open']),
            'previous_close': float(prev['Close']),
            'change_abs': float(latest['Close'] - prev['Close']),
            'change_pct': float((latest['Close'] - prev['Close']) / prev['Close'] * 100),
            'source': 'yfinance',
            'dataframe': dxy_df[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10).round(4).to_dict('records')
        }
    else:
        data['DXY'] = {
            'symbol_used': None,
            'status': 'unavailable',
            'price': None,
            'open': None,
            'previous_close': None,
            'change_abs': None,
            'change_pct': None,
            'source': 'yfinance'
        }

    # 6L - fallbacks (pode ser futuro ou outro ativo)
    sixl_symbols = ['6L=F', '6L', '6LF24']
    sixl_df, sixl_sym = fetch_asset_data(sixl_symbols)
    if sixl_sym and not sixl_df.empty:
        latest = sixl_df.iloc[-1]
        prev = sixl_df.iloc[-2]
        data['6L'] = {
            'symbol_used': sixl_sym,
            'status': 'available',
            'price': float(latest['Close']),
            'open': float(latest['Open']),
            'previous_close': float(prev['Close']),
            'change_abs': float(latest['Close'] - prev['Close']),
            'change_pct': float((latest['Close'] - prev['Close']) / prev['Close'] * 100),
            'source': 'yfinance',
            'dataframe': sixl_df[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10).round(4).to_dict('records')
        }
    else:
        data['6L'] = {
            'symbol_used': None,
            'status': 'unavailable',
            'price': None,
            'open': None,
            'previous_close': None,
            'change_abs': None,
            'change_pct': None,
            'source': 'yfinance'
        }

    return data


# app.py

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
