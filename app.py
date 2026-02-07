import xml.etree.ElementTree as ET
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
GOLD_API_KEY = "goldapi-5w1smlcmmepr-io"
NEWS_API_KEY = "bd41341b1983401699fa6c69be2c6e65" 

# --- HELPERS ---

def get_time_ago(date_str):
    """Formats the time to look like 'Feb 08 | 02:45'"""
    try:
        # For NewsAPI (ISO format)
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%b %d | %H:%M")
        # For RSS (Standard format)
        return date_str[5:11] + " | " + date_str[17:22]
    except:
        return "Recent"

def fetch_combined_news(trend_icon):
    combined_news = []

    # 1. Fetch from Kitco (Specialist Gold News)
    try:
        kitco_res = requests.get("https://www.kitco.com/rss/gold-news", timeout=5)
        if kitco_res.status_code == 200:
            root = ET.fromstring(kitco_res.content)
            for item in root.findall('./channel/item')[:2]: # Get top 2
                combined_news.append({
                    "title": f"{trend_icon} {item.find('title').text}",
                    "time_tag": get_time_ago(item.find('pubDate').text),
                    "impact": "MAJOR",
                    "source": "Kitco Gold"
                })
    except: pass

    # 2. Fetch from NewsAPI (Global Market Context)
    try:
        url = f"https://newsapi.org/v2/everything?q=gold+price+XAUUSD&language=en&sortBy=publishedAt&pageSize=2&apiKey={NEWS_API_KEY}"
        news_res = requests.get(url, timeout=5)
        if news_res.status_code == 200:
            articles = news_res.json().get('articles', [])
            for art in articles:
                combined_news.append({
                    "title": f"{trend_icon} {art['title']}",
                    "time_tag": get_time_ago(art['publishedAt']),
                    "impact": "LATEST",
                    "source": art['source']['name']
                })
    except: pass

    return combined_news

def fetch_market_data():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": GOLD_API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            curr = data.get('price', 4966.0)
            prev = data.get('prev_close_price', curr)
            trend_icon = "▲" if curr >= prev else "▼"
            change_pct = round(((curr - prev) / prev) * 100, 2)
            return curr, trend_icon, change_pct
    except: pass
    return 4966.0, "—", 0.0

# --- MAIN ROUTE ---

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    current_price, trend_icon, change_pct = fetch_market_data()
    live_news = fetch_combined_news(trend_icon)

    return jsonify({
        "lastUpdate": datetime.now().strftime("%I:%M %p"),
        "marketTrend": f"{trend_icon} {change_pct}%",
        "price": current_price,
        "newsUpdates": live_news,
        # ... (rest of levels and advice remain the same)
    })
# --- MAIN ROUTE ---

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    current_price, trend_icon, change_pct = fetch_market_data()
    live_news = fetch_gold_specific_news(trend_icon)

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
                "title": f"Gold Market Analysis {trend_icon}",
                "bodyText": f"Major news sources show high activity. Current XAUUSD price is ${current_price}."
            }
        ]
    })

# (Journal routes remain the same...)
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
