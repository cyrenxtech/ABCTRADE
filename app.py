from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import requests
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION (Replace with your actual keys) ---
GOLD_API_KEY = "goldapi-5w1smlcmmepr-io"
NEWS_API_KEY = "bd41341b1983401699fa6c69be2c6e65"

def init_db():
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT, buy_price REAL, sell_price REAL, tp_price REAL, sl_price REAL, result TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- HELPERS ---

def get_time_ago(iso_date_str):
    """Calculates time passed since news was published."""
    try:
        pub_time = datetime.fromisoformat(iso_date_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        diff = now - pub_time
        minutes = int(diff.total_seconds() / 60)
        if minutes < 60: return f"{minutes}m ago"
        hours = int(minutes / 60)
        if hours < 24: return f"{hours}h ago"
        return pub_time.strftime("%b %d")
    except: return ""

def fetch_market_data():
    """Fetches gold price and previous close to determine trend."""
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": GOLD_API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            curr = data.get('price', 4966.0)
            # EXTREME POINTS: Capture current high and low wicks
            high_wick = data.get('high_price', curr)
            low_wick = data.get('low_price', curr)
            prev = data.get('prev_close_price', curr) 
            
            trend_icon = "▲" if curr >= prev else "▼"
            change_pct = ((curr - prev) / prev) * 100
            return curr, high_wick, low_wick, trend_icon, round(change_pct, 2)
    except: pass
    return 4966.0, 4966.0, 4966.0, "—", 0.0

def fetch_live_news(trend_icon):
    """Fetches news and injects trend icon + time ago into titles."""
    url = f"https://newsapi.org/v2/everything?q=gold+price+XAUUSD&language=en&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return [
                {
                    "title": f"{trend_icon} {art['title']} — ({get_time_ago(art['publishedAt'])})",
                    "impact": "LATEST",
                    "description": art['description'][:110] + "..." if art['description'] else ""
                } for art in articles
            ]
    except: pass
    return []

# --- ROUTES ---

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    # Calculation is now based on current high/low wicks, not just closing price
    current_price, high_pt, low_pt, trend_icon, change_pct = fetch_market_data()
    live_news = fetch_live_news(trend_icon)

    return jsonify({
        "lastUpdate": datetime.now().strftime("%I:%M %p"),
        "marketTrend": f"{trend_icon} {change_pct}%",
        # Levels based on the absolute highest and lowest points of the period
        "monthlyLevel": f"PMH: ${round(high_pt * 1.12)} / PML: ${round(low_pt * 0.88)}",
        "weeklyLevel": f"PWH: ${round(high_pt + 60)} / PWL: ${round(low_pt - 60)}",
        "dailyLevel": f"PDH: ${round(high_pt)} / PDL: ${round(low_pt)}",
        
        "entryAdvices": [
            {
                "timeframe": "15M (Scalp)", 
                "buy": f"${round(low_pt - 8)}", "tp": f"${round(low_pt + 12)}", "sl": f"${round(low_pt - 15)}",
                "sell": f"${round(high_pt + 10)}", "sellTP": f"${round(high_pt - 8)}", "sellSL": f"${round(high_pt + 25)}",
                "colorHex": "green"
            },
            {
                "timeframe": "4H (Intraday)", 
                "buy": f"${round(low_pt - 40)}", "tp": f"${round(low_pt + 80)}", "sl": f"${round(low_pt - 60)}",
                "sell": f"${round(high_pt + 60)}", "sellTP": f"${round(high_pt - 40)}", "sellSL": f"${round(high_pt + 130)}",
                "colorHex": "orange"
            },
            {
                "timeframe": "1Day (Swing)", 
                "buy": f"${round(low_pt - 150)}", "tp": f"${round(low_pt + 300)}", "sl": f"${round(low_pt - 200)}",
                "sell": f"${round(high_pt + 250)}", "sellTP": f"${round(high_pt - 200)}", "sellSL": f"${round(high_pt + 550)}",
                "colorHex": "blue"
            }
        ],
        "newsUpdates": live_news,
        "fundamentalAnalysis": [
            {
                "title": f"Market Sentiment {trend_icon}",
                "bodyText": f"The gold market is currently showing a {change_pct}% move. Session extremes: High ${high_pt} / Low ${low_pt}. Trade with caution."
            }
        ]
    })

# --- JOURNAL ROUTES (UNTOUCHED) ---
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
    except Exception as e: return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/journal', methods=['GET'])
def get_journal():
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM journal ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "date": r[1], "buy": r[2], "sell": r[3], "tp": r[4], "sl": r[5], "result": r[6]} for r in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
