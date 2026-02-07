from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
GOLD_API_KEY = "goldapi-5w1smlcmmepr-io"  # From GoldAPI.io
NEWS_API_KEY = "bd41341b1983401699fa6c69be2c6e65"  # From NewsAPI.org

def init_db():
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            buy_price REAL, sell_price REAL, tp_price REAL, sl_price REAL, result TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- NEW: HELPER TO FETCH LIVE NEWS ---
def fetch_live_news():
    try:
        url = f"https://newsapi.org/v2/everything?q=gold+market+XAUUSD&language=en&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=5)
        articles = response.json().get('articles', [])
        
        news_list = []
        for art in articles:
            news_list.append({
                "title": art['title'],
                "impact": "LIVE UPDATE", # Automated tags
                "description": art['description'][:150] + "..." if art['description'] else "Click to read more."
            })
        return news_list if news_list else [{"title": "No recent news", "impact": "NEUTRAL", "description": "Market is quiet."}]
    except:
        return [{"title": "News Feed Offline", "impact": "ERROR", "description": "Could not connect to news server."}]

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    # 1. Fetch Live Price
    current_price = 4966.0 # Default
    try:
        price_res = requests.get("https://www.goldapi.io/api/XAU/USD", headers={"x-access-token": GOLD_API_KEY}, timeout=5)
        if price_res.status_code == 200:
            current_price = price_res.json().get('price', 4966.0)
    except: pass

    # 2. Fetch Live News
    live_news = fetch_live_news()

    return jsonify({
        "status": "Fully Automated",
        "lastUpdated": datetime.now().strftime("%H:%M"),
        "monthlyLevel": f"PMH: ${round(current_price * 1.1)} / PML: ${round(current_price * 0.9)}",
        "weeklyLevel": f"PWH: ${round(current_price + 50)} / PWL: ${round(current_price - 50)}",
        "dailyLevel": f"PDH: ${round(current_price + 15)} / PDL: ${round(current_price - 15)}",
        
        "entryAdvices": [
            {
                "timeframe": "15M (Scalp)", 
                "buy": f"${round(current_price - 8)}", "tp": f"${round(current_price + 12)}", "sl": f"${round(current_price - 15)}",
                "sell": f"${round(current_price + 12)}", "sellTP": f"${round(current_price - 8)}", "sellSL": f"${round(current_price + 20)}",
                "colorHex": "green"
            }
        ],
        
        "newsUpdates": live_news, # NOW AUTOMATIC HEADLINES
        
        "fundamentalAnalysis": [
            {
                "title": "Automated Market Sentiment",
                "bodyText": f"XAUUSD is currently ${current_price}. Pivot points and news are refreshed every time you open the app."
            }
        ]
    })

# --- JOURNAL ROUTES REMAIN UNCHANGED ---
@app.route('/journal', methods=['POST'])
def save_journal():
    data = request.json
    try:
        conn = sqlite3.connect('journal.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO journal (date, buy_price, sell_price, tp_price, sl_price, result) VALUES (?, ?, ?, ?, ?, ?)',
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
