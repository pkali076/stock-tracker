import os
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
BASE_URL = 'https://www.alphavantage.co/query'

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
        data = request.form
        symbol = data['symbol'].upper()
        stock_data = get_stock_data(symbol)
        if 'error' in stock_data:
            return render_template('index.html', error=stock_data['error'])
        labels = list(stock_data.keys())
        data = [float(value['1. open']) for value in stock_data.values()]
        return render_template('index.html', symbol=symbol, stock_data=stock_data, labels=labels, data=data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)






# import os
# from flask import Flask, request, render_template
# from flask_cors import CORS
# import logging
# from stock_data import get_stock_data
# from datetime import datetime

# app = Flask(__name__)
# CORS(app)

# # Set up logging
# logging.basicConfig(level=logging.INFO)

# # Store recent searches
# recent_searches = []

# @app.route('/')
# def index():
#     logging.info('Rendering index page')
#     return render_template('index.html')

# @app.route('/get-stock', methods=['POST'])
# def get_stock():
#     try:
#         symbol = request.form['symbol'].upper()
#         stock_data = get_stock_data(symbol)
#         if 'error' in stock_data:
#             logging.error(f"Error fetching stock data for {symbol}: {stock_data['error']}")
#             return render_template('index.html', error=stock_data['error'])
        
#         logging.info(f"Successfully fetched stock data for {symbol}")
        
#         # Process data for Chart.js
#         labels = []
#         data = []
#         for time, price_info in stock_data.items():
#             labels.append(datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))
#             data.append(float(price_info['1. open']))  # using '1. open' as an example
        
#         # Save to recent searches
#         recent_searches.append(symbol)
        
#         return render_template('index.html', stock_data=stock_data, symbol=symbol, labels=labels, data=data)
#     except Exception as e:
#         logging.error(f"Error processing request: {e}")
#         return render_template('index.html', error='Internal server error')

# @app.route('/recent-searches')
# def recent_searches_page():
#     return render_template('recent_searches.html', searches=recent_searches)

# if __name__ == '__main__':
#     app.run(debug=True)
