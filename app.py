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

     # --- THIS IS THE SECTION YOUR APP IS MISSING ---
        "coachAdvice": {
            "date": "Feb 03, 2026",
            "marketContext": "Absorption phase after January expansion.",
            "gamePlan": "Buy deep value dips near $4,750.",
            "riskLevel": "1.5% per trade"
            
}
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
