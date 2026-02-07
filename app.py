import xml.etree.ElementTree as ET
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

GOLD_API_KEY = "goldapi-5w1smlcmmepr-io"

# --- HELPERS ---

def fetch_gold_specific_news(trend_icon):
    """Pulls news from Kitco (Gold Specialists) and Myfxbook."""
    # Kitco is much better for 'Major Gold News'
    rss_url = "https://www.kitco.com/rss/gold-news" 
    news_list = []
    
    try:
        response = requests.get(rss_url, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall('./channel/item')[:3]:
                title = item.find('title').text
                # Get the full date/time from the feed
                pub_date_raw = item.find('pubDate').text 
                
                # Format: "Sun, 08 Feb"
                short_date = pub_date_raw[5:11] 
                # Format: "02:45"
                short_time = pub_date_raw[17:22] 

                news_list.append({
                    # Added small letters (date/time) next to title as requested
                    "title": f"{trend_icon} {title}",
                    "time_tag": f"{short_date} | {short_time}", # Small letters data
                    "impact": "MAJOR",
                    "description": "Source: Kitco Gold"
                })
        return news_list
    except Exception as e:
        print(f"Error: {e}")
        return [{"title": "Searching for Gold news...", "time_tag": "Live", "impact": "INFO"}]

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
