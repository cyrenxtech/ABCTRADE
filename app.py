import os
import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Replace with your actual key or use environment variables
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
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
        
        # 1. Previous Levels (Liquidity Points) - iloc[-2] gets the most recently CLOSED period
        pdh, pdl = float(hist_d['High'].iloc[-2]), float(hist_d['Low'].iloc[-2])
        pwh, pwl = float(hist_w['High'].iloc[-2]), float(hist_w['Low'].iloc[-2])
        pmh, pml = float(hist_m['High'].iloc[-2]), float(hist_m['Low'].iloc[-2])

        # 2. Current Candle Extremes
        curr_low = float(current_candles['Low'].min())
        curr_high = float(current_candles['High'].max())

        # 3. Dynamic Zone Calculation
        buy_floor = min(pdl, pwl, pml)
        buy_range = f"{min(curr_low, buy_floor):.2f} - {max(curr_low, buy_floor):.2f}"

        sell_ceiling = max(pdh, pwh, pmh)
        sell_range = f"{min(curr_high, sell_ceiling):.2f} - {max(curr_high, sell_ceiling):.2f}"

        return jsonify({
            "sentiment": "NEUTRAL",
            "educational_note": f"Gold {interval} analysis complete. Watch horizontal rays.",
            "buy_range": buy_range,
            "sell_range": sell_range,
            "levels": {
                "pdh": pdh, "pdl": pdl, 
                "pwh": pwh, "pwl": pwl, 
                "pmh": pmh, "pml": pml
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_coach():
    try:
        data = request.json
        user_message = data.get('message')
        context = data.get('context') # Receives timeframe and levels from Swift
        
        # Extract context safely
        tf = context.get('timeframe', 'Unknown')
        levels = context.get('current_levels', {})
        pdh = levels.get('pdh', 'N/A')
        pwh = levels.get('pwh', 'N/A')

        system_prompt = f"""
        You are the ABC Gold Coach, an expert in XAUUSD Liquidity trading.
        Current Market Context:
        - Active Timeframe: {tf}
        - Previous Daily High (PDH): {pdh}
        - Previous Weekly High (PWH): {pwh}
        
        Rules:
        1. Give short, professional advice (max 2 sentences).
        2. Use a "trader-to-trader" tone.
        3. If price is near PDH, suggest watching for a liquidity sweep or rejection.
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
    except Exception as e:
        return jsonify({"answer": "Coach is currently offline. Check your API key."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
