import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/analyze', methods=['POST'])
def analyze():
    # This is the data your iPhone app will receive
    return jsonify({
        "sentiment": "BULLISH",
        "educational_note": "15M Sweep confirmed. Displacement above PDH detected.",
        "buy_range": "$2030 - $2035",
        "sell_range": "$2055 - $2060"
    })

if __name__ == "__main__":
    # Render provides the port automatically via environment variables
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)