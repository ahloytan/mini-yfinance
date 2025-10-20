import datetime
import requests
from bs4 import BeautifulSoup
import os

if os.getenv('ENV') == 'production':
    from .variables import *
else:
    from variables import *


def conversion(value, rate):
    million = 1000000
    return value / rate / million

def get_exchange_rate_to_usd(currency):
    try:
        response = requests.get(f'{ofx_api_url}{currency}/1')
        data = response.json()

        return data['InterbankAmount']
    except requests.exceptions.RequestException as e:
        return ''

def is_float(string):
    try:
        float_value = float(string)
        return float_value
    except ValueError:
        return 0

def index_of_property_in_json(property, json):
    return next((i for i, d in enumerate(json) if property in d), None)

def generate_params(stock, keys):
    now = datetime.datetime.now()

    start_timestamp = int((now - datetime.timedelta(days=365*5)).timestamp())
    end_timestamp = int(now.timestamp())

    return {
        'lang': 'en-US',
        'region': 'US',
        'symbol': stock,
        'padTimeSeries': 'true',
        'merge': 'false',
        'type': ','.join(keys),
        'period1': start_timestamp,
        'period2': end_timestamp,
        'corsDomain': 'finance.yahoo.com',
    }
def generate_search_params(query):

    #Most of the query params are not needed
    return {
        'q': query,
        'lang': 'en-SG',
        'region': 'SG',
        'quotesCount': 10,
        'newsCount': 0,
        'listsCount': 0,
        'enableFuzzyQuery': 'false',
        'quotesQueryId': 'tss_match_phrase_query',
        'multiQuoteQueryId': 'multi_quote_single_token_query',
        'newsQueryId': 'news_cie_vespa',
        'enableCb': 'false',
        'enableNavLinks': 'false',
        'enableEnhancedTrivialQuery': 'true',
        'enableResearchReports': 'false',
        'enableCulturalAssets': 'true',
        'enableLogoUrl': 'true',
        'enableLists': 'false',
        'recommendCount': 10,
        'enableCccBoost': 'true'
    }

def extract_data(data, key, index, exchange_rate):
    if index is None:
        return {}
    else:
        return {
            entry['asOfDate']: conversion(entry['reportedValue']['raw'], exchange_rate)
            for entry in data[index][key] if entry
        }

#v0 methods
def get_soup(url):
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.content, 'html.parser')

def get_currency(soup):
    currency = soup.select('.Fz\(xs\) span')[-2].text
    if 'Currency in' in currency:
        return currency.split('.')[0][-3:]
    
    return ''

def get_soup_cash_flow_level1_processor_and_currency(url, ticker):
    soup = get_soup(url.format(ticker=ticker))
    table = soup.select_one('.BdT')
    all_data = []
            
    currency = get_currency(soup)
    for row in table.select('.D\(tbr\)'):
        data = [cell.text for cell in row.select('.Ta\(c\), .Ta\(start\)')]
        all_data.append(data)

    return all_data, currency

def get_soup_income_statement_processor(url, ticker):
    soup = get_soup(url.format(ticker=ticker))
    table = soup.select_one('.BdT')

    all_data = []
    for row in table.select('.D\(tbr\)'):
        data = [cell.text for cell in row.select('.Ta\(c\), .Ta\(start\)')]
        all_data.append(data)

        if data[0] == 'Net Income Common Stockholders':
            return all_data
        
    return all_data 

def get_soup_fcf_growth_rate(stock):
    url = f'https://sg.finance.yahoo.com/quote/{stock}/analysis?p={stock}'
    soup = get_soup(url.format(ticker=stock))
    res = soup.select('.Ta\(end\).Py\(10px\)')
    return res[-8].text

def process_yfinance_scraped_value(value):
    if isinstance(value, float):
        return value * 1000

    return int(value.replace(',', '')) * 1000