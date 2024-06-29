# stock_data.py
import os
import requests
import logging

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

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        time_series_key = f'Time Series ({interval})'
        if time_series_key in data:
            return data[time_series_key]
        else:
            return {'error': 'Error fetching data'}
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return {'error': 'Request failed'}
