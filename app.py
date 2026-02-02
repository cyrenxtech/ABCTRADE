import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    tf = data.get('timeframe', '15')
    
    # Map for Yahoo Finance
    tf_map = {"15": "15m", "240": "4h", "D": "1d"}
    interval = tf_map.get(tf, "15m")

    # Fetch Data
    gold = yf.Ticker("GC=F")
    hist_d = gold.history(period="5d", interval="1d")
    hist_w = gold.history(period="1mo", interval="1wk")
    hist_m = gold.history(period="6mo", interval="1mo")
    current_candles = gold.history(period="1d", interval=interval)
    
    # 6 Core Levels (Previous Periods)
    pdh, pdl = hist_d['High'].iloc[-2], hist_d['Low'].iloc[-2]
    pwh, pwl = hist_w['High'].iloc[-2], hist_w['Low'].iloc[-2]
    pmh, pml = hist_m['High'].iloc[-2], hist_m['Low'].iloc[-2]

    # Current Extremes
    curr_low = current_candles['Low'].min()
    curr_high = current_candles['High'].max()

    # Buy/Sell Zone Logic
    buy_low = min(curr_low, pdl, pwl, pml)
    buy_high = max(pdl, pwl, pml) # Resistance turned Support
    
    sell_high = max(curr_high, pdh, pwh, pmh)
    sell_low = min(pdh, pwh, pmh) # Support turned Resistance

    return jsonify({
        "sentiment": "BULLISH" if current_candles['Close'].iloc[-1] > pdl else "BEARISH",
        "educational_note": f"Analyzing {interval}. Watch for reaction at Yellow (Daily) rays.",
        "buy_range": f"{buy_low:.2f} - {buy_high:.2f}",
        "sell_range": f"{sell_low:.2f} - {sell_high:.2f}",
        "levels": {
            "pdh": pdh, "pdl": pdl, "pwh": pwh, "pwl": pwl, "pmh": pmh, "pml": pml
        }
    })
