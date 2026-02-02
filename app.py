import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Fetch Gold Data
    gold = yf.Ticker("GC=F")
    d_h = gold.history(period="5d", interval="1d")
    w_h = gold.history(period="1mo", interval="1wk")
    m_h = gold.history(period="6mo", interval="1mo")

    # Extract 6 core levels
    pdh, pdl = d_h['High'].iloc[-2], d_h['Low'].iloc[-2]
    pwh, pwl = w_h['High'].iloc[-2], w_h['Low'].iloc[-2]
    pmh, pml = m_h['High'].iloc[-2], m_h['Low'].iloc[-2]

    # Buy Zone Calculation (Difference between major liquidity lows)
    buy_zone = f"{min(pdl, pwl, pml):.2f} - {max(pdl, pwl, pml):.2f}"
    sell_zone = f"{min(pdh, pwh, pmh):.2f} - {max(pdh, pwh, pmh):.2f}"

    return jsonify({
        "sentiment": "BULLISH" if d_h['Close'].iloc[-1] > pdh else "BEARISH",
        "educational_note": f"Market showing liquidity grab near {pwl:.2f}. Trend is currently respecting the daily bullish order block.",
        "buy_range": buy_zone,
        "sell_range": sell_zone,
        "levels": {
            "pdh": pdh, "pdl": pdl,
            "pwh": pwh, "pwl": pwl,
            "pmh": pmh, "pml": pml
        }
    })
