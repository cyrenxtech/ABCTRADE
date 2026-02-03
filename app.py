from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trading.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Permanent Journal Database
class TradeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    pair = db.Column(db.String(10), default="XAUUSD")
    entry = db.Column(db.String(20))
    sl = db.Column(db.String(20))
    result = db.Column(db.String(10)) # Win/Loss
    coach_note = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route('/newsletter', methods=['GET'])
def get_daily_update():
    # Coach D's Feb 3, 2026 Market Intelligence
    return jsonify({
        "headline": "THE WARSH SHOCK RECOVERY",
        "coach_advise": "The prior one-direction bull run is dead. We are now in a volatility phase. Gold found massive demand at $4,400 (The Floor). We are currently rebounding toward $4,850. Do not chase the pump—wait for the sweep of PDL.",
        "levels": {
            "pdh": 4885.0, "pdl": 4404.0,  # Previous Day High/Low
            "pwh": 5451.0, "pwl": 4681.0,  # Previous Week High/Low
            "pmh": 5608.0, "pml": 4345.0   # Previous Month High/Low
        },
        "bias": "BULLISH RELIEF",
        "buy_zone": "$4,750 - $4,780",
        "sell_zone": "$4,950 - $5,050"
    })

@app.route('/log_trade', methods=['POST'])
def log_trade():
    data = request.json
    new_log = TradeLog(
        entry=data['entry'],
        sl=data['sl'],
        result=data['result'],
        coach_note=data.get('note', '')
    )
    db.session.add(new_log)
    db.session.commit()
    return jsonify({"status": "Logged to Database"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
