from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///entries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model for your Journal
class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    entry_price = db.Column(db.String(20))
    tp = db.Column(db.String(20))
    sl = db.Column(db.String(20))
    result = db.Column(db.String(20)) # Win / Loss / BE
    mood = db.Column(db.String(10))

with app.app_context():
    db.create_all()

@app.route('/journal', methods=['POST'])
def add_entry():
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
    return jsonify({"status": "Trade Logged Successfully"}), 201

@app.route('/journal', methods=['GET'])
def get_entries():
    entries = JournalEntry.query.order_by(JournalEntry.date.desc()).all()
    return jsonify([{
        "date": e.date.strftime("%Y-%m-%d"),
        "entry": e.entry_price,
        "result": e.result,
        "mood": e.mood
    } for e in entries])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
