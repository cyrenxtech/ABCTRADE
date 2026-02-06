from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    # February 6, 2026: Live Market Context
    # Gold recovered to $4,850 after a massive 13% weekly correction.
    # US-Iran diplomacy scheduled for today is the primary "Fear Premium" driver.
    
    return jsonify({
        "monthlyLevel": "PMH: $5,594 / PML: $4,400",
        "weeklyLevel": "PWH: $5,100 / PWL: $4,720",
        "dailyLevel": "PDH: $4,870 / PDL: $4,760",
        
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
                "title": "US-Iran Diplomacy (Oman)", 
                "impact": "BEARISH", 
                "description": "High-level talks scheduled for Friday afternoon. Diplomatic progress could strip the 'Fear Premium' and push XAUUSD toward $4,750."
            },
            {
                "title": "Nasdaq 'AI Capex' Rout", 
                "impact": "BULLISH", 
                "description": "Software stocks lost $1T this week. Forced deleveraging in tech is creating a safety bid for Gold as investors exit risk assets."
            },
            {
                "title": "US Michigan Consumer Sentiment", 
                "impact": "NEUTRAL", 
                "description": "Data due at 10:00 AM. Markets watching for inflation expectations (Prev: 4.0%). High readings will boost USD, capping Gold."
            }
        ],
        
        "fundamentalAnalysis": [
            {
                "title": "The 'Warsh' Correction vs. Dip Buyers",
                "bodyText": "While the Warsh nomination triggered a hawkish USD rally, physical demand in Singapore and Sydney remains robust. Institutional accumulation is noted at the $4,850 psychological level."
            },
            {
                "title": "Equity Correlation Shift",
                "bodyText": "The traditional inverse correlation is back. As the Nasdaq pulls back from 26k, Gold is reclaiming its role as the ultimate safe-haven hedge."
            }
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
