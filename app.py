from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    # Simulation of real-time 2026 market analysis
    # Context: Recovery from the Jan 30th "Warsh Shock"
    
    return jsonify({
        "monthlyLevel": "PWH: $5,594 / PWL: $4,400",
        "weeklyLevel": "Supply: $5,115 / Demand: $4,625",
        "dailyLevel": "Pivot: $4,955 / Support: $4,805",
        
        "entryAdvices": [
            {
                "timeframe": "15M (Scalp)", 
                "buy": "$4,905 – $4,920", "tp": "$4,955", "sl": "$4,890",
                "sell": "$4,980 – $5,005", "sellTP": "$4,925", "sellSL": "$5,030",
                "colorHex": "green"
            },
            {
                "timeframe": "4H (Intraday)", 
                "buy": "$4,805 – $4,850", "tp": "$5,115", "sl": "$4,745",
                "sell": "$5,150 – $5,220", "sellTP": "$4,955", "sellSL": "$5,280",
                "colorHex": "orange"
            },
            {
                "timeframe": "Daily (Swing)", 
                "buy": "$4,625 – $4,700", "tp": "$5,400", "sl": "$4,550",
                "sell": "$5,500 – $5,590", "sellTP": "$5,100", "sellSL": "$5,680",
                "colorHex": "blue"
            }
        ],
        
        "newsUpdates": [
            {
                "title": "US Jobless Claims / JOLTS", 
                "impact": "BULLISH", # Icon triggered by 'BULLISH' string in iOS
                "description": "Softening labor market data (ADP +22k) counters hawkish Fed rhetoric, providing a floor for XAUUSD at $4,900."
            },
            {
                "title": "Kevin Warsh Confirmation Hearing", 
                "impact": "BEARISH", 
                "description": "Senate testimony hints at aggressive balance sheet reduction; DXY hits 2-week high, capping Gold's recovery."
            },
            {
                "title": "Nasdaq AI 'Deleveraging' Stampede", 
                "impact": "NEUTRAL", 
                "description": "US Equities (Nasdaq -1.2%) under pressure from AI capex concerns. Gold seeing mild safe-haven flow but limited by USD strength."
            },
            {
                "title": "Chinese Lunar New Year Liquidity", 
                "impact": "NEUTRAL", 
                "description": "Approaching Feb 16 holiday. Expect 'thin' market volatility. Institutional accumulation noted at $4,850."
            },
            {
                "title": "US-Iran Diplomacy (Myfxbook)", 
                "impact": "BEARISH", 
                "description": "Planned talks for Friday afternoon reducing geopolitical risk premium; initial target for Gold $4,885."
            }
        ],
        
        # Additional hourly trending logic for EducationalDashboardView
        "fundamentalAnalysis": [
            {
                "title": "1. Gold vs. US Equities",
                "bodyText": "An inverse correlation has intensified. As the 'AI Capex Hangover' slams software stocks (lose $1T in value), Gold is fighting to reclaim its safe-haven status against a surging Dollar."
            },
            {
                "title": "2. Hourly Trend (XAUUSD)",
                "bodyText": "Price is currently consolidating above the $4,955 Wolfe Wave breakout point. Bulls need a 4H candle close above $5,005 to target $5,115."
            }
        ]
    })

if __name__ == '__main__':
    # Using 5000 for local development
    app.run(host='0.0.0.0', port=5000, debug=True)
