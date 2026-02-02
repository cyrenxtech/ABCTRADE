import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_levels():
    ticker = yf.Ticker("GC=F") # Gold Futures
    # Get Daily data for PDH/PDL
    d_hist = ticker.history(period="5d", interval="1d")
    # Get Weekly data for PWH/PWL
    w_hist = ticker.history(period="1mo", interval="1wk")
    
    # Yesterday's High/Low (Index -2 because -1 is the current live candle)
    pdh = d_hist['High'].iloc[-2]
    pdl = d_hist['Low'].iloc[-2]
    
    # Last Week's High/Low
    pwh = w_hist['High'].iloc[-2]
    pwl = w_hist['Low'].iloc[-2]
    
    return {
        "pdh": f"{pdh:.2f}", "pdl": f"{pdl:.2f}",
        "pwh": f"{pwh:.2f}", "pwl": f"{pwl:.2f}",
        "pmh": f"{pdh + 10:.2f}", "pml": f"{pdl - 10:.2f}" # Placeholder for Monthly
    }

@app.route('/analyze', methods=['POST'])
def analyze():
    levels = get_levels()
    # Basic logic: If price is above PDH, sentiment is Bullish
    sentiment = "BULLISH" if float(levels['pdh']) > 2000 else "BEARISH"
    
    return jsonify({
        "sentiment": sentiment,
        "educational_note": f"Gold is reacting to {levels['pdh']} (PDH). Watch for a sweep of {levels['pdl']}.",
        "buy_range": f"{float(levels['pdl'])-2:.1f} - {levels['pdl']}",
        "sell_range": f"{levels['pdh']} - {float(levels['pdh'])+2:.1f}",
        **levels
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
