import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_live_data(symbol="GC=F"):
    try:
        ticker = yf.Ticker(symbol)
        # Fetching 5 days of 1h data to calculate trend
        df = ticker.history(period="5d", interval="1h")
        if df.empty:
            return 2035.00, "NEUTRAL"
        
        current_price = df['Close'].iloc[-1]
        avg_price = df['Close'].mean()
        trend = "BULLISH" if current_price > avg_price else "BEARISH"
        return current_price, trend
    except Exception as e:
        print(f"Error fetching data: {e}")
        return 2035.00, "NEUTRAL"

def calculate_zones(base_price, pip_range, trend):
    # Fibo-based Demand (0.0 - 0.236) and Supply (0.786 - 1.0)
    buy_low = base_price - (pip_range * 0.5)
    buy_high = buy_low + (pip_range * 0.236)
    
    sell_high = base_price + (pip_range * 0.5)
    sell_low = sell_high - (pip_range * 0.236)

    if trend == "BULLISH":
        note = f"Trend is UP. Look for entries at Demand (${buy_high:.2f}). Target: Recent Highs."
    elif trend == "BEARISH":
        note = f"Trend is DOWN. Look for shorts at Supply (${sell_low:.2f}). Target: Liquidity Lows."
    else:
        note = "Market neutral. Watch for break of structure before entry."
    
    return buy_low, buy_high, sell_low, sell_high, note

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    tf = data.get('timeframe', '15')
    
    price, trend = get_live_data()

    # Dynamic pip range based on volatility of Gold per timeframe
    if tf == "D":
        pip_val = 30.0 # Daily swing
    elif tf == "240":
        pip_val = 15.0 # 4H range
    else:
        pip_val = 7.0  # 15M scalp

    b_low, b_high, s_low, s_high, note = calculate_zones(price, pip_val, trend)

    return jsonify({
        "sentiment": trend,
        "educational_note": note,
        "buy_range": f"{b_low:.2f} - {b_high:.2f}",
        "sell_range": f"{s_low:.2f} - {s_high:.2f}"
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
