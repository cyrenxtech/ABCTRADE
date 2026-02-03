from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# IMPORTANT: CORS allows your SwiftUI app to access this API
CORS(app)

@app.route('/newsletter', methods=['GET'])
def get_newsletter():
    # This dictionary must match the "Codable" structs in Swift
    data = {
        "headline": "THE GANN 144-BAR CYCLE RELIEF",
        "market_date": "Feb 3, 2026",
        "levels": {
            "monthly": "High: $5,608 / Low: $4,400",
            "weekly": "High: $5,200 / Low: $4,604",
            "daily": "High: $4,895 / Low: $4,405"
        },
        "advices": [
            {"tf": "15M (Scalping)", "buy": "$4,750-4,775", "tp": "$4,850", "sl": "$4,735", "hex": "#00FF00"},
            {"tf": "4H (Intraday)", "buy": "$4,604-4,680", "tp": "$5,050", "sl": "$4,580", "hex": "#FFA500"},
            {"tf": "Daily (Swing)", "buy": "$4,405-4,550", "tp": "$5,300", "sl": "$4,350", "hex": "#0000FF"}
        ],
        "news": [
            {"title": "Warsh Fed Nomination", "impact": "BEARISH", "desc": "Trump's pick triggered a hawkish pivot."},
            {"title": "CME Margin Hikes", "impact": "BEARISH", "desc": "Forced liquidations caused the flash crash."},
            {"title": "India Tariff Cut (18%)", "impact": "BULLISH", "desc": "PM Modi agreed to halt Russian oil imports."},
            {"title": "US-Iran De-escalation", "impact": "NEUTRAL", "desc": "Easing risk removes 'Fear Premium'."},
            {"title": "US Govt Shutdown", "impact": "BULLISH", "desc": "Fiscal uncertainty usually favors Gold."}
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    # Render requires binding to 0.0.0.0
    app.run(host='0.0.0.0', port=5000)
