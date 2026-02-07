from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- DATABASE SETUP FOR JOURNAL ---
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

@app.route('/newsletter', methods=['GET'])
def get_gold_data():
    # February 8, 2026: Live Market Context
    # Gold (XAUUSD) closed the week strong at $4,966 after a volatile dip to $4,400.
    # The market is currently testing the psychological $5,000 resistance.
    
    return jsonify({
        "monthlyLevel": "PMH: $5,595 / PML: $4,400",
        "weeklyLevel": "PWH: $5,024 / PWL: $4,402",
        "dailyLevel": "PDH: $4,971 / PDL: $4,655",
        
        "entryAdvices": [
            {
                "timeframe": "15M (Scalp)", 
                "buy": "$4,920 – $4,935", "tp": "$4,980", "sl": "$4,905",
                "sell": "$4,990 – $5,010", "sellTP": "$4,950", "sellSL": "$5,025",
                "colorHex": "green"
            },
            {
                "timeframe": "4H (Intraday)", 
                "buy": "$4,750 – $4,800", "tp": "$5,050", "sl": "$4,710",
                "sell": "$5,080 – $5,150", "sellTP": "$4,920", "sellSL": "$5,200",
                "colorHex": "orange"
            },
            {
                "timeframe": "Daily (Swing)", 
                "buy": "$4,450 – $4,600", "tp": "$5,500", "sl": "$4,380",
                "sell": "$5,550 – $5,650", "sellTP": "$5,100", "sellSL": "$5,750",
                "colorHex": "blue"
            }
        ],
        
        "newsUpdates": [
            {
                "title": "US-Iran Diplomacy Update", 
                "impact": "BEARISH", 
                "description": "The 'Fear Premium' is easing as Oman talks show progress. Technicals suggest a move toward $4,800 if $4,950 support breaks."
            },
            {
                "title": "Central Bank Accumulation", 
                "impact": "BULLISH", 
                "description": "Emerging markets continue to diversify reserves. Long-term structural demand remains the primary floor for XAUUSD at $4,500."
            },
            {
                "title": "Nasdaq Volatility Spillover", 
                "impact": "NEUTRAL", 
                "description": "Tech stocks' 'AI Capex' correction is forcing some liquidity exits in Gold, creating choppy two-way price action."
            }
        ],
        
        "fundamentalAnalysis": [
            {
                "title": "Risk Management Protocol",
                "bodyText": "Standard Disclaimer: All levels provided are theoretical benchmarks. We recommend a maximum risk of 1-2% per trade. Never trade with capital you cannot afford to lose."
            },
            {
                "title": "The $5,000 Psychological Barrier",
                "bodyText": "Gold is battling the $5,000 mark. A clean daily close above this level could trigger a massive short-squeeze toward the $5,600 ATH."
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
            data.get('buy'),
            data.get('sell'),
            data.get('tp'),
            data.get('sl'),
            data.get('result')
        ))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Journal entry saved!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/journal', methods=['GET'])
def get_journal():
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM journal ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "date": row[1],
            "buy": row[2],
            "sell": row[3],
            "tp": row[4],
            "sl": row[5],
            "result": row[6]
        })
    return jsonify(history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
