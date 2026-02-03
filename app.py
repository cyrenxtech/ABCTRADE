from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app) # Crucial for SwiftUI communication
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coach_d_journal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class TradeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    entry_price = db.Column(db.String(20))
    sl = db.Column(db.String(20))
    result = db.Column(db.String(10)) # Win/Loss/BE
    coach_feedback = db.Column(db.Text)

with app.app_context():
    db.create_all()

# --- COACH D API ROUTES ---
@app.route('/newsletter', methods=['GET'])
def daily_newsletter():
    # Tailored for Feb 3, 2026 market intelligence
    return jsonify({
        "headline": "THE RELIEF RALLY (WARSH PHASE II)",
        "coach_advise": "Focus on the liquidity sweep of the $4,885 PDH. If we hold $4,780, the path to $5k is open. Do not over-leverage in this high-volatility environment.",
        "bias": "BULLISH RELIEF",
        "buy_range": "$4,780 - $4,815",
        "sell_range": "$4,940 - $4,990",
        "levels": {
            "pdh": 4885.20, "pdl": 4404.10,
            "pwh": 5451.80, "pwl": 4681.40,
            "pmh": 5608.00, "pml": 4345.50
        }
    })

@app.route('/journal', methods=['POST'])
def log_trade():
    data = request.json
    try:
        new_trade = TradeEntry(
            entry_price=data['entryPrice'],
            sl=data['sl'],
            result=data['result'],
            coach_feedback=data.get('feedback', 'No notes added.')
        )
        db.session.add(new_trade)
        db.session.commit()
        return jsonify({"status": "Trade logged to Coach D Database"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
