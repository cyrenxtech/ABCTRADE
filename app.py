from flask import Flask, request, jsonify

from flask_cors import CORS



app = Flask(__name__)

CORS(app)



def calculate_zones(base_price, pip_range):

    # Buy Zone: Lowest Low to Lowest High (Demand)

    # Using Fibonacci 0.0 to 0.236 for the "Extreme Demand" zone

    buy_low = base_price - (pip_range / 2)

    buy_high = buy_low + (pip_range * 0.236)

    

    # Sell Zone: Highest Low to Highest High (Supply)

    # Using Fibonacci 0.786 to 1.0 for the "Extreme Supply" zone

    sell_high = base_price + (pip_range / 2)

    sell_low = sell_high - (pip_range * 0.236)

    

    return {

        "buy": f"{buy_low:.2f} - {buy_high:.2f}",

        "sell": f"{sell_low:.2f} - {sell_high:.2f}"

    }



@app.route('/analyze', methods=['POST'])

def analyze():

    data = request.json

    tf = data.get('timeframe', '15')

    

    # Live Gold Price (XAUUSD) Mock - Replace with real API for production

    current_gold_price = 2035.50 



    if tf == "D":

        # 1 Day = 200 Pip Range ($20.00 for Gold)

        pip_val = 20.0

        bias = "DAILY BIAS: Institutional Liquidity Hunt. Look for PMH/PML sweeps."

    elif tf == "240":

        # 4 Hour = 100 Pip Range ($10.00 for Gold)

        pip_val = 10.0

        bias = "4H BIAS: Trend Continuation. Watch for PWH/PWL reactions."

    else:

        # 15 Min = 50 Pip Range ($5.00 for Gold)

        pip_val = 5.0

        bias = "15M BIAS: Scalp Range. Use PDH/PDL for entry targets."



    zones = calculate_zones(current_gold_price, pip_val)



    return jsonify({

        "sentiment": "ANALYZING",

        "educational_note": bias,

        "buy_range": zones["buy"],

        "sell_range": zones["sell"]

    })



if __name__ == "__main__":

    app.run(host='0.0.0.0', port=5000)
