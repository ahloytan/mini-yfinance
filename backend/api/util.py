import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'}

def get_soup(url):
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.content, 'html.parser')

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

def get_currency(soup):
    currency = soup.select('.Fz\(xs\) span')[-2].text
    if 'Currency in' in currency:
        return currency.split('.')[0][-3:]
    
    return ''

def process_yfinance_scraped_value(value):
    return int(value.replace(',', '')) * 1000

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
    

def get_soup_fcf_growth_rate(stock):
    url = f'https://sg.finance.yahoo.com/quote/{stock}/analysis?p={stock}'
    soup = get_soup(url.format(ticker=stock))
    res = soup.select('.Ta\(end\).Py\(10px\)')
    return res[-8].text
