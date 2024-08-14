import os
from flask import Flask, request, render_template
from flask_cors import CORS
import logging
from stock_data import get_stock_data, get_daily_stock_data, get_monthly_stock_data, get_weekly_stock_data
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
        # fetch stock data using imported functions from stock_data module
        stock_data = get_stock_data(symbol)
        daily_data = get_daily_stock_data(symbol)
        weekly_data = get_weekly_stock_data(symbol)
        monthly_data = get_monthly_stock_data(symbol)
        #check if there were errors in fetching stock data
        if 'error' in stock_data:
            logging.error(f"Error fetching stock data for {symbol}: {stock_data['error']}")
            return render_template('index.html', error=stock_data['error'])
        
        logging.info(f"Successfully fetched stock data for {symbol}")
        
        # process stock data for displaying in chart
        labels_intraday, data_intraday = process_stock_data(stock_data, '15min')
        labels_daily, data_daily = process_stock_data(daily_data, 'Daily')
        labels_weekly, data_weekly = process_stock_data(weekly_data, 'Weekly')
        labels_monthly, data_monthly = process_stock_data(monthly_data, 'Monthly')

        logging.info(f"Labels Intraday: {labels_intraday}")
        logging.info(f"Data Intraday: {data_intraday}")
        logging.info(f"Labels Daily: {labels_daily}")
        logging.info(f"Data Daily: {data_daily}")
        logging.info(f"Labels Weekly: {labels_weekly}")
        logging.info(f"Data Weekly: {data_weekly}")
        logging.info(f"Labels monthly: {labels_monthly}")
        logging.info(f"Data Monthly: {data_monthly}")


        # labels = [] #initialize array for labels on chart
        # data = [] #initialize array for the data on chart
        # for time, price_info in stock_data.items():
        #     #convert time string to a datetime object and format it
        #     labels.append(datetime.strptime(time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))
        #     #extract the open price and covert to a float
        #     data.append(float(price_info['1. open']))
        
        # Save search symbol to recent searches for recent_searches.html template
        recent_searches.append(symbol)
        # render index.html template
        return render_template('index.html', stock_data=stock_data, symbol=symbol, labels_intraday=labels_intraday,
                               data_intraday=data_intraday, labels_daily=labels_daily, data_daily=data_daily,
                               labels_weekly=labels_weekly, data_weekly=data_weekly, labels_monthly=labels_monthly,
                               data_monthly=data_monthly)
    except Exception as e:
        logging.error(f"Error processing request: {e}") #log exceptions
        return render_template('index.html', error='Internal server error')

def process_stock_data(data, interval):
    labels = []
    data_points = []
    for time, price_info in data.items():
        try:
            if interval == '15min':
                label = datetime.strptime(time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            else:
                label = time
            labels.append(label)

            data_point = float(price_info.get('1. open', 0))
            data_points.append(data_point)

        # try:
        #     label = datetime.strptime(time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') if interval == '15min' else time
        #     labels.append(label)
        #     data_point = float(price_info.get('1. open', 0))  # Default to 0 if '1. open' is not found
        #     data_points.append(data_point)


        except (TypeError, ValueError) as e:
            logging.error(f"Error processing data point {time}: {e}")
            continue
    return labels, data_points


@app.route('/recent-searches')
def recent_searches_page():
    # render recent_searches.html template with list of recent searches
    return render_template('recent_searches.html', searches=recent_searches)

if __name__ == '__main__':
    app.run(debug=True) #debug mode allows for further error logging in development
