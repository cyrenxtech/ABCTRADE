from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/newsletter', methods=['GET'])
def get_newsletter():
    data = {
        "monthlyLevel": "2750.50",
        "weeklyLevel": "2715.00",
        "dailyLevel": "2695.20",
        "entryAdvices": [
            {
                "timeframe": "15M",
                "buy": "2685.00",
                "tp": "2705.00",
                "sl": "2678.00",
                "sell": "2720.00",
                "sellTP": "2700.00",
                "sellSL": "2730.00",
                "colorHex": "green"
            }
        ],
        "newsUpdates": [
            {
                "title": "NFP Report",
                "impact": "HIGH",
                "description": "Expect high volatility at 8:30 AM EST."
            }
        ],
        # --- COACH D DYNAMIC DATA ---
        "coachDate": "03/02/26",
        "coachContext": "January expanded, February absorbing",
        "coachMarketCondition": "range trading",
        "coachBullTrigger": "2,740",
        "coachBearTrigger": "2,660",
        "coachBehavior": "Heavy sweeping of liquidity below Asia lows",
        "coachPositioning": "Bullish Trend",
        "coachHowToTreat": "Buy the deep retracements"
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
