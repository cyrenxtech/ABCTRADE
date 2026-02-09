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

def get_time_ago(iso_date_str):
    try:
        pub_time = datetime.fromisoformat(iso_date_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        diff = now - pub_time
        minutes = int(diff.total_seconds() / 60)
        if minutes < 60: return f"{minutes}m ago"
        hours = int(minutes / 60)
        if hours < 24: return f"{hours}h ago"
        return pub_time.strftime("%b %d")
    except: return "Recent"

def fetch_market_data():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": GOLD_API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            curr = data.get('price', 2000.0) # Using 2000 as a safer fallback than 4966
            prev = data.get('prev_close_price', curr)
            trend_icon = "BULLISH" if curr >= prev else "BEARISH"
            change_pct = ((curr - prev) / prev) * 100
            return float(curr), trend_icon, round(change_pct, 2)
    except: pass
    return 2000.0, "NEUTRAL", 0.0

def fetch_live_news(trend_status):
    url = f"https://newsapi.org/v2/everything?q=gold+market+XAUUSD&language=en&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return [
                {
                    "title": art['title'][:60] + "...",
                    "impact": trend_status,
                    "description": art['description'][:100] + "..." if art['description'] else "No description available."
                } for art in articles
            ]
    except: pass
    return []

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    price, trend, change = fetch_market_data()
    return jsonify({
        "price": price,
        "monthlyLevel": f"H: ${round(price + 100)} / L: ${round(price - 100)}",
        "weeklyLevel": f"H: ${round(price + 40)} / L: ${round(price - 40)}",
        "dailyLevel": f"H: ${round(price + 15)} / L: ${round(price - 15)}",
        "entryAdvices": [
            {"timeframe": "15M", "buy": str(round(price-2)), "tp": str(round(price+5)), "sl": str(round(price-6)), "colorHex": "green"},
            {"timeframe": "4H", "buy": str(round(price-15)), "tp": str(round(price+30)), "sl": str(round(price-25)), "colorHex": "orange"},
            {"timeframe": "1D", "buy": str(round(price-50)), "tp": str(round(price+120)), "sl": str(round(price-80)), "colorHex": "blue"}
        ],
        "newsUpdates": fetch_live_news(trend),
        "fundamentalAnalysis": [{"title": "Sentiment", "bodyText": f"Market is {trend} at {change}% change."}],
        "activeAlert": None 
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
