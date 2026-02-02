
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_live_data(symbol="GC=F"): # Gold Futures symbol
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="5d", interval="1h")
    if df.empty:
        return 2035.00, "Neutral"
    
    current_price = df['Close'].iloc[-1]
    # Simple Trend Logic: Compare current price to 5-period average
    avg_price = df['Close'].mean()
    trend = "BULLISH" if current_price > avg_price else "BEARISH"
    
    return current_price, trend

def calculate_zones(base_price, pip_range, trend):
    # Fibo-based Demand/Supply logic
    buy_low = base_price - (pip_range * 0.5)
    buy_high = buy_low + (pip_range * 0.236)
    
    sell_high = base_price + (pip_range * 0.5)
    sell_low = sell_high - (pip_range * 0.236)

    # Dynamic AI Suggestion
    if trend == "BULLISH":
        note = f"Trend is UP. Look for entries at the Demand Zone (${buy_high:.2f}). Target: Next high."
    else:
        note = f"Trend is DOWN. Look for shorts at the Supply Zone (${sell_low:.2f}). Target: Liquidity low."
    
    return buy_low, buy_high, sell_low, sell_high, note

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    tf = data.get('timeframe', '15')
    
    # 1. Get REAL live price and trend
    live_price, live_trend = get_live_data()

    # 2. Assign Pip Range based on timeframe
    if tf == "D":
        pip_val = 20.0
    elif tf == "240":
        pip_val = 10.0
    else:
        pip_val = 5.0

    # 3. Calculate dynamic zones and AI suggestions
    b_low, b_high, s_low, s_high, ai_suggestion = calculate_zones(live_price, pip_val, live_trend)

    return jsonify({
        "sentiment": live_trend,
        "educational_note": ai_suggestion,
        "buy_range": f"{b_low:.2f} - {b_high:.2f}",
        "sell_range": f"{s_low:.2f} - {s_high:.2f}"
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
