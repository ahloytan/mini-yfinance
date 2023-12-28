import requests
import os

if os.getenv('ENV') == 'production':
    from .util import *
else:
    from util import *

financials_api_url = f'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/'

def get_income_statement_data(stock):
    total_revenue, income_statement_ttm, net_income_from_continuing_operations_ttm, net_income_from_operating_continuing_operations, exchange_rate = 0, 0, 0, 0, 1
    keys = ['annualOperatingRevenue', 'trailingNetIncomeFromContinuingOperationNetMinorityInterest', 'trailingOperatingRevenue', 'annualNetIncomeFromContinuingOperationNetMinorityInterest']
    hasCurrency = None
    params = generateParams(stock, keys, '1703494636')
    end_point = f"{financials_api_url}{stock}"
    response = requests.get(end_point, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()['timeseries']['result']
        hasCurrency = data[index_of_property_in_json(keys[0], data)][keys[0]][0]['currencyCode']
        if hasCurrency and hasCurrency != 'USD':
            exchange_rate = get_exchange_rate_to_usd(hasCurrency)

        total_revenue = {
            entry['asOfDate']: conversion(entry['reportedValue']['raw'], exchange_rate)
            for entry in data[index_of_property_in_json(keys[0], data)][keys[0]]
        }
        net_income_from_continuing_operations_ttm = conversion(data[index_of_property_in_json(keys[1], data)][keys[1]][0]['reportedValue']['raw'], exchange_rate)
        income_statement_ttm = conversion(data[index_of_property_in_json(keys[2], data)][keys[2]][0]['reportedValue']['raw'], exchange_rate)
        net_income_from_operating_continuing_operations = {
            entry['asOfDate']: conversion(entry['reportedValue']['raw'], exchange_rate)
            for entry in data[index_of_property_in_json(keys[3], data)][keys[3]]
        }

    return total_revenue, income_statement_ttm, net_income_from_continuing_operations_ttm, net_income_from_operating_continuing_operations, exchange_rate

def get_balance_sheet_data(stock, exchange_rate):
    cash_equivalent_and_short_term_investments = 0
    keys = ['quarterlyCashCashEquivalentsAndShortTermInvestments']
    params = generateParams(stock, keys, '1703510062')
    end_point = f"{financials_api_url}{stock}"
    response = requests.get(end_point, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()['timeseries']['result']
        cash_equivalent_and_short_term_investments = {
            entry['asOfDate']: conversion(entry['reportedValue']['raw'], exchange_rate)
            for entry in data[index_of_property_in_json(keys[0], data)][keys[0]]
        }
    return cash_equivalent_and_short_term_investments

def get_cash_flow_data(stock, exchange_rate):
    operating_cash_flow, operating_cash_flow_ttm, free_cash_flow, free_cash_flow_ttm = 0, 0, 0, 0
    keys = ['trailingFreeCashFlow','annualFreeCashFlow','annualOperatingCashFlow','trailingOperatingCashFlow']
    params = generateParams(stock, keys, '1703510062')
    end_point = f"{financials_api_url}{stock}"
    response = requests.get(end_point, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()['timeseries']['result']
        free_cash_flow_ttm = conversion(data[index_of_property_in_json(keys[0], data)][keys[0]][0]['reportedValue']['raw'], exchange_rate)
        free_cash_flow = {
            entry['asOfDate']: conversion(entry['reportedValue']['raw'], exchange_rate)
            for entry in data[index_of_property_in_json(keys[1], data)][keys[1]]
        }
        operating_cash_flow = {
            entry['asOfDate']: conversion(entry['reportedValue']['raw'], exchange_rate)
            for entry in data[index_of_property_in_json(keys[2], data)][keys[2]]
        }
        operating_cash_flow_ttm = conversion(data[index_of_property_in_json(keys[3], data)][keys[3]][0]['reportedValue']['raw'], exchange_rate)

    return operating_cash_flow, operating_cash_flow_ttm, free_cash_flow, free_cash_flow_ttm

def get_eps_next_5y(stock):
    eps_next_5y = '0%'
    end_point = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{stock}'
    params = {
        'formatted': 'true',
        'crumb': '1DOWVhBLaD.',
        'lang': 'en-US',
        'region': 'US',
        'modules': 'earningsTrend',
        'corsDomain': 'finance.yahoo.com',
    }
    
    response = requests.get(end_point, params=params, headers=headers)
    if response.status_code == 200:        
        eps_next_5y = response.json()['quoteSummary']['result'][0]['earningsTrend']['trend'][-2]['growth']['fmt']
        return eps_next_5y
    else:
        return jsonify({'error': f'Request failed with status code {response}'})

#https://www.reddit.com/r/Python/comments/vncw6d/what_is_the_best_library_for_website_scraping/