import requests
import os
from flask import jsonify

if os.getenv('ENV') == 'production':
    from .util import conversion, get_exchange_rate_to_usd, index_of_property_in_json, generateParams
    from .variables import *
else:
    from util import *
    from variables import *

def get_company_name_and_last_close(stock):
    keys = ['longName', 'shortName', 'regularMarketPrice']
    params = {
        'formatted': 'true',
        'crumb': '1DOWVhBLaD.',
        'lang': 'en-US',
        'region': 'US',
        'fields': ','.join(keys),
        'symbols': stock,
        'corsDomain': 'finance.yahoo.com',
    }
    response = requests.get(summary_api_url, params=params, headers=headers)
    if response.status_code == 200:
        full_name = response.json()['quoteResponse']['result'][0]['longName']
        last_close = response.json()['quoteResponse']['result'][0]['regularMarketPrice']['raw']
        return full_name, last_close
    
    return 'Error Retrieving Name'

def get_income_statement_data(stock):
    total_revenue, income_statement_ttm, net_income_from_continuing_operations_ttm, net_income_from_operating_continuing_operations, exchange_rate = 0, 0, 0, 0, 1
    keys = ['annualOperatingRevenue', 'trailingNetIncomeFromContinuingOperationNetMinorityInterest', 'trailingOperatingRevenue', 'annualNetIncomeFromContinuingOperationNetMinorityInterest']
    hasCurrency = None
    params = generateParams(stock, keys)
    end_point = f"{financials_api_url}{stock}"
    response = requests.get(end_point, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()['timeseries']['result']
        hasCurrency = data[index_of_property_in_json(keys[0], data)][keys[0]][0]['currencyCode']
        if hasCurrency and hasCurrency != 'USD':
            exchange_rate = get_exchange_rate_to_usd(hasCurrency)

        total_revenue = extract_data(data, keys[0], index_of_property_in_json(keys[0], data), exchange_rate)

        net_income_from_continuing_operations_ttm = conversion(data[index_of_property_in_json(keys[1], data)][keys[1]][0]['reportedValue']['raw'], exchange_rate)

        income_statement_ttm = conversion(data[index_of_property_in_json(keys[2], data)][keys[2]][0]['reportedValue']['raw'], exchange_rate)

        net_income_from_operating_continuing_operations = extract_data(data, keys[3], index_of_property_in_json(keys[3], data), exchange_rate)

    return total_revenue, income_statement_ttm, net_income_from_continuing_operations_ttm, net_income_from_operating_continuing_operations, exchange_rate

def get_balance_sheet_data(stock, exchange_rate):
    cash_equivalent_and_short_term_investments = 0
    keys = ['quarterlyCashCashEquivalentsAndShortTermInvestments', 'quarterlyLongTermDebt', 'quarterlyCurrentDebtAndCapitalLeaseObligation']
    params = generateParams(stock, keys)
    end_point = f"{financials_api_url}{stock}"
    response = requests.get(end_point, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()['timeseries']['result']

        cash_equivalent_and_short_term_investments = extract_data(data, keys[0], index_of_property_in_json(keys[0], data), exchange_rate)

        #debt
        quarterly_long_term_debt = extract_data(data, keys[1], index_of_property_in_json(keys[1], data), exchange_rate)
        quarterly_current_debt = extract_data(data, keys[2], index_of_property_in_json(keys[2], data), exchange_rate)

        total_debt = {
            key: quarterly_long_term_debt[key] + quarterly_current_debt.get(key, 0)
            for key in quarterly_long_term_debt
        }

    return cash_equivalent_and_short_term_investments, total_debt

def get_cash_flow_data(stock, exchange_rate):
    operating_cash_flow, operating_cash_flow_ttm, free_cash_flow, free_cash_flow_ttm = 0, 0, 0, 0
    keys = ['trailingFreeCashFlow','annualFreeCashFlow','annualOperatingCashFlow','trailingOperatingCashFlow']
    params = generateParams(stock, keys)
    end_point = f"{financials_api_url}{stock}"
    response = requests.get(end_point, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()['timeseries']['result']
        free_cash_flow_ttm = conversion(data[index_of_property_in_json(keys[0], data)][keys[0]][0]['reportedValue']['raw'], exchange_rate)
        free_cash_flow = extract_data(data, keys[1], index_of_property_in_json(keys[1], data), exchange_rate)

        operating_cash_flow = extract_data(data, keys[2], index_of_property_in_json(keys[2], data), exchange_rate)
        operating_cash_flow_ttm = conversion(data[index_of_property_in_json(keys[3], data)][keys[3]][0]['reportedValue']['raw'], exchange_rate)

    return operating_cash_flow, operating_cash_flow_ttm, free_cash_flow, free_cash_flow_ttm

def get_eps_next_5y(stock):
    eps_next_5y = '0%'
    end_point = f'{eps_api_url}{stock}'
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
        eps_next_5y = response.json()['quoteSummary']['result'][0]['earningsTrend']['trend'][-2]['growth'].get('fmt', "0%")
        return eps_next_5y
    else:
        return jsonify({'error': f'Request failed with status code {response}'})

#https://www.reddit.com/r/Python/comments/vncw6d/what_is_the_best_library_for_website_scraping/