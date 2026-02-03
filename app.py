from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Crucial for SwiftUI to connect

@app.route('/newsletter', methods=['GET'])
def get_newsletter():
    return jsonify({
        "headline": "THE GANN 144-BAR CYCLE RELIEF",
        "market_date": "Feb 3, 2026",
        # MH/ML, WH/WL, DH/DL Restored
        "levels": {
            "monthly": "High: $5,608 / Low: $4,400",
            "weekly": "High: $5,200 / Low: $4,604",
            "daily": "High: $4,895 / Low: $4,405"
        },
        "advices": [
            {"tf": "15M (Scalping)", "buy": "4,750-4,775", "tp": "4,850", "sl": "4,735", "hex": "#00FF00"},
            {"tf": "4H (Intraday)", "buy": "4,604-4,680", "tp": "5,050", "sl": "4,580", "hex": "#FFA500"},
            {"tf": "Daily (Swing)", "buy": "4,405-4,550", "tp": "5,300", "sl": "4,350", "hex": "#0000FF"}
        ],
        "news": [
            {"title": "Warsh Fed Nomination", "impact": "BEARISH", "desc": "Hawkish pivot boosting USD."},
            {"title": "CME Margin Hikes", "impact": "BEARISH", "desc": "Forced liquidations caused flash crash."},
            {"title": "India Tariff Cut (18%)", "impact": "BULLISH", "desc": "Physical demand support."},
            {"title": "US-Iran De-escalation", "impact": "NEUTRAL", "desc": "Fear premium fading."},
            {"title": "US Govt Shutdown", "impact": "BULLISH", "desc": "Safety hedge amid fiscal delay."}
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
