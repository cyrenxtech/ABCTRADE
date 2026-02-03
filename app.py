import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Use your actual key here
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def get_level(ticker, period, interval, type='High'):
    hist = ticker.history(period=period, interval=interval, auto_adjust=True)
    if len(hist) < 2: return 0.0
    # iloc[-2] is the most recently CLOSED candle
    return float(hist[type].iloc[-2])

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        tf_code = data.get('timeframe', '15')
        tf_map = {"15": "15m", "240": "4h", "D": "1d"}
        interval = tf_map.get(tf_code, "15m")

        gold = yf.Ticker("GC=F") # Gold Futures
        
        # Calculate Levels
        pdh = get_level(gold, "5d", "1d", "High")
        pdl = get_level(gold, "5d", "1d", "Low")
        pwh = get_level(gold, "1mo", "1wk", "High")
        pwl = get_level(gold, "1mo", "1wk", "Low")
        pmh = get_level(gold, "6mo", "1mo", "High")
        pml = get_level(gold, "6mo", "1mo", "Low")

        # Trend Calculation for Coach
        current_candles = gold.history(period="1d", interval=interval)
        curr_price = float(current_candles['Close'].iloc[-1])
        # Simple SMA-style trend
        avg_price = (pdh + pdl) / 2
        trend = "BULLISH" if curr_price > avg_price else "BEARISH"
        
        note = f"Gold is {trend} on the {interval} chart. Price is holding {'above' if trend == 'BULLISH' else 'below'} the daily midpoint. "
        note += "Watch for liquidity sweeps near the " + ("PDH" if trend == "BULLISH" else "PDL") + "."

        return jsonify({
            "sentiment": trend,
            "educational_note": note,
            "buy_range": f"{pdl:.2f} - {min(pwl, pml):.2f}",
            "sell_range": f"{pdh:.2f} - {max(pwh, pmh):.2f}",
            "levels": {"pdh": pdh, "pdl": pdl, "pwh": pwh, "pwl": pwl, "pmh": pmh, "pml": pml}
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_coach():
    # ... (Same logic as before for OpenAI completions)
    return jsonify({"answer": "AI Coach logic connected."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
