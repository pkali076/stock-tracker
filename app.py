import os
from flask import Flask, request, render_template
from flask_cors import CORS
import logging
from stock_data import get_stock_data
from datetime import datetime

app = Flask(__name__) #Initialize Flask application for templates and app routing
CORS(app) #enable cross-origin resource sharing for all routes

# Set up logging for informational messages
logging.basicConfig(level=logging.INFO)

#initialize list to store recent stock symbol searches
recent_searches = []

@app.route('/')
def index():
    #render index.html template when accessing the root URL
    logging.info('Rendering index page')
    return render_template('index.html')

@app.route('/get-stock', methods=['POST'])
def get_stock():
    """
    Handle the POST request to get stock data for a given symbol
    Process data and render the index.html template with the stock data
    """
    try:
        #get stock symbol from the form and covert it to uppercase for searching
        symbol = request.form['symbol'].upper()
        # fetch stock data using get_stock_data function
        stock_data = get_stock_data(symbol)
        #check if there were errors in fetching stock data
        if 'error' in stock_data:
            logging.error(f"Error fetching stock data for {symbol}: {stock_data['error']}")
            return render_template('index.html', error=stock_data['error'])
        
        logging.info(f"Successfully fetched stock data for {symbol}")
        
        # process stock data for displaying in chart
        labels = [] #initialize array for labels on chart
        data = [] #initialize array for the data on chart
        for time, price_info in stock_data.items():
            #convert time string to a datetime object and format it
            labels.append(datetime.strptime(time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))
            #extract the open price and covert to a float
            data.append(float(price_info['1. open']))
        
        # Save search symbol to recent searches for recent_searches.html template
        recent_searches.append(symbol)
        # render index.html template
        return render_template('index.html', stock_data=stock_data, symbol=symbol, labels=labels, data=data)
    except Exception as e:
        logging.error(f"Error processing request: {e}") #log exceptions
        return render_template('index.html', error='Internal server error')

@app.route('/recent-searches')
def recent_searches_page():
    # render recent_searches.html template with list of recent searches
    return render_template('recent_searches.html', searches=recent_searches)

if __name__ == '__main__':
    app.run(debug=True) #debug mode allows for further error logging in development
