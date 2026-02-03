from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/newsletter', methods=['GET'])
def get_newsletter():
    # Feb 3, 2026: The Gann 144-Cycle Update
    return jsonify({
        "headline": "THE GANN 144-BAR CYCLE RELIEF",
        "coach_advise": "We have hit the 90-degree square of the previous high. The $4,404 floor is a Gann Natural Number. Expect a 45-degree bounce toward the 1x1 line ($4,885). Watch for the CRT reversal at the London Open.",
        "gann_levels": {
            "square_of_9": 4404.0,
            "1x1_angle": 4885.0,
            "mid_point": 4644.0,
            "next_target": 5120.0
        },
        "bias": "GANN BULLISH",
        "buy_zone": "4,750 (45° Support)",
        "sell_zone": "5,020 (90° Resistance)"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
