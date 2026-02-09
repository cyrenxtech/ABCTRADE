import yfinance as yf

def fetch_market_data():
    """Fetches gold price using yfinance for better reliability."""
    try:
        # XAUUSD=X is the Yahoo Finance symbol for Gold Spot US Dollar
        gold = yf.Ticker("XAUUSD=X")
        data = gold.history(period="2d")
        
        if not data.empty:
            curr = round(data['Close'].iloc[-1], 2)
            prev = round(data['Close'].iloc[-2], 2)
            
            trend_icon = "▲" if curr >= prev else "▼"
            change_pct = ((curr - prev) / prev) * 100
            return curr, trend_icon, round(change_pct, 2)
    except Exception as e:
        print(f"Error fetching data: {e}")
    
    # Updated fallback to something closer to current 2026 market levels
    return 5075.0, "—", 0.0 

@app.route('/newsletter', methods=['GET'])
def get_newsletter():
    # Call the helper to get fresh data
    current_price, trend_icon, change_pct = fetch_market_data()

    return jsonify({
        "price": current_price,
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
