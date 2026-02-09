from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import requests
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
GOLD_API_KEY = "goldapi-5w1smlcmmepr-io"
NEWS_API_KEY = "bd41341b1983401699fa6c69be2c6e65"

def init_db():
    with sqlite3.connect('journal.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS journal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT, buy_price REAL, sell_price REAL, tp_price REAL, sl_price REAL, result TEXT
            )
        ''')

init_db()

def fetch_market_data():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": GOLD_API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            curr = data.get('price', 2000.0)
            prev = data.get('prev_close_price', curr)
            trend = "BULLISH" if curr >= prev else "BEARISH"
            return float(curr), trend
    except:
        return 2000.0, "NEUTRAL"

def fetch_live_news(trend_status):
    url = f"https://newsapi.org/v2/everything?q=gold+market+XAUUSD&language=en&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
    try:
        res = requests.get(url, timeout=5).json()
        return [{
            "title": art['title'][:60],
            "impact": trend_status,
            "description": art['description'][:100] if art['description'] else "N/A"
        } for art in res.get('articles', [])]
    except:
        return []

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    price, trend = fetch_market_data()
    # ALL KEYS BELOW MATCH YOUR SWIFT CodingKeys
    return jsonify({
        "price": price,
        "monthlyLevel": f"PMH: ${round(price + 100)} / PML: ${round(price - 100)}",
        "weeklyLevel": f"PWH: ${round(price + 45)} / PWL: ${round(price - 45)}",
        "dailyLevel": f"PDH: ${round(price + 15)} / PDL: ${round(price - 15)}",
        "entryAdvices": [
            {"timeframe": "15M", "buy": str(round(price-3)), "tp": str(round(price+6)), "sl": str(round(price-7)), "colorHex": "green", "sell": None, "sellTP": None, "sellSL": None},
            {"timeframe": "4H", "buy": str(round(price-20)), "tp": str(round(price+50)), "sl": str(round(price-40)), "colorHex": "orange", "sell": None, "sellTP": None, "sellSL": None}
        ],
        "newsUpdates": fetch_live_news(trend),
        "fundamentalAnalysis": [{"title": "Market Sentiment", "bodyText": f"Currently {trend}"}],
        "activeAlert": None
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
