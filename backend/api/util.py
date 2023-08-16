import requests
import pandas as pd
from bs4 import BeautifulSoup

def convertToMillion(value):
    million = 1000000
    return value / million

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'}

def get_soup(url):
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.content, 'html.parser')

def get_soup_cash_flow_level1_processor(url, ticker):
    soup = get_soup(url.format(ticker=ticker))
    table = soup.select_one('.BdT')
    all_data = []
    for row in table.select('.D\(tbr\)'):
        data = [cell.text for cell in row.select('.Ta\(c\), .Ta\(start\)')]
        all_data.append(data)

    return all_data

def get_soup_income_statement_processor(url, ticker):
    soup = get_soup(url.format(ticker=ticker))

    table = soup.select_one('.BdT')
    for row in table.select('.D\(tbr\)'):
        data = [cell.text for cell in row.select('.Ta\(c\), .Ta\(start\)')]

        if data[0] == 'Total Revenue':
            return data

    return []

def processYFinanceScrapedValue(value):
    return int(value.replace(',', '')) * 1000