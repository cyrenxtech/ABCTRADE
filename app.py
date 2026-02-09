import sqlite3
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app) # Allows your SwiftUI app to connect without security blocks

# --- CONFIGURATION ---
GOLD_API_KEY = "goldapi-5w1smlcmmepr-io"
NEWS_API_KEY = "bd41341b1983401699fa6c69be2c6e65"

# --- DATABASE INIT ---
def init_db():
    conn = sqlite3.connect('journal.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS journal 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, 
                     buy_price TEXT, sell_price TEXT, tp_price TEXT, 
                     sl_price TEXT, result TEXT)''')
    conn.close()

init_db()

# --- HELPER FUNCTIONS ---

def get_time_ago(iso_date_str):
    """Parses ISO dates from NewsAPI into '5m ago' style strings."""
    try:
        clean_date = iso_date_str.replace('Z', '+00:00')
        pub_time = datetime.fromisoformat(clean_date)
        now = datetime.now(timezone.utc)
        diff = now - pub_time
        minutes = int(diff.total_seconds() / 60)
        if minutes < 60: return f"{max(0, minutes)}m ago"
        hours = int(minutes / 60)
        if hours < 24: return f"{hours}h ago"
        return pub_time.strftime("%b %d")
    except: return "Just now"

def fetch_market_data():
    """Fetches real-time Gold price from GoldAPI.io."""
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": GOLD_API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            curr = float(data.get('price', 5069.52))
            prev = float(data.get('prev_close_price', curr))
            
            trend_icon = "▲" if curr >= prev else "▼"
            change_pct = round(((curr - prev) / prev) * 100, 2)
            return curr, trend_icon, change_pct
    except Exception as e:
        print(f"API Error: {e}")
    
    # Fallback if API fails
    return 5069.52, "—", 0.0

def fetch_live_news(trend_icon):
    """Fetches live market news from NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q=gold+price+XAUUSD&language=en&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return [
                {
                    "id": i,
                    "title": f"{trend_icon} {art['title'][:70]}...",
                    "impact": f"LATEST ({get_time_ago(art['publishedAt'])})",
                    "description": art['description'][:100] + "..." if art['description'] else ""
                } for i, art in enumerate(articles)
            ]
    except: pass
    return [{"id": 0, "title": "News feed temporarily unavailable", "impact": "N/A", "description": "Please check back later."}]

# --- ROUTES ---

@app.route('/newsletter', methods=['GET'])
def get_newsletter():
    current_price, trend_icon, change_pct = fetch_market_data()
    live_news = fetch_live_news(trend_icon)

    return jsonify({
        "price": current_price,
        "lastUpdate": datetime.now().strftime("%I:%M %p"),
        "marketTrend": f"{trend_icon} {change_pct}%",
        "monthlyLevel": f"PMH: ${round(current_price * 1.05)} / PML: ${round(current_price * 0.95)}",
        "weeklyLevel": f"PWH: ${round(current_price + 45)} / PWL: ${round(current_price - 45)}",
        "dailyLevel": f"PDH: ${round(current_price + 15)} / PDL: ${round(current_price - 15)}",
        
        "entryAdvices": [
            {
                "timeframe": "15M (Scalp)", 
                "buy": f"${round(current_price - 8)}", "tp": f"${round(current_price + 12)}", "sl": f"${round(current_price - 15)}",
                "sell": f"${round(current_price + 10)}", "sellTP": f"${round(current_price - 8)}", "sellSL": f"${round(current_price + 25)}",
                "colorHex": "green"
            },
            {
                "timeframe": "4H (Intraday)", 
                "buy": f"${round(current_price - 40)}", "tp": f"${round(current_price + 80)}", "sl": f"${round(current_price - 60)}",
                "sell": f"${round(current_price + 60)}", "sellTP": f"${round(current_price - 40)}", "sellSL": f"${round(current_price + 130)}",
                "colorHex": "orange"
            },
            {
                "timeframe": "1Day (Swing)", 
                "buy": f"${round(current_price - 150)}", "tp": f"${round(current_price + 300)}", "sl": f"${round(current_price - 200)}",
                "sell": f"${round(current_price + 250)}", "sellTP": f"${round(current_price - 200)}", "sellSL": f"${round(current_price + 550)}",
                "colorHex": "blue"
            }
        ],
        "newsUpdates": live_news,
        "fundamentalAnalysis": [
            {
                "title": f"Market Sentiment {trend_icon}",
                "bodyText": f"The gold market is showing a {change_pct}% move. Caution is advised near the ${round(current_price)} level."
            }
        ]
    })

@app.route('/journal', methods=['POST'])
def save_journal():
    data = request.json
    try:
        conn = sqlite3.connect('journal.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO journal (date, buy_price, sell_price, tp_price, sl_price, result) VALUES (?,?,?,?,?,?)',
                       (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data.get('buy'), data.get('sell'), data.get('tp'), data.get('sl'), data.get('result')))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 201
    except Exception as e: 
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/journal', methods=['GET'])
def get_journal():
    try:
        conn = sqlite3.connect('journal.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM journal ORDER BY id DESC')
        rows = cursor.fetchall()
        conn.close()
        return jsonify([{"id": r[0], "date": r[1], "buy": r[2], "sell": r[3], "tp": r[4], "sl": r[5], "result": r[6]} for r in rows])
    except:
        return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
