import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        tf_code = data.get('timeframe', '15')
        tf_map = {"15": "15m", "240": "4h", "D": "1d"}
        interval = tf_map.get(tf_code, "15m")

        gold = yf.Ticker("GC=F")
        hist = gold.history(period="5d", interval=interval, auto_adjust=True)
        hist_d = gold.history(period="5d", interval="1d", auto_adjust=True)
        hist_w = gold.history(period="1mo", interval="1wk", auto_adjust=True)
        hist_m = gold.history(period="6mo", interval="1mo", auto_adjust=True)

        # 1. Supply/Demand Calculation (Recent Price Action)
        last_3 = hist.tail(3)
        supply_top = float(last_3['High'].max())
        supply_bottom = float(last_3['Open'].min()) if hist['Close'].iloc[-1] < hist['Open'].iloc[-1] else float(last_3['Low'].max())
        
        demand_bottom = float(last_3['Low'].min())
        demand_top = float(last_3['Open'].max()) if hist['Close'].iloc[-1] > hist['Open'].iloc[-1] else float(last_3['High'].min())

        # 2. Historical Levels
        levels = {
            "pdh": float(hist_d['High'].iloc[-2]), "pdl": float(hist_d['Low'].iloc[-2]),
            "pwh": float(hist_w['High'].iloc[-2]), "pwl": float(hist_w['Low'].iloc[-2]),
            "pmh": float(hist_m['High'].iloc[-2]), "pml": float(hist_m['Low'].iloc[-2])
        }

        # 3. Trend Logic
        curr_price = float(hist['Close'].iloc[-1])
        trend = "BULLISH" if curr_price > levels['pdl'] else "BEARISH"
        note = f"Gold is {trend} on {interval}. Supply zone sits at {supply_top:.2f}, while Demand is firm at {demand_bottom:.2f}."

        return jsonify({
            "sentiment": trend,
            "educational_note": note,
            "buy_range": f"{demand_bottom:.2f} - {demand_top:.2f}",
            "sell_range": f"{supply_bottom:.2f} - {supply_top:.2f}",
            "levels": levels
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
