import os
from flask import Flask, request, render_template
from flask_cors import CORS
import logging
from stock_data import get_stock_data
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Store recent searches
recent_searches = []

@app.route('/')
def index():
    logging.info('Rendering index page')
    return render_template('index.html')

@app.route('/get-stock', methods=['POST'])
def get_stock():
    try:
        symbol = request.form['symbol'].upper()
        stock_data = get_stock_data(symbol)
        if 'error' in stock_data:
            logging.error(f"Error fetching stock data for {symbol}: {stock_data['error']}")
            return render_template('index.html', error=stock_data['error'])
        
        logging.info(f"Successfully fetched stock data for {symbol}")
        
        # Process data for Chart.js
        labels = []
        data = []
        for time, price_info in stock_data.items():
            labels.append(datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))
            data.append(float(price_info['1. open']))  # using '1. open' as an example
        
        # Save to recent searches
        recent_searches.append(symbol)
        
        return render_template('index.html', stock_data=stock_data, symbol=symbol, labels=labels, data=data)
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return render_template('index.html', error='Internal server error')

@app.route('/recent-searches')
def recent_searches_page():
    return render_template('recent_searches.html', searches=recent_searches)

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
