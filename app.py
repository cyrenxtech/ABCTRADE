import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    tf_input = data.get('timeframe', '15')
    
    # Map timeframes for yfinance
    tf_map = {"15": "15m", "240": "4h", "D": "1d"}
    current_tf = tf_map.get(tf_input, "15m")

    # 1. Fetch Gold Data (GC=F is the Gold Futures proxy for XAUUSD)
    gold = yf.Ticker("GC=F")
    hist_d = gold.history(period="5d", interval="1d")
    hist_w = gold.history(period="1mo", interval="1wk")
    hist_m = gold.history(period="6mo", interval="1mo")
    current_candles = gold.history(period="1d", interval=current_tf)

    # 2. Get 6 Core Horizontal Ray Levels
    pdh, pdl = hist_d['High'].iloc[-2], hist_d['Low'].iloc[-2]
    pwh, pwl = hist_w['High'].iloc[-2], hist_w['Low'].iloc[-2]
    pmh, pml = m_h = hist_m['High'].iloc[-2], hist_m['Low'].iloc[-2]

    # 3. Get Current Candle Extremes
    curr_low = current_candles['Low'].min()
    curr_high = current_candles['High'].max()

    # 4. Refined Zone Logic
    # Buy Zone: Current Low to the Lowest of (PDL, PWL, PML)
    buy_floor = min(pdl, pwl, pml)
    buy_range = f"{min(curr_low, buy_floor):.2f} - {max(curr_low, buy_floor):.2f}"

    # Sell Zone: Current High to the Highest of (PDH, PWH, PMH)
    sell_ceiling = max(pdh, pwh, pmh)
    sell_range = f"{min(curr_high, sell_ceiling):.2f} - {max(curr_high, sell_ceiling):.2f}"

    return jsonify({
        "sentiment": "ANALYZING",
        "educational_note": f"Trend Check: Current {current_tf} candle is testing liquidity levels.",
        "buy_range": buy_range,
        "sell_range": sell_range,
        "levels": {
            "pdh": pdh, "pdl": pdl, "pwh": pwh, "pwl": pwl, "pmh": pmh, "pml": pml
        }
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
