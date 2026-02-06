import os
import time
import threading
import yfinance as yf
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data_cache = {}

def update_gold_market_data():
    global data_cache
    while True:
        try:
            # Gold Futures Ticker
            gold_ticker = yf.Ticker("GC=F") 
            hist = gold_ticker.history(period="1d")
            
            if not hist.empty:
                live_price = hist['Close'].iloc[-1]
                formatted_price = f"${live_price:,.2f}"

                data_cache = {
                    "monthlyLevel": "PMH: $5,594 / PML: $4,400",
                    "weeklyLevel": "PWH: $5,100 / PWL: $4,720",
                    "dailyLevel": f"Live: {formatted_price} (PDH: $4,870 / PDL: $4,760)",
                    "entryAdvices": [
                        {"timeframe": "15M (Scalp)", "buy": "$4,820 – $4,835", "tp": "$4,870", "sl": "$4,805", "sell": "$4,890 – $4,910", "sellTP": "$4,840", "sellSL": "$4,925", "colorHex": "green"},
                        {"timeframe": "4H (Intraday)", "buy": "$4,720 – $4,760", "tp": "$5,000", "sl": "$4,680", "sell": "$5,050 – $5,120", "sellTP": "$4,870", "sellSL": "$5,180", "colorHex": "orange"},
                        {"timeframe": "Daily (Swing)", "buy": "$4,530 – $4,650", "tp": "$5,400", "sl": "$4,450", "sell": "$5,450 – $5,590", "sellTP": "$5,000", "sellSL": "$5,700", "colorHex": "blue"}
                    ],
                    "newsUpdates": [
                        {"title": "US-Iran Diplomacy", "impact": "BEARISH", "description": "High-level talks scheduled for Friday. Fear premium may drop."},
                        {"title": "Nasdaq AI Rout", "impact": "BULLISH", "description": "Tech sell-off driving safety bid into Gold."}
                    ],
                    "fundamentalAnalysis": [
                        {"title": "The 'Warsh' Correction", "bodyText": f"Institutional demand remains robust at {formatted_price}."}
                    ]
                }
                print(f"✅ Market Data Synced: {formatted_price}")
        except Exception as e:
            print(f"❌ Sync Error: {e}")
        
        time.sleep(60)

# START THREAD HERE (Outside main)
# This ensures it runs even when Gunicorn starts the app
sync_thread = threading.Thread(target=update_gold_market_data, daemon=True)
sync_thread.start()

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    if not data_cache:
        return jsonify({"error": "Data warming up..."}), 503
    return jsonify(data_cache)

# This part is only for local testing
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
