from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    return jsonify({
        "monthlyLevel": "High: $5,608 / Low: $4,400",
        "weeklyLevel": "High: $5,200 / Low: $4,604",
        "dailyLevel": "High: $4,895 / Low: $4,405",
        
        "entryAdvices": [
            {
                "timeframe": "15M (Scalp)", 
                "buy": "$4,750 – $4,775", "tp": "$4,850", "sl": "$4,735",
                "sell": "$4,880 – $4,900", "sellTP": "$4,800", "sellSL": "$4,915",
                "colorHex": "green"
            }
        ],
        
        "newsUpdates": [
            {"title": "CME Margin Hikes", "impact": "BEARISH", "description": "Forced liquidations."}
        ],

        # --- THIS IS THE SECTION YOUR APP IS MISSING ---
        "coachAdvice": {
            "date": "Feb 03, 2026",
            "marketContext": "Absorption phase after January expansion.",
            "gamePlan": "Buy deep value dips near $4,750.",
            "riskLevel": "1.5% per trade"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
