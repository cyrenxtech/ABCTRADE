from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/newsletter', methods=['GET'])
def get_data():
    return jsonify({
        "monthlyLevel": "High: $5,608 / Low: $4,400",
        "weeklyLevel": "High: $5,200 / Low: $4,604",
        "dailyLevel": "High: $4,895 / Low: $4,405",
        "entryAdvices": [
            {"timeframe": "15M (Scalping)", "buy": "$4,750", "tp": "$4,850", "sl": "$4,735", "colorHex": "green"},
            {"timeframe": "4H (Intraday)", "buy": "$4,604", "tp": "$5,050", "sl": "$4,580", "colorHex": "orange"},
            {"timeframe": "Daily (Swing)", "buy": "$4,405", "tp": "$5,300", "sl": "$4,350", "colorHex": "blue"}
        ],
        "newsUpdates": [
            {"title": "Warsh Fed Nomination", "impact": "BEARISH", "description": "Hawkish repricing boosting USD."},
            {"title": "India Tariff Cut", "impact": "BULLISH", "description": "Supports physical gold demand."}
        ]
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
