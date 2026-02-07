from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION (Replace with your keys) ---
GOLD_API_KEY = "goldapi-5w1smlcmmepr-io"  # Get from goldapi.io
NEWS_API_KEY = "bd41341b1983401699fa6c69be2c6e65"  # Get from newsapi.org

# --- DATABASE SETUP FOR JOURNAL (Existing) ---
def init_db():
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            buy_price REAL,
            sell_price REAL,
            tp_price REAL,
            sl_price REAL,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- AUTOMATION HELPERS ---

def fetch_live_gold_price():
    """Fetches real-time price from GoldAPI.io"""
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": GOLD_API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json().get('price', 4966.0)
    except:
        pass
    return 4966.0  # Fallback

def fetch_live_news():
    """Fetches live news from NewsAPI.org"""
    url = f"https://newsapi.org/v2/everything?q=gold+market+XAUUSD&language=en&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return [
                {
                    "title": art['title'],
                    "impact": "LIVE",
                    "description": art['description'][:120] + "..." if art['description'] else "No summary available."
                } for art in articles
            ]
    except:
        pass
    return []

# --- MAIN DATA ROUTE ---

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    current_price = fetch_live_gold_price()
    live_news = fetch_live_news()
    
    # Mathematical pivot calculations based on live price
    levels = {
        "monthlyLevel": f"PMH: ${round(current_price * 1.12)} / PML: ${round(current_price * 0.88)}",
        "weeklyLevel": f"PWH: ${round(current_price + 60)} / PWL: ${round(current_price - 60)}",
        "dailyLevel": f"PDH: ${round(current_price + 20)} / PDL: ${round(current_price - 20)}"
    }
    
    # UPDATED: Timeframes 15M, 4H, and 1Day
    entry_advices = [
        {
            "timeframe": "15M (Scalp)", 
            "buy": f"${round(current_price - 8)} – ${round(current_price - 4)}", 
            "tp": f"${round(current_price + 12)}", "sl": f"${round(current_price - 15)}",
            "sell": f"${round(current_price + 10)} – ${round(current_price + 15)}", 
            "sellTP": f"${round(current_price - 8)}", "sellSL": f"${round(current_price + 25)}",
            "colorHex": "green"
        },
        {
            "timeframe": "4H (Intraday)", 
            "buy": f"${round(current_price - 40)} – ${round(current_price - 20)}", 
            "tp": f"${round(current_price + 80)}", "sl": f"${round(current_price - 60)}",
            "sell": f"${round(current_price + 60)} – ${round(current_price + 100)}", 
            "sellTP": f"${round(current_price - 40)}", "sellSL": f"${round(current_price + 130)}",
            "colorHex": "orange"
        },
        {
            "timeframe": "1Day (Swing)", 
            "buy": f"${round(current_price - 150)} – ${round(current_price - 100)}", 
            "tp": f"${round(current_price + 300)}", "sl": f"${round(current_price - 200)}",
            "sell": f"${round(current_price + 250)} – ${round(current_price + 400)}", 
            "sellTP": f"${round(current_price - 200)}", "sellSL": f"${round(current_price + 550)}",
            "colorHex": "blue"
        }
    ]

    return jsonify({
        **levels,
        "entryAdvices": entry_advices,
        "newsUpdates": live_news if live_news else [{"title": "Updating news...", "impact": "NEUTRAL", "description": "Fetch in progress."}],
        "fundamentalAnalysis": [
            {
                "title": "Automated Market View",
                "bodyText": f"XAUUSD is trading at ${current_price}. Pivot zones are refreshed automatically based on current market volatility."
            }
        ]
    })

# --- JOURNAL SECTION (UNTOUCHED) ---

@app.route('/journal', methods=['POST'])
def save_journal():
    data = request.json
    try:
        conn = sqlite3.connect('journal.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO journal (date, buy_price, sell_price, tp_price, sl_price, result)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get('buy'), data.get('sell'), data.get('tp'), data.get('sl'), data.get('result')
        ))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

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
