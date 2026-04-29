import yfinance as yf
import pandas as pd
import numpy as np


def fetch_single_asset(tickers):
    # Tenta snapshot via info
    for sym in tickers:
        try:
            ticker_obj = yf.Ticker(sym)
            info = ticker_obj.info
            price = info.get('regularMarketPrice') or info.get('currentPrice')
            if price is None:
                continue
            open_price = info.get('regularMarketOpen')
            prev_close = info.get('regularMarketPreviousClose')
            change_abs = info.get('regularMarketChange')
            if change_abs is None and prev_close is not None:
                change_abs = price - prev_close
            change_pct = info.get('regularMarketChangePercent')
            if change_pct is None and prev_close is not None and prev_close != 0:
                change_pct = (change_abs / prev_close) * 100
            return {
                'symbol_used': sym,
                'status': 'OK',
                'price': float(price),
                'open': float(open_price) if open_price else np.nan,
                'previous_close': float(prev_close) if prev_close else np.nan,
                'change_abs': float(change_abs) if change_abs else np.nan,
                'change_pct': float(change_pct) if change_pct else np.nan,
                'source': 'yfinance.info'
            }
        except Exception:
            continue

    # Fallback para history diário
    for sym in tickers:
        try:
            data = yf.download(sym, period='5d', interval='1d', progress=False, group_by='ticker')
            if isinstance(data, pd.DataFrame) and not data.empty and len(data) >= 2:
                data = data['Close'].dropna() if 'Close' in data.columns else data
                if len(data) >= 2:
                    last_close = data.iloc[-1]
                    prev_close = data.iloc[-2]
                    change_abs = last_close - prev_close
                    change_pct = (change_abs / prev_close) * 100 if prev_close != 0 else np.nan
                    # Pega open do último dia
                    full_data = yf.download(sym, period='2d', interval='1d', progress=False)
                    open_price = full_data['Open'].iloc[-1] if not full_data.empty else np.nan
                    return {
                        'symbol_used': sym,
                        'status': 'Fallback diário',
                        'price': float(last_close),
                        'open': float(open_price),
                        'previous_close': float(prev_close),
                        'change_abs': float(change_abs),
                        'change_pct': float(change_pct),
                        'source': 'yfinance.history 1d'
                    }
        except Exception:
            continue

    return {
        'symbol_used': None,
        'status': 'Sem dados disponíveis',
        'price': np.nan,
        'open': np.nan,
        'previous_close': np.nan,
        'change_abs': np.nan,
        'change_pct': np.nan,
        'source': None,
    }


def get_auto_data():
    assets = {
        'WDO': ['USDBRL=X', 'BRL=X'],
        'DXY': ['DX-Y.NYB', 'DX=F', 'DXY'],
        '6L': ['6L=F', 'GBPUSD=X']
    }
    result = {}
    for asset, tickers in assets.items():
        result[asset] = fetch_single_asset(tickers)
    return result
