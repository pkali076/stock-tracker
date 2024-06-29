import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
BASE_URL = 'https://www.alphavintage.co/query'

def get_stock_data(symbol, interval='1min', outputsize='compact'):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': interval,
        'apikey': API_KEY,
        'outputsize': outputsize
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()
    time_series_key = f'Time Series ({interval})'
    if time_series_key in data:
        return data[time_series_key]
    else:
        return {'error': 'Error fetching data'}
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        symbol = data['symbol'].upper()
        stock_data = get_stock_data(symbol)
    else:
        return """
        <h1>Stock Price Tracker API</h1>
        <p>Use a POST request to this endpoint with a JSON payload containing a stock symbol to get stock data.</p>
        """


if __name__ == '__main__':
    app.run(debug=True)