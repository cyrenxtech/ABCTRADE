import os
import time
import threading
import yfinance as yf
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global cache to store live data
data_cache = {}

def update_gold_market_data():
    """Background task to fetch live gold prices every 60 seconds."""
    global data_cache
    while True:
        try:
            # Fetch Gold Futures (GC=F) - Better liquidity/updates than spot tickers on YF
            gold_ticker = yf.Ticker("GC=F") 
            hist = gold_ticker.history(period="1d", interval="1m")
            
            if not hist.empty:
                live_price = hist['Close'].iloc[-1]
                formatted_price = f"${live_price:,.2f}"

                # Update the global cache with your specific UI structure
                data_cache = {
                    "monthlyLevel": "PMH: $5,594 / PML: $4,400",
                    "weeklyLevel": "PWH: $5,100 / PWL: $4,720",
                    "dailyLevel": f"Live: {formatted_price} (PDH: $4,870 / PDL: $4,760)",
                    "entryAdvices": [
                        {
                            "timeframe": "15M (Scalp)", 
                            "buy": "$4,820 – $4,835", "tp": "$4,870", "sl": "$4,805",
                            "sell": "$4,890 – $4,910", "sellTP": "$4,840", "sellSL": "$4,925",
                            "colorHex": "green"
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
                            "title": "US-Iran De-escalation", 
                            "impact": "BEARISH", 
                            "description": "Washington signals conciliatory rhetoric. If talks succeed, Fear Bid could drop."
                        },
                        {
                            "title": "Central Bank Floor", 
                            "impact": "BULLISH", 
                            "description": "Institutional dip-buying confirmed near $4,400. Structural accumulation remains."
                        }
                    ],
                    "fundamentalAnalysis": [
                        {
                            "title": "The 'Warsh' Chair Effect",
                            "bodyText": "Nomination of Kevin Warsh as Fed Chair has recalibrated USD expectations."
                        },
                        {
                            "title": "Mean Reversion Phase",
                            "bodyText": f"Currently in a classic mean-reversion. Watch $4,700 as the primary magnet."
                        }
                    ]
                }
                print(f"✅ Market Data Synced: {formatted_price}")
            else:
                print("⚠️ Sync Warning: No price data returned from Yahoo.")

        except Exception as e:
            print(f"❌ Sync Error: {e}")
        
        # Interval for price updates (60 seconds)
        time.sleep(60)

# --- START BACKGROUND THREAD ---
# This must be outside the __main__ block for Render/Gunicorn to trigger it
sync_thread = threading.Thread(target=update_gold_market_data, daemon=True)
sync_thread.start()

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    # Return 503 if the thread hasn't finished the first fetch yet
    if not data_cache:
        return jsonify({"error": "Data warming up..."}), 503
    return jsonify(data_cache)

if __name__ == '__main__':
    # Used for local development only
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
