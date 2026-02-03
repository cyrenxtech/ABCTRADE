from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('', methods=['GET'])
def get_gold_data():
    return jsonify({
        "monthlyLevel": "High: $5,608 / Low: $4,400",
        "weeklyLevel": "High: $5,200 / Low: $4,604",
        "dailyLevel": "High: $4,895 / Low: $4,405",
        "entryAdvices": [
            {"timeframe": "15M (Scalping)", "buy": "$4,750 – $4,775", "tp": "$4,850", "sl": "$4,735", "colorName": "green"},
            {"timeframe": "4H (Intraday)", "buy": "$4,604 – $4,680", "tp": "$5,050", "sl": "$4,580", "colorName": "orange"},
            {"timeframe": "Daily (Swing)", "buy": "$4,405 – $4,550", "tp": "$5,300", "sl": "$4,350", "colorName": "blue"}
        ],
        "newsUpdates": [
            {"title": "Warsh Fed Nomination", "impact": "BEARISH", "description": "Trump's pick triggered a hawkish repricing."},
            {"title": "CME Margin Hikes", "impact": "BEARISH", "description": "Forced liquidations caused the crash."},
            {"title": "India Tariff Cut (18%)", "impact": "BULLISH", "description": "Supports physical gold demand."},
            {"title": "US-Iran De-escalation", "impact": "NEUTRAL", "description": "Removing the Fear Premium."},
            {"title": "US Govt Shutdown", "impact": "BULLISH", "description": "Data darkness favors Gold safety."}
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
