from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = 'AlphaVintageAPIKey'
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
    
@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    symbol = data['symbol'].upper()
    stock_data = get_stock_data(symbol)
    return jsonify(stock_data)

if __name__ == '__main__':
    app.run(debug=True)