from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import yfinance as yf

app = Flask(__name__)
CORS(app)

# Global variable to store the latest data
cached_data = {}

def fetch_market_data():
    """Function to update gold data every minute."""
    global cached_data
    while True:
        try:
            # 1. Fetch Real-time Gold Price (GC=F is Gold Futures, XAUUSD=X is Spot)
            gold = yf.Ticker("GC=F")
            current_price = gold.history(period="1d")['Close'].iloc[-1]
            formatted_price = f"${current_price:,.2f}"

            # 2. Prepare the payload (Using your February 6, 2026 context)
            cached_data = {
                "monthlyLevel": f"PWH: $5,594 / Current: {formatted_price}",
                "weeklyLevel": "PWH: $5,100 / PWL: $4,720",
                "dailyLevel": f"Live Spot: {formatted_price}",
                
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
                    }
                ],
                
                "newsUpdates": [
                    {
                        "title": "US-Iran Diplomacy (Oman)", 
                        "impact": "BEARISH", 
                        "description": "High-level talks scheduled for Friday. Diplomatic progress could strip 'Fear Premium'."
                    },
                    {
                        "title": "Nasdaq 'AI Capex' Rout", 
                        "impact": "BULLISH", 
                        "description": "Software stocks lost $1T this week, creating a safety bid for Gold."
                    }
                ],
                
                "fundamentalAnalysis": [
                    {
                        "title": "Equity Correlation Shift",
                        "bodyText": "Traditional inverse correlation is back. Gold reclaiming role as the ultimate hedge."
                    }
                ]
            }
            print(f"Data updated successfully at {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"Update failed: {e}")
        
        # Wait 60 seconds before next update
        time.sleep(60)

# Start the background thread
update_thread = threading.Thread(target=fetch_market_data, daemon=True)
update_thread.start()

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    # Return the latest cached data
    return jsonify(cached_data if cached_data else {"status": "Loading data..."})

if __name__ == '__main__':
    # Use environment variable for Port (Required by Render)
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
