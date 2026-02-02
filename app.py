import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    tf_code = data.get('timeframe', '15')
    
    # Map for yfinance
    tf_map = {"15": "15m", "240": "4h", "D": "1d"}
    interval = tf_map.get(tf_code, "15m")

    # Fetch Data (GC=F is Gold Futures)
    gold = yf.Ticker("GC=F")
    hist_d = gold.history(period="5d", interval="1d")
    hist_w = gold.history(period="1mo", interval="1wk")
    hist_m = gold.history(period="6mo", interval="1mo")
    current_candles = gold.history(period="1d", interval=interval)
    
    # 1. Previous Levels (Liquidity Points)
    pdh, pdl = hist_d['High'].iloc[-2], hist_d['Low'].iloc[-2]
    pwh, pwl = hist_w['High'].iloc[-2], hist_w['Low'].iloc[-2]
    pmh, pml = hist_m['High'].iloc[-2], hist_m['Low'].iloc[-2]

    # 2. Current Candle Extremes
    curr_low = current_candles['Low'].min()
    curr_high = current_candles['High'].max()

    # 3. Dynamic Zone Calculation
    # Buy Zone: Current Low to the lowest historical low
    buy_floor = min(pdl, pwl, pml)
    buy_range = f"{min(curr_low, buy_floor):.2f} - {max(curr_low, buy_floor):.2f}"

    # Sell Zone: Current High to the highest historical high
    sell_ceiling = max(pdh, pwh, pmh)
    sell_range = f"{min(curr_high, sell_ceiling):.2f} - {max(curr_high, sell_ceiling):.2f}"

    return jsonify({
        "sentiment": "NEUTRAL",
        "educational_note": f"Gold {interval} analysis complete. Watch horizontal rays.",
        "buy_range": buy_range,
        "sell_range": sell_range,
        "levels": {
            "pdh": pdh, "pdl": pdl, "pwh": pwh, "pwl": pwl, "pmh": pmh, "pml": pml
        }
    })
