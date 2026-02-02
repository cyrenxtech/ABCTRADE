import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    tf_code = data.get('timeframe', '15')
    
    # Map for yfinance
    tf_map = {"15": "15m", "240": "4h", "D": "1d"}
    interval = tf_map.get(tf_code, "15m")

    # Fetch Data (GC=F is Gold Futures)
    gold = yf.Ticker("GC=F")
    hist_d = gold.history(period="5d", interval="1d")
    hist_w = gold.history(period="1mo", interval="1wk")
    hist_m = gold.history(period="6mo", interval="1mo")
    current_candles = gold.history(period="1d", interval=interval)
    
    # 1. Previous Levels (Liquidity Points)
    pdh, pdl = hist_d['High'].iloc[-2], hist_d['Low'].iloc[-2]
    pwh, pwl = hist_w['High'].iloc[-2], hist_w['Low'].iloc[-2]
    pmh, pml = hist_m['High'].iloc[-2], hist_m['Low'].iloc[-2]

    # 2. Current Candle Extremes
    curr_low = current_candles['Low'].min()
    curr_high = current_candles['High'].max()

    # 3. Dynamic Zone Calculation
    # Buy Zone: Current Low to the lowest historical low
    buy_floor = min(pdl, pwl, pml)
    buy_range = f"{min(curr_low, buy_floor):.2f} - {max(curr_low, buy_floor):.2f}"

    # Sell Zone: Current High to the highest historical high
    sell_ceiling = max(pdh, pwh, pmh)
    sell_range = f"{min(curr_high, sell_ceiling):.2f} - {max(curr_high, sell_ceiling):.2f}"

    return jsonify({
        "sentiment": "NEUTRAL",
        "educational_note": f"Gold {interval} analysis complete. Watch horizontal rays.",
        "buy_range": buy_range,
        "sell_range": sell_range,
        "levels": {
            "pdh": pdh, "pdl": pdl, "pwh": pwh, "pwl": pwl, "pmh": pmh, "pml": pml

            @app.route('/ask', methods=['POST'])
def ask_coach():
    user_query = request.json.get('message')
    current_context = request.json.get('context') # Pass current price/levels
    
    # Example logic for a smart response
    # In production, you would send user_query + context to OpenAI API here
    response_text = f"Based on the {current_context['tf']} timeframe, Gold is holding near {current_context['pdh']}. If it breaks this, look for a sell-off toward the Blue weekly levels."
    
    return jsonify({"answer": response_text})
        }
        pip install open API
                 import os
from openai import OpenAI
from flask import Flask, request, jsonify

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

@app.route('/ask', methods=['POST'])
def ask_coach():
    data = request.json
    user_message = data.get('message')
    context = data.get('context') # This receives the prices from your Swift app
    
    # System prompt defines the AI's "personality" and knowledge
    system_prompt = f"""
    You are the ABC Gold Coach. You are an expert in Gold (XAUUSD) Liquidity.
    Current Context:
    - Timeframe: {context['timeframe']}
    - Daily High (PDH): {context['current_levels']['pdh']}
    - Weekly High (PWH): {context['current_levels']['pwh']}
    
    Give short, professional advice (max 2 sentences). 
    If price is near PDH, suggest watching for a liquidity sweep.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    
    answer = response.choices[0].message.content
    return jsonify({"answer": answer})
    })
