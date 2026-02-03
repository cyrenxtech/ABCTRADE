from flask import Flask, jsonify
from flask_cors import CORS

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
                "timeframe": "15M (Scalping)", 
                "buy": "$4,750 – $4,775", "tp": "$4,850", "sl": "$4,735",
                "sell": "$4,880 – $4,900", "sellTP": "$4,800", "sellSL": "$4,915",
                "colorHex": "green"
            },
            {
                "timeframe": "4H (Intraday)", 
                "buy": "$4,604 – $4,680", "tp": "$5,050", "sl": "$4,580",
                "sell": "$5,150 – $5,200", "sellTP": "$4,950", "sellSL": "$5,230",
                "colorHex": "orange"
            },
            {
                "timeframe": "Daily (Swing)", 
                "buy": "$4,405 – $4,550", "tp": "$5,300", "sl": "$4,350",
                "sell": "$5,450 – $5,600", "sellTP": "$5,100", "sellSL": "$5,650",
                "colorHex": "blue"
            }
        ],
        "newsUpdates": [
            {"title": "Warsh Fed Nomination", "impact": "BEARISH", "description": "Trump's pick triggered a hawkish repricing."},
            {"title": "CME Margin Hikes", "impact": "BEARISH", "description": "Forced liquidations caused the crash."},
            {"title": "India Tariff Cut (18%)", "impact": "BULLISH", "description": "India cut import duties on gold/silver to 6%, supporting demand."},
            {"title": "US-Iran De-escalation", "impact": "NEUTRAL", "description": "Removing the Fear Premium as tensions cool."},
            {"title": "US Govt Shutdown", "impact": "BULLISH", "description": "Safety bid amid fiscal uncertainty and debt ceiling fears."}
        ]
    })

if __name__ == '__main__':
    # Render uses the PORT environment variable, but 5000 is fine for local dev
    app.run(host='0.0.0.0', port=5000)
