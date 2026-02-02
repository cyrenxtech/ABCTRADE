import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_liquidity_data():
    ticker = yf.Ticker("GC=F") # Gold Futures
    
    # Fetch different periods
    d_data = ticker.history(period="5d", interval="1d")
    w_data = ticker.history(period="1mo", interval="1wk")
    m_data = ticker.history(period="6mo", interval="1mo")

    # Extract Highs and Lows (using .iloc[-2] for the most recent completed period)
    pdh, pdl = d_data['High'].iloc[-2], d_data['Low'].iloc[-2]
    pwh, pwl = w_data['High'].iloc[-2], w_data['Low'].iloc[-2]
    pmh, pml = m_data['High'].iloc[-2], m_data['Low'].iloc[-2]

    # Strategy: Buy Zone is the range between the lowest lows
    # Sell Zone is the range between the highest highs
    buy_low = min(pdl, pwl, pml)
    buy_high = max(pdl, pwl, pml)
    
    sell_low = min(pdh, pwh, pmh)
    sell_high = max(pdh, pwh, pmh)

    return {
        "pdh": round(pdh, 2), "pdl": round(pdl, 2),
        "pwh": round(pwh, 2), "pwl": round(pwl, 2),
        "pmh": round(pmh, 2), "pml": round(pml, 2),
        "buy_range": f"{buy_low:.2f} - {buy_high:.2f}",
        "sell_range": f"{sell_low:.2f} - {sell_high:.2f}"
    }

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = get_liquidity_data()
        return jsonify({
            "sentiment": "NEUTRAL",
            "educational_note": f"Liquidity focused. PDH at {data['pdh']}, PML at {data['pml']}.",
            "buy_range": data['buy_range'],
            "sell_range": data['sell_range'],
            "levels": data # Passing all raw levels for the chart
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
