# ARQUIVO 1: data_auto.py
import yfinance as yf
import pandas as pd

def get_auto_data():
    data = {}
    try:
        sixl_ticker = "6L=F"
        sixl = yf.download(sixl_ticker, period="1d", interval="5m", progress=False)
        if sixl.empty or len(sixl) == 0:
            raise ValueError("Sem dados para 6L")
        close_current = sixl["Close"].iloc[-1]
        open_day = sixl["Open"].iloc[0]
        max_6l = sixl["High"].max()
        min_6l = sixl["Low"].min()
        data["max_6l"] = max_6l
        data["min_6l"] = min_6l
        data["pct_6l"] = (close_current - open_day) / open_day * 100
        data["dist_max_6l"] = (close_current - max_6l) / max_6l * 100
        data["dist_min_6l"] = (close_current - min_6l) / min_6l * 100

        wdo_ticker = "WDOZ24.SA"
        wdo = yf.download(wdo_ticker, period="1d", interval="5m", progress=False)
        if wdo.empty or len(wdo) == 0:
            raise ValueError("Sem dados para WDO")
        data["preco_atual_wdo"] = wdo["Close"].iloc[-1]
        typical = (wdo["High"] + wdo["Low"] + wdo["Close"]) / 3
        vol_sum = wdo["Volume"].sum()
        if vol_sum > 0:
            data["vwap_wdo"] = (typical * wdo["Volume"]).sum() / vol_sum
        else:
            data["vwap_wdo"] = data["preco_atual_wdo"]

        dxy_ticker = "DX-Y.NYB"
        dxy = yf.download(dxy_ticker, period="5d", interval="1d", progress=False)
        if len(dxy) < 2:
            raise ValueError("Sem dados suficientes para DXY")
        prev_close = dxy["Close"].iloc[-2]
        curr_close = dxy["Close"].iloc[-1]
        data["dxy_pct"] = (curr_close - prev_close) / prev_close * 100

        return data
    except Exception as e:
        raise Exception(f"Erro ao coletar dados: {str(e)}")
