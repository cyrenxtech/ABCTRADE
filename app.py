import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    tf = data.get('timeframe', '15')
    
    # Logic configuration based on your requirements
    # Assuming a base price of 2030.00 for XAUUSD (Gold) if no live feed is connected yet
    base_price = 2030.00 
    
    if tf == "D":
        pip_range = 20.0  # 200 Pips for Gold ($20.00)
        note = "Daily Bias: Identifying institutional supply/demand over 200 pip volatility."
    elif tf == "240":
        pip_range = 10.0  # 100 Pips ($10.00)
        note = "4H Bias: Identifying H4 supply/demand over 100 pip volatility."
    else:
        pip_range = 5.0   # 50 Pips ($5.00)
        note = "15M Bias: Scalping range identified over 50 pip volatility."

    # Fibo/Supply-Demand Logic (Simplified calculation)
    # Buy Zone: Lowest Low to Lowest High area (Demand)
    buy_low = base_price - (pip_range / 2)
    buy_high = buy_low + (pip_range * 0.23) # Bottom 23% of the range
    
    # Sell Zone: Highest Low to Highest High area (Supply)
    sell_high = base_price + (pip_range / 2)
    sell_low = sell_high - (pip_range * 0.23) # Top 23% of the range

    return jsonify({
        "sentiment": "NEUTRAL",
        "educational_note": note,
        "buy_range": f"${buy_low:.2f} - ${buy_high:.2f}",
        "sell_range": f"${sell_low:.2f} - ${sell_high:.2f}"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
