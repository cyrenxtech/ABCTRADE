import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    tf = data.get('timeframe', '15')
    
    # In a real app, you'd use 'yfinance' or 'alpha_vantage' here.
    # For now, let's create dynamic logic based on the time.
    hour = datetime.datetime.now().hour
    
    # Logic: If it's London/NY session, be more "Bullish"
    sentiment = "BULLISH" if 8 <= hour <= 17 else "NEUTRAL"
    
    educational_note = f"Analysis for {tf}M timeframe: "
    if sentiment == "BULLISH":
        educational_note += "Price is holding above the Weekly Open. Look for a liquidity sweep of PDH before targeting higher expansion."
    else:
        educational_note += "Market is in a consolidation phase. Avoid trading inside the range until displacement is clear."

    return jsonify({
        "sentiment": sentiment,
        "educational_note": educational_note,
        "buy_range": "$2025.50 - $2028.00",
        "sell_range": "$2045.10 - $2048.50"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
