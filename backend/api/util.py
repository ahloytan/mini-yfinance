import requests
from bs4 import BeautifulSoup
from flask import jsonify

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',      
    'Accept': 'application/json',
    'Cookie': 'gam_id=y-TjEDJPZE2uK4i9QlUnuBYCL0ic4L15gV~A; tbla_id=ae1c33c9-968b-4267-acf9-8d840d8251a1-tuctbc9f210; GUC=AQEBCAFliYBltEIeiQSX&s=AQAAAH7EZOHq&g=ZYgwYg; A1=d=AQABBCVi3WACEIUwHsGub3w6lx5fuudrkAsFEgEBCAGAiWW0Za-0b2UB_eMBAAcIJWLdYOdrkAs&S=AQAAAhJfv3S_GzYP5xLa4zsXGW4; A3=d=AQABBCVi3WACEIUwHsGub3w6lx5fuudrkAsFEgEBCAGAiWW0Za-0b2UB_eMBAAcIJWLdYOdrkAs&S=AQAAAhJfv3S_GzYP5xLa4zsXGW4; gpp=DBAA; gpp_sid=-1; axids=gam=y-TjEDJPZE2uK4i9QlUnuBYCL0ic4L15gV~A&dv360=eS1uRzhBUjVaRTJ1RTBabUt6OWdjeDZwRmJhdG5NZ0UyMn5B&ydsp=y-Y2zOWI5E2uLK1Zgb88WuWLWVD3l.xMMh~A; cmp=t=1703656357&j=0&u=1---; PRF=t%3DAMD%252BAAPL%252BBABA%252BTCEHY%26newChartbetateaser%3D0%252C1704775172404; A1S=d=AQABBCVi3WACEIUwHsGub3w6lx5fuudrkAsFEgEBCAGAiWW0Za-0b2UB_eMBAAcIJWLdYOdrkAs&S=AQAAAhJfv3S_GzYP5xLa4zsXGW4&j=WORLD'
}

def conversion(value, rate):
    million = 1000000
    return value / rate / million

def get_exchange_rate_to_usd(currency):
    try:
        response = requests.get(f'https://api.ofx.com/PublicSite.ApiService/OFX/spotrate/Individual/USD/{currency}/1')
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

def generateParams(stock, keys, period2Value):
    return {
        'lang': 'en-US',
        'region': 'US',
        'symbol': stock,
        'padTimeSeries': 'true',
        'merge': 'false',
        'type': ','.join(keys),
        'period1': '493590046',
        'period2': period2Value,
        'corsDomain': 'finance.yahoo.com',
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