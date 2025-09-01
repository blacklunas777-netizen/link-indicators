import pandas as pd
import pandas_ta as ta
from config import THRESHOLDS

def evaluate_signals(candles):
    df = pd.DataFrame(candles)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    signals = {}

   # MACD
    macd = ta.macd(df["close"])
    if macd["MACD_12_26_9"].iat[-1] > macd["MACDs_12_26_9"].iat[-1] and macd["MACD_12_26_9"].iat[-1] > 0:
        signals["MACD"] = "buy"

    # RSI rebound
    rsi = ta.rsi(df["close"], length=14)
    if rsi.iat[-2] < 30 and rsi.iat[-1] > 30:
        signals["RSI_Rebound"] = "buy"

    # RSI bullish divergence
    lows = df["close"].rolling(40).apply(lambda x: x.idxmin())
    rsi_lows = rsi.loc[lows.dropna().astype(int)]
    if len(rsi_lows) >= 2 and rsi_lows.iloc[-1] > rsi_lows.iloc[-2]:
        signals["RSI_Divergence"] = "buy"

    return signals
