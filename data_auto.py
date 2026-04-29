import yfinance as yf
import pandas as pd
import numpy as np


def fetch_symbol(tickers):
    for symbol in tickers:
        try:
            ticker_obj = yf.Ticker(symbol)
            hist = ticker_obj.history(period='2d', interval='1d')
            if not hist.empty and len(hist) >= 1:
                price = hist['Close'].iloc[-1]
                open_price = hist['Open'].iloc[-1]
                prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else np.nan
                change_abs = price - prev_close if not np.isnan(prev_close) else np.nan
                change_pct = (change_abs / prev_close * 100) if not np.isnan(prev_close) else np.nan
                source = 'history'
                df = hist.tail(5)
                return {
                    'symbol_used': symbol,
                    'status': 'OK',
                    'price': float(price),
                    'open': float(open_price),
                    'previous_close': float(prev_close) if not np.isnan(prev_close) else np.nan,
                    'change_abs': float(change_abs) if not np.isnan(change_abs) else np.nan,
                    'change_pct': float(change_pct) if not np.isnan(change_pct) else np.nan,
                    'source': source,
                    'dataframe': df
                }
            # Fallback to info
            info = ticker_obj.info
            price = info.get('regularMarketPrice') or info.get('currentPrice')
            if price:
                open_price = info.get('regularMarketOpen', np.nan)
                prev_close = info.get('regularMarketPreviousClose', np.nan)
                change_abs = info.get('regularMarketChange', np.nan)
                change_pct = info.get('regularMarketChangePercent', np.nan)
                source = 'info'
                return {
                    'symbol_used': symbol,
                    'status': 'OK',
                    'price': float(price),
                    'open': float(open_price) if not np.isnan(open_price) else np.nan,
                    'previous_close': float(prev_close) if not np.isnan(prev_close) else np.nan,
                    'change_abs': float(change_abs) if not np.isnan(change_abs) else np.nan,
                    'change_pct': float(change_pct) if not np.isnan(change_pct) else np.nan,
                    'source': source,
                    'dataframe': None
                }
        except Exception:
            continue
    # Fallback if all fail
    return {
        'symbol_used': 'Nenhum',
        'status': 'Dados indisponíveis no momento. Tente novamente mais tarde.',
        'price': np.nan,
        'open': np.nan,
        'previous_close': np.nan,
        'change_abs': np.nan,
        'change_pct': np.nan,
        'source': 'N/A',
        'dataframe': None
    }


def get_auto_data():
    data = {}
    # WDO
    wdo_tickers = ['USDBRL=X', 'BRL=X']
    data['WDO'] = fetch_symbol(wdo_tickers)
    # DXY
    dxy_tickers = ['DX-Y.NYB', 'DX=F', 'DXY']
    data['DXY'] = fetch_symbol(dxy_tickers)
    # 6L
    sixl_tickers = ['6L=F']
    data['6L'] = fetch_symbol(sixl_tickers)
    return data
