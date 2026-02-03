import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Fetch Gold Futures
        gold = yf.Ticker("GC=F")
        # auto_adjust=True is critical for clean High/Low data
        df_d = gold.history(period="5d", interval="1d", auto_adjust=True)
        df_w = gold.history(period="1mo", interval="1wk", auto_adjust=True)
        df_m = gold.history(period="6mo", interval="1mo", auto_adjust=True)

        # Extraction with safety fallbacks
        levels = {
            "pdh": float(df_d['High'].iloc[-2]),
            "pdl": float(df_d['Low'].iloc[-2]),
            "pwh": float(df_w['High'].iloc[-2]),
            "pwl": float(df_w['Low'].iloc[-2]),
            "pmh": float(df_m['High'].iloc[-2]),
            "pml": float(df_m['Low'].iloc[-2])
        }

        return jsonify({
            "educational_note": "Trend analysis active. Levels synced.",
            "buy_range": f"{levels['pdl']:.2f} - {levels['pwl']:.2f}",
            "sell_range": f"{levels['pdh']:.2f} - {levels['pwh']:.2f}",
            "levels": levels
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Data fetch failed"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
