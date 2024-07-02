import os
import requests #HTTP Library 
import logging #Logging package for Python; based on PEP 282
#Getting the API Key from environment variable
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
#base url for Alpha Vantage API
BASE_URL = 'https://www.alphavantage.co/query'

def get_stock_data(symbol, interval='15min', outputsize='compact'):

    """
        fetches stock data for given symbol from Alpha Vantage API

    
    Parameters:
        symbol: stock ticker symbol (e.g. NFLX for Netflix)
        interval: interval between data points (1min 5min, 15min, 30min, 60min)
        outputsize: amount of data to return ('compact', 'full'), compact returns latest 100 data points
                    in the intraday time series; full returns trailing 30 days of the most recent intraday data

    See more: https://www.alphavantage.co/documentation/
    Returns:
        dictionary: containing stock data 
    """
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol, #symbol from the function definition parameters
        'interval': interval, #interval from function definition parameters
        'apikey': API_KEY, #API Key from environment
        'outputsize': outputsize #output size from function definition parameters
    }

    try:
        response = requests.get(BASE_URL, params=params) #make API request through get method; URL request for new params object
        response.raise_for_status() #raise an HTTPError if request was unsuccessful
        data = response.json() #parse JSON response from Get Request
        logging.log(data) #read parsed data information (for testing purposes only)
        time_series_key = f'Time Series ({interval})' #key has access to time series data
        if time_series_key in data: #check if key exists in response data
            return data[time_series_key]
        else:
            return {'error': 'Error fetching data'}
    except requests.exceptions.RequestException as e: #log errors if any occurred upon request failure, plus the reason
        logging.error(f"Request failed: {e}")
        return {'error': 'Request failed'}
