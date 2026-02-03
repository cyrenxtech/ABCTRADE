from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    return jsonify({
        "monthlyLevel": "$4,400 - $5,608",
        "weeklyLevel": "$4,604 - $5,200",
        "dailyLevel": "$4,405 - $4,895",
        
        "entryAdvices": [
            {
                "timeframe": "15M (Scalp)",
                "buy": "4,750 - 4,775", "tp": "4,850", "sl": "4,735",
                "sell": "4,880 - 4,900", "sellTP": "4,800", "sellSL": "4,915",
                "colorHex": "green"
            }
        ],
        
        "newsUpdates": [
            {
                "title": "Fed Interest Rate Decision",
                "impact": "BULLISH",
                "description": "Rates held steady; gold reacts positively to weakening dollar."
            }
        ],

        "coachAdvice": {
            "date": "Feb 3, 2026",
            "marketContext": "Price is currently in a 'Warsh Shock' expansion. Volume is building.",
            "gamePlan": "Look for 15M structure shift at the 4,750 POC. No trade without validation.",
            "riskLevel": "1% per trade"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
