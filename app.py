import xml.etree.ElementTree as ET # New import for RSS parsing
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import requests
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
GOLD_API_KEY = "goldapi-5w1smlcmmepr-io"

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

def fetch_myfxbook_news(trend_icon):
    """Fetches live news from Myfxbook RSS Feed (Forex & Gold focus)."""
    rss_url = "https://www.myfxbook.com/rss/forex-news"
    news_list = []
    try:
        response = requests.get(rss_url, timeout=10)
        if response.status_code == 200:
            # Parse the XML RSS Feed
            root = ET.fromstring(response.content)
            # Find the first 3 news items
            for item in root.findall('./channel/item')[:3]:
                title = item.find('title').text
                pub_date = item.find('pubDate').text # Format: Tue, 03 Feb 2026 12:00:00 GMT
                
                # Format the title as requested: Arrow + Title + (Time)
                news_list.append({
                    "title": f"{trend_icon} {title} — ({pub_date[5:16]})",
                    "impact": "HIGH",
                    "description": "Source: Myfxbook Live Feed"
                })
        return news_list
    except Exception as e:
        print(f"RSS Error: {e}")
        return [{"title": "News sync error", "impact": "LOW", "description": "Check connection"}]

def fetch_market_data():
    """Fetches gold price and trend data."""
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": GOLD_API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            curr = data.get('price', 4966.0)
            prev = data.get('prev_close_price', curr)
            trend_icon = "▲" if curr >= prev else "▼"
            change_pct = ((curr - prev) / prev) * 100
            return curr, trend_icon, round(change_pct, 2)
    except: pass
    return 4966.0, "—", 0.0

# --- MAIN ROUTE ---

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    current_price, trend_icon, change_pct = fetch_market_data()
    # Now using the Myfxbook RSS helper
    live_news = fetch_myfxbook_news(trend_icon)

    return jsonify({
        "lastUpdate": datetime.now().strftime("%I:%M %p"),
        "marketTrend": f"{trend_icon} {change_pct}%",
        "monthlyLevel": f"PMH: ${round(current_price * 1.12)} / PML: ${round(current_price * 0.88)}",
        "weeklyLevel": f"PWH: ${round(current_price + 60)} / PWL: ${round(current_price - 60)}",
        "dailyLevel": f"PDH: ${round(current_price + 20)} / PDL: ${round(current_price - 20)}",
        
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
                "title": f"Market Insight {trend_icon}",
                "bodyText": f"Forex Factory sentiment suggests high volatility. Current XAUUSD price is ${current_price}."
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
