import yfinance as yf
import sqlite3
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# --- HELPER FUNCTIONS ---

def fetch_market_data():
    """Fetches real-time gold price with better error handling."""
    try:
        # 1. Use download for more robust data retrieval
        # '1m' interval gives us the most recent price point
        data = yf.download("XAUUSD=X", period="1d", interval="1m", progress=False)
        
        if not data.empty:
            # Get the very last available price
            curr = round(data['Close'].iloc[-1], 2)
            # Get the price from the start of the day for the trend
            prev = round(data['Close'].iloc[0], 2) 
            
            trend_icon = "▲" if curr >= prev else "▼"
            change_pct = ((curr - prev) / prev) * 100
            
            print(f"Success! Price: {curr}") # Check your console!
            return float(curr), trend_icon, round(change_pct, 2)
            
    except Exception as e:
        print(f"YFinance Error: {e}")
    
    # Updated fallback to match current 2026 Spot Gold (~$5069)
    return 5069.52, "—", 0.0

def get_live_news_feed(trend_icon):
    """Simulates news updates based on market movement."""
    # In a real app, you'd fetch from an RSS feed or News API here
    return [
        {
            "id": 1,
            "title": "Fed Interest Rate Speculation",
            "impact": "BULLISH" if trend_icon == "▲" else "BEARISH",
            "description": "Traders are adjusting positions based on latest inflation data."
        },
        {
            "id": 2,
            "title": "Central Bank Reserves",
            "impact": "BULLISH",
            "description": "Global demand for physical gold remains at historic highs in 2026."
        }
    ]

# --- MAIN ROUTES ---

@app.route('/newsletter', methods=['GET'])
def get_newsletter():
    # Use the fresh data
    current_price, trend_icon, change_pct = fetch_market_data()
    
    # Ensure current_price is valid
    if not current_price:
        current_price = 5069.52

    # Fetch news updates variable
    live_news = get_live_news_feed(trend_icon)

    # YOUR DYNAMIC LEVELS (These now update based on the price)
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
                "bodyText": f"The gold market is currently showing a {change_pct}% move. Trade with caution around the ${round(current_price)} level."
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
        # Create table if it doesn't exist for first-time use
        cursor.execute('''CREATE TABLE IF NOT EXISTS journal 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, 
                           buy_price TEXT, sell_price TEXT, tp_price TEXT, 
                           sl_price TEXT, result TEXT)''')
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
    except Exception as e:
        return jsonify([])

if __name__ == '__main__':
    # Initialize DB on start
    conn = sqlite3.connect('journal.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS journal 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, 
                     buy_price TEXT, sell_price TEXT, tp_price TEXT, 
                     sl_price TEXT, result TEXT)''')
    conn.close()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
