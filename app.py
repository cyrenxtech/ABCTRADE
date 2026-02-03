from flask import Flask, jsonify
from flask_cors import CORS # You must run 'pip install flask-cors'

app = Flask(__name__)
# Enable CORS so your SwiftUI app/simulator can fetch the data
CORS(app)

@app.route('/newsletter', methods=['GET'])
def get_gold_update():
    # DATA MATCHES FEB 3, 2026 MARKET CONTEXT
    data = {
        "status": "success",
        "market_date": "Feb 3, 2026",
        "liquidity_levels": {
            "monthly": "High: $5,608 / Low: $4,400",
            "weekly": "High: $5,200 / Low: $4,604",
            "daily": "High: $4,895 / Low: $4,405"
        },
        "entry_advices": [
            {
                "timeframe": "15M (Scalping)",
                "buy_zone": "$4,750 – $4,775",
                "tp": "$4,850",
                "sl": "$4,735",
                "color": "green"
            },
            {
                "timeframe": "4H (Intraday)",
                "buy_zone": "$4,604 – $4,680",
                "tp": "$5,050",
                "sl": "$4,580",
                "color": "orange"
            },
            {
                "timeframe": "Daily (Swing)",
                "buy_zone": "$4,405 – $4,550",
                "tp": "$5,300",
                "sl": "$4,350",
                "color": "blue"
            }
        ],
        "coach_d_advise": [
            {
                "step": "1. Define the Range (CRT)",
                "content": "H4/Daily: We are in a 'Warsh Shock' expansion. Range High: $5,608 | Range Low: $4,400."
            },
            {
                "step": "2. Volume Profile (FRVP)",
                "content": "POC is sitting heavy near $4,850. Below POC = Discount (Look for Buys near $4,650)."
            },
            {
                "step": "3. Fibonacci Confluence",
                "content": "Focus on 61.8% ($4,576). We are currently testing the 61.8% floor. Watch for rejection."
            }
        ],
        "major_news": [
            {
                "title": "Warsh Fed Nomination",
                "impact": "BEARISH",
                "desc": "Trump's pick of Kevin Warsh as Fed Chair triggered hawkish repricing. Gold pressured by USD strength."
            },
            {
                "title": "CME Margin Hikes",
                "impact": "BEARISH",
                "desc": "CME raised margins for Gold futures. Forced liquidation caused the recent 9% flash crash."
            },
            {
                "title": "India Tariff Cut (18%)",
                "impact": "BULLISH",
                "desc": "Trade deal with India supports physical demand in the world's #2 gold consumer."
            },
            {
                "title": "US-Iran De-escalation",
                "impact": "NEUTRAL",
                "desc": "Geopolitical 'Fear Premium' is fading as officials meet to discuss security buffers."
            },
            {
                "title": "US Govt Shutdown",
                "impact": "BULLISH",
                "desc": "NFP delayed. Market uncertainty usually favors Gold as a safe-haven hedge."
            }
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    # Run on port 5000. Access via http://192.168.0.73/newsletter
    app.run(host='0.0.0.0', port=5000, debug=True)
