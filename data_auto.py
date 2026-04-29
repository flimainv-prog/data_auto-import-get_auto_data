import yfinance as yf
import pandas as pd
import numpy as np

def process_df(df, symbol, source):
    if df.empty or len(df) < 1:
        return None
    price = float(df['Close'].iloc[-1])
    open_price = float(df['Open'].iloc[-1])
    previous_close = float(df['Close'].iloc[-2]) if len(df) >= 2 else np.nan
    change_abs = price - previous_close if not np.isnan(previous_close) else np.nan
    change_pct = (change_abs / previous_close * 100) if not np.isnan(previous_close) and previous_close != 0 else np.nan
    return {
        'symbol_used': symbol,
        'status': 'success',
        'price': price,
        'open': open_price,
        'previous_close': previous_close,
        'change_abs': change_abs,
        'change_pct': change_pct,
        'source': source
    }

def fetch_asset_data(tickers, asset_name):
    strategies = [('1d', '5m'), ('2d', '1h'), ('5d', '1d')]
    for ticker in tickers:
        for period, interval in strategies:
            try:
                df = yf.download(ticker, period=period, interval=interval, progress=False, group_by=None)
                result = process_df(df, ticker, f'{interval}_{period}')
                if result:
                    return result
            except Exception:
                continue
    return {
        'symbol_used': None,
        'status': f'Dados indisponíveis para {asset_name}. Todos os tickers falharam.',
        'price': np.nan,
        'open': np.nan,
        'previous_close': np.nan,
        'change_abs': np.nan,
        'change_pct': np.nan,
        'source': None
    }

def get_auto_data():
    data = {}
    data['WDO'] = fetch_asset_data(['USDBRL=X', 'BRL=X'], 'WDO')
    data['DXY'] = fetch_asset_data(['DX-Y.NYB', 'DX=F', 'DXY'], 'DXY')
    data['6L'] = fetch_asset_data(['6L=F', 'GBPUSD=X'], '6L')
    return data
