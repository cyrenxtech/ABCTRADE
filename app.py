import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    tf_code = data.get('timeframe', '15')
    tf_map = {"15": "15m", "240": "4h", "D": "1d"}
    interval = tf_map.get(tf_code, "15m")

    gold = yf.Ticker("GC=F")
    # Fetch extra history for trend calculation (SMA 20)
    hist_trend = gold.history(period="5d", interval=interval)
    hist_d = gold.history(period="5d", interval="1d")
    hist_w = gold.history(period="1mo", interval="1wk")
    hist_m = gold.history(period="6mo", interval="1mo")
    current_candles = gold.history(period="1d", interval=interval)
    
    # 1. Previous Levels
    pdh, pdl = float(hist_d['High'].iloc[-2]), float(hist_d['Low'].iloc[-2])
    pwh, pwl = float(hist_w['High'].iloc[-2]), float(hist_w['Low'].iloc[-2])
    pmh, pml = float(hist_m['High'].iloc[-2]), float(hist_m['Low'].iloc[-2])

    # 2. Trend Logic (2-3 sentences)
    current_price = float(current_candles['Close'].iloc[-1])
    sma_20 = float(hist_trend['Close'].rolling(window=20).mean().iloc[-1])
    
    trend = "BULLISH" if current_price > sma_20 else "BEARISH"
    trend_desc = f"The chart is currently showing a {trend} trend as price holds {'above' if trend == 'BULLISH' else 'below'} the short-term average. "
    trend_desc += f"Watch for liquidity grabs at the {'PDH' if trend == 'BULLISH' else 'PDL'} before the next major move."

    # 3. Dynamic Zone Calculation
    curr_low, curr_high = float(current_candles['Low'].min()), float(current_candles['High'].max())
    buy_floor = min(pdl, pwl, pml)
    buy_range = f"{min(curr_low, buy_floor):.2f} - {max(curr_low, buy_floor):.2f}"
    sell_ceiling = max(pdh, pwh, pmh)
    sell_range = f"{min(curr_high, sell_ceiling):.2f} - {max(curr_high, sell_ceiling):.2f}"

    return jsonify({
        "sentiment": trend,
        "educational_note": trend_desc, # This goes to your AI Coach section
        "buy_range": buy_range,
        "sell_range": sell_range,
        "levels": {
            "pdh": pdh, "pdl": pdl, "pwh": pwh, "pwl": pwl, "pmh": pmh, "pml": pml
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
