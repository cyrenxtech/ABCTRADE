from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    return jsonify({
        # KEPT EXACT: Key levels remain as per your request
        "monthlyLevel": "PMH: $5,594 / PML: $4,400",
        "weeklyLevel": "PWH: $5,100 / PWL: $4,720",
        "dailyLevel": "PDH: $4,870 / PDL: $4,760",
        
        # KEPT EXACT: Technical setups
        "entryAdvices": [
            {
                "timeframe": "15M (Scalp)", 
                "buy": "$4,820 – $4,835", "tp": "$4,870", "sl": "$4,805",
                "sell": "$4,890 – $4,910", "sellTP": "$4,840", "sellSL": "$4,925",
                "colorHex": "green"
            },
            {
                "timeframe": "Daily (Swing)", 
                "buy": "$4,530 – $4,650", "tp": "$5,400", "sl": "$4,450",
                "sell": "$5,450 – $5,590", "sellTP": "$5,000", "sellSL": "$5,700",
                "colorHex": "blue"
            }
        ],
        
        # UPDATED: Live News for February 6, 2026
        "newsUpdates": [
            {
                "title": "US-Iran De-escalation Talk", 
                "impact": "BEARISH", 
                "description": "Risk premium is unwinding as Washington signals conciliatory rhetoric. If talks in Oman succeed, 'Fear Bid' could drop Gold to $4,700."
            },
            {
                "title": "CME Margin Hikes (8.8%)", 
                "impact": "NEUTRAL", 
                "description": "CME raised Gold margins to nearly 9% following the record 1,000-point drop. Expect lower liquidity and choppy consolidation."
            },
            {
                "title": "Central Bank Floor", 
                "impact": "BULLISH", 
                "description": "Institutional dip-buying confirmed near $4,400. While short-term trend is bearish, structural accumulation remains intact."
            }
        ],
        
        # UPDATED: Macro Fundamentals
        "fundamentalAnalysis": [
            {
                "title": "The 'Warsh' Chair Effect",
                "bodyText": "The nomination of Kevin Warsh as Fed Chair has recalibrated USD expectations. The 'Higher for Longer' narrative is putting heavy pressure on zero-yield assets."
            },
            {
                "title": "Mean Reversion Phase",
                "bodyText": "After the parabolic run to $5,600, we are in a classic February mean-reversion. Watch the 0.272 Fibonacci level at $4,700 as the primary magnet."
            }
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
