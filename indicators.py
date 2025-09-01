import pandas as pd, pandas_ta as ta
from config import THRESHOLDS

def evaluate_signals(candles):
    df = pd.DataFrame(candles)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    signals = {}

    df["EMA9"] = ta.ema(df["close"], length=9)
    df["EMA21"] = ta.ema(df["close"], length=21)
    if df["EMA9"].iat[-2] < df["EMA21"].iat[-2] and df["EMA9"].iat[-1] > df["EMA21"].iat[-1]:
        signals["EMA_Crossover"] = "buy"

    macd = ta.macd(df["close"])
    if macd["MACD_12_26_9"].iat[-1] > macd["MACDs_12_26_9"].iat[-1] and macd["MACD_12_26_9"].iat[-1] > 0:
        signals["MACD"] = "buy"

    rsi = ta.rsi(df["close"], length=14)
    if rsi.iat[-2] < 30 and rsi.iat[-1] > 30:
        signals["RSI_Rebound"] = "buy"

    lows = df["close"].rolling(40).apply(lambda x: x.idxmin())
    rsi_lows = rsi.loc[lows.dropna().astype(int)]
    if len(rsi_lows) >= 2 and rsi_lows.iloc[-1] > rsi_lows.iloc[-2]:
        signals["RSI_Divergence"] = "buy"

    stoch = ta.stoch(df["high"], df["low"], df["close"], k=14, d=3)
    k = stoch["STOCHk_14_3_3"]
    lows = df["close"].rolling(40).apply(lambda x: x.idxmin())
    k_lows = k.loc[lows.dropna().astype(int)]
    if len(k_lows) >= 2 and k_lows.iloc[-1] > k_lows.iloc[-2]:
        signals["Stoch_Divergence"] = "buy"

    bb = ta.bbands(df["close"], length=20, std=2)
    if df["close"].iat[-1] > bb["BBU_20_2.0"].iat[-1]:
        signals["Bollinger_Breakout"] = "buy"

    vol_ma = df["volume"].rolling(20).mean()
    if df["volume"].iat[-1] > THRESHOLDS["volume_surge_pct"] * vol_ma.iat[-1]:
        signals["Volume_Surge"] = "buy"

    atr = ta.atr(df["high"], df["low"], df["close"], length=14)
    atr_ma = atr.rolling(20).mean()
    if atr.iat[-1] > THRESHOLDS["atr_multiple"] * atr_ma.iat[-1]:
        signals["ATR_Surge"] = "buy"

    bandwidth = bb["BBU_20_2.0"] - bb["BBL_20_2.0"]
    bw_ma = bandwidth.rolling(20).mean()
    if bandwidth.iat[-1] > THRESHOLDS["boll_bandwidth_multiple"] * bw_ma.iat[-1]:
        signals["Bollinger_Bandwidth"] = "buy"

    return signals
