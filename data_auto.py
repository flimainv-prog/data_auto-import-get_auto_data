import yfinance as yf
import pandas as pd
import numpy as np

def get_auto_data():
    result = {}
    
    # WDO - USD/BRL (ticker sempre disponível)
    try:
        wdo = yf.download('USDBRL=X', period='2d', progress=False)
        if not wdo.empty:
            latest = wdo.iloc[-1]
            prev = wdo.iloc[-2] if len(wdo) > 1 else latest
            result['WDO'] = {
                'status': 'OK',
                'symbol': 'USDBRL=X',
                'price': float(latest['Close']),
                'open': float(latest['Open']),
                'change_abs': float(latest['Close'] - prev['Close']),
                'change_pct': float((latest['Close'] - prev['Close']) / prev['Close'] * 100)
            }
        else:
            result['WDO'] = {'status': 'erro', 'price': 0, 'change_pct': 0}
    except Exception as e:
        result['WDO'] = {'status': 'erro', 'price': 0, 'change_pct': 0}
    
    # DXY
    try:
        dxy = yf.download('DX=F', period='2d', progress=False)
        if not dxy.empty:
            latest = dxy.iloc[-1]
            prev = dxy.iloc[-2] if len(dxy) > 1 else latest
            result['DXY'] = {
                'status': 'OK',
                'symbol': 'DX=F',
                'price': float(latest['Close']),
                'open': float(latest['Open']),
                'change_abs': float(latest['Close']
