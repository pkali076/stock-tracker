import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
from stock_data import get_stock_data

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

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
        return render_template('index.html', stock_data=stock_data, symbol=symbol)
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return render_template('index.html', error='Internal server error')

if __name__ == '__main__':
    app.run(debug=True)
