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
    # February 6, 2026: Live Market Context
    # Gold recovered to $4,850 after a massive 13% weekly correction.
    # US-Iran diplomacy scheduled for today is the primary "Fear Premium" driver.
    
    return jsonify({
        "monthlyLevel": "PMH: $5,594 / PML: $4,400",
        "weeklyLevel": "PWH: $5,100 / PWL: $4,720",
        "dailyLevel": "PDH: $4,870 / PDL: $4,760",
        
        "entryAdvices": [
            {
                "timeframe": "15M (Scalp)", 
                "buy": "$4,820 – $4,835", "tp": "$4,870", "sl": "$4,805",
                "sell": "$4,890 – $4,910", "sellTP": "$4,840", "sellSL": "$4,925",
                "colorHex": "green"
            },
            {
                "timeframe": "4H (Intraday)", 
                "buy": "$4,720 – $4,760", "tp": "$5,000", "sl": "$4,680",
                "sell": "$5,050 – $5,120", "sellTP": "$4,870", "sellSL": "$5,180",
                "colorHex": "orange"
            },
            {
                "timeframe": "Daily (Swing)", 
                "buy": "$4,530 – $4,650", "tp": "$5,400", "sl": "$4,450",
                "sell": "$5,450 – $5,590", "sellTP": "$5,000", "sellSL": "$5,700",
                "colorHex": "blue"
            }
        ],
        
        "newsUpdates": [
            {
                "title": "US-Iran Diplomacy (Oman)", 
                "impact": "BEARISH", 
                "description": "High-level talks scheduled for Friday afternoon. Diplomatic progress could strip the 'Fear Premium' and push XAUUSD toward $4,750."
            },
            {
                "title": "Nasdaq 'AI Capex' Rout", 
                "impact": "BULLISH", 
                "description": "Software stocks lost $1T this week. Forced deleveraging in tech is creating a safety bid for Gold as investors exit risk assets."
            },
            {
                "title": "US Michigan Consumer Sentiment", 
                "impact": "NEUTRAL", 
                "description": "Data due at 10:00 AM. Markets watching for inflation expectations (Prev: 4.0%). High readings will boost USD, capping Gold."
            }
        ],
        
      # Inside your get_gold_data() function in Flask:

"fundamentalAnalysis": [
    {
        "title": "Risk Management Protocol",
        "bodyText": "Standard Disclaimer: All levels provided are theoretical benchmarks. We recommend a maximum risk of 1-2% per trade. Never trade with capital you cannot afford to lose."
    },
    {
        "title": "Equity Correlation Shift",
        "bodyText": "The traditional inverse correlation is back. As the Nasdaq pulls back from 26k, Gold is reclaiming its role as the ultimate safe-haven hedge."
    }
]
    })

# --- NEW JOURNAL SECTION ---

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

