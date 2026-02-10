from flask import Flask, jsonify
from flask_cors import CORS
import os
import requests
import re

app = Flask(__name__)
CORS(app)

def get_live_gold_price():
    """
    Fetches real-time gold price without an API key by 
    parsing public market data.
    """
    try:
        # Using a reliable public source for price fetching
        response = requests.get("https://data-asid.goldprice.org/db_otc_gold_all.php", timeout=5)
        data = response.json()
        # Extracting the spot price (USD)
        price = float(data['ts_gold_all'][0]['ask'])
        return price
    except Exception as e:
        print(f"Price Fetch Error: {e}")
        return 2650.00  # Fallback price if scraper fails

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    current_price = get_live_gold_price()
    
    # This matches your Swift 'GoldResponse' model exactly
    return jsonify({
        "price": current_price,
        "monthlyLevel": "H: 2750.50 / L: 2610.20",
        "weeklyLevel": "H: 2690.00 / L: 2635.40",
        "dailyLevel": "H: 2672.10 / L: 2648.80",
        "entryAdvices": [
            {
                "timeframe": "15M",
                "buy": "2652.00",
                "tp": "2665.00",
                "sl": "2644.00",
                "colorHex": "green"
            },
            {
                "timeframe": "4H",
                "buy": "2615.00",
                "tp": "2700.00",
                "sl": "2590.00",
                "colorHex": "orange"
            }
        ],
        "newsUpdates": [
            {
                "title": "DXY Resistance Hit",
                "impact": "BULLISH",
                "description": "Dollar Index rejected at 105.20. Gold holding support."
            },
            {
                "title": "Treasury Yields Steady",
                "impact": "NEUTRAL",
                "description": "10Y yields stabilizing before the NY session open."
            }
        ],
        "fundamentalAnalysis": [
            {
                "title": "Market Sentiment",
                "bodyText": "Institutional buyers are clustering around the 2640 zone."
            }
        ],
        # If you want to force an alert popup on everyone's phone:
        "activeAlert": None 
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
