import os
import time
import threading
import yfinance as yf
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global cache to store the "Live" version of your data
data_cache = {}

def update_gold_market_data():
    """Background task to fetch live gold prices every 60 seconds."""
    global data_cache
    while True:
        try:
            # Fetch Gold Spot Price (XAU/USD)
            gold_ticker = yf.Ticker("GC=F") # Gold Futures
            hist = gold_ticker.history(period="1d")
            live_price = hist['Close'].iloc[-1]
            formatted_price = f"${live_price:,.2f}"

            # Update the global cache while keeping your specific structure
            data_cache = {
                "monthlyLevel": f"PMH: $5,594 / PML: $4,400",
                "weeklyLevel": f"PWH: $5,100 / PWL: $4,720",
                "dailyLevel": f"Live: {formatted_price} (PDH: $4,870 / PDL: $4,760)",
                
                "entryAdvices": [
                    {
                        "timeframe": "15M (Scalp)", 
                        "buy": "$4,820 – $4,835", "tp": "$4,870", "sl": "$4,805",
                        "sell": "$4,890 – $4,910", "sellTP": "$4,840", "sellSL": "$4,925",
                        "colorHex": "green"
                    },
                    {
                        "timeframe": "4H (Intraday)", 
                        "buy": "$4,720 – $4,760", "tp": "$5,000", "sl": "$4,680",
                        "sell": "$5,050 – $5,120", "sellTP": "$4,870", "sellSL": "$5,180",
                        "colorHex": "orange"
                    },
                    {
                        "timeframe": "Daily (Swing)", 
                        "buy": "$4,530 – $4,650", "tp": "$5,400", "sl": "$4,450",
                        "sell": "$5,450 – $5,590", "sellTP": "$5,000", "sellSL": "$5,700",
                        "colorHex": "blue"
                    }
                ],
                "newsUpdates": [
                    {
                        "title": "US-Iran Diplomacy (Oman)", 
                        "impact": "BEARISH", 
                        "description": "High-level talks scheduled for Friday afternoon. Diplomatic progress could strip the 'Fear Premium'."
                    },
                    {
                        "title": "Nasdaq 'AI Capex' Rout", 
                        "impact": "BULLISH", 
                        "description": "Software stocks lost $1T this week. Forced deleveraging creating a safety bid for Gold."
                    }
                ],
                "fundamentalAnalysis": [
                    {
                        "title": "The 'Warsh' Correction vs. Dip Buyers",
                        "bodyText": f"Institutional accumulation noted at the {formatted_price} level. Singapore and Sydney demand remains robust."
                    }
                ]
            }
            print(f"Market Data Synced: {formatted_price}")
        except Exception as e:
            print(f"Sync Error: {e}")
        
        # Sleep for 60 seconds
        time.sleep(60)

# Start the background thread so it runs independent of the API calls
sync_thread = threading.Thread(target=update_gold_market_data, daemon=True)
sync_thread.start()

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    # Return the latest minute-by-minute data from the cache
    if not data_cache:
        return jsonify({"error": "Data warming up..."}), 503
    return jsonify(data_cache)

if __name__ == '__main__':
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
