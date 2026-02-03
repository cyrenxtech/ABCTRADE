from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Creates a local file called 'trading.db' to store your trades
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trading.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    entry_price = db.Column(db.String(20))
    tp = db.Column(db.String(20))
    sl = db.Column(db.String(20))
    result = db.Column(db.String(10)) # Win, Loss, BE
    mood = db.Column(db.String(10))

# Create the database tables
with app.app_context():
    db.create_all()

# --- ROUTES ---
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    tf = data.get('timeframe', '15')
    
    # 2026 Market Context: Gold recovering from 'Warsh Shock' volatility
    return jsonify({
        "sentiment": "Recovery/Bullish",
        "educational_note": f"XAUUSD ({tf}M) is stabilizing above $4,780. Look for liquidity grabs at PDH before continuation.",
        "buy_range": "$4,780 - $4,810",
        "sell_range": "$4,940 - $4,980",
        "levels": {
            "pdh": 4885.0, "pdl": 4402.0,
            "pwh": 5451.0, "pwl": 4681.0,
            "pmh": 5608.0, "pml": 4345.0
        }
    })

@app.route('/journal', methods=['POST', 'GET'])
def journal():
    if request.method == 'POST':
        data = request.json
        new_entry = JournalEntry(
            entry_price=data['entryPrice'],
            tp=data['tp'],
            sl=data['sl'],
            result=data['result'],
            mood=data['mood']
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"status": "success"})
    
    # GET: Return last 10 entries
    entries = JournalEntry.query.order_by(JournalEntry.timestamp.desc()).limit(10).all()
    return jsonify([{
        "entryPrice": e.entry_price, "tp": e.tp, "sl": e.sl, 
        "result": e.result, "mood": e.mood
    } for e in entries])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
