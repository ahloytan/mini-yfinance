from flask_cors import CORS
from flask import Flask, jsonify, request
from finvizfinance.quote import finvizfinance
import os
import json
from timeit import default_timer as timer
from concurrent.futures import ThreadPoolExecutor

if os.getenv('ENV') == 'production':
    from .util import conversion, is_float
    from .methods import *
    from .variables import yahoo_url, default_stock
else:
    import yfinance as yf
    from util import *
    from methods import *
    from variables import yahoo_url, default_stock

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def health_check():
    return "ok"

@app.route('/yfinance_data', methods=['GET'])
def yfinance_data():
    try:
        start = timer()
        stock = request.args.get('stock', default=default_stock)

        #company name
        full_name, last_close = get_company_name_and_last_close(stock)

        #eps
        eps_next_5y = get_eps_next_5y(stock)

        with ThreadPoolExecutor(max_workers=3) as executor:
            try:
                #income statement
                total_revenue, income_statement_ttm, net_income_from_continuing_operations_ttm, net_income_from_operating_continuing_operations = executor.submit(get_income_statement_data, stock).result()

                #balance sheet                
                cash_equivalent_and_short_term_investments, total_debt = executor.submit(get_balance_sheet_data, stock).result()
                
                #cash flow         
                operating_cash_flow, operating_cash_flow_ttm, free_cash_flow, free_cash_flow_ttm = executor.submit(get_cash_flow_data, stock).result()

            except Exception as e:
                print(f"Error type: {type(e).__name__}")
                print(f"Error message: {str(e)}")
                return jsonify({'error': 'Financials not found for this ticker'}), 500   
            
        end = timer()
        data = {
            'timeTaken': end-start,
            'epsNext5Y': float(eps_next_5y[:-1]),
            'lastClose': round(last_close, 2),
            'fullName': full_name,
            'totalRevenue': json.dumps(total_revenue),
            'incomeStatementTTM': round(income_statement_ttm, 2),
            'cashEquivalentAndShortTermInvestments': json.dumps(cash_equivalent_and_short_term_investments),
            'totalDebt': json.dumps(total_debt), #Total debt is calculated using Current Debt + Long Term Debt (excluding Long Term Capital Lease Obligation)
            'operatingCashFlow': json.dumps(operating_cash_flow),
            'netIncomeFromContinuingOperations': json.dumps(net_income_from_operating_continuing_operations),
            'freeCashFlow': json.dumps(free_cash_flow),
            'operatingCashFlowTTM': round(operating_cash_flow_ttm, 2),
            'netIncomeFromContinuingOperationsTTM': round(net_income_from_continuing_operations_ttm, 2),
            'freeCashFlowTTM': round(free_cash_flow_ttm, 2)
        }

        return jsonify({"code": 200, "data": data}), 200
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500   

@app.route('/finviz_data', methods=['GET'])
def finviz_data():
    try: 
        stock = request.args.get('stock', default=default_stock)

        finviz_finance_data = finvizfinance(stock).ticker_fundament()

        peg = finviz_finance_data['PEG']
        current_ratio = finviz_finance_data['Current Ratio']
        roe = finviz_finance_data['ROE']
        eps_next_5y = finviz_finance_data['EPS next 5Y']
        beta = finviz_finance_data['Beta']
        shs_outstanding = finviz_finance_data['Shs Outstand']

        data = {
            'peg': peg,
            'currentRatio': current_ratio,
            'roe': roe,
            'epsNext5Y': is_float(eps_next_5y[:-1]),
            'beta': float(beta[:-1]),
            'shsOutstanding': shs_outstanding
        }

        return jsonify({"code": 200, "data": data}), 200
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500       

@app.route('/yfinance_data_v0', methods=['GET'])
def yfinance_data_v0():
    try: 
        start = timer()
        
        stock = request.args.get('stock', default=default_stock)
        ticker = yf.Ticker(stock)

        last_close = ticker.history()['Close'].iloc[-1]
        exchange_rate = 1

        eps_next_5y = get_soup_fcf_growth_rate(stock)
        
        #income statement
        quarterly_income_statement = conversion(ticker.quarterly_income_stmt, exchange_rate)
        annual_income_statement = conversion(ticker.income_stmt, exchange_rate)
        total_revenue = annual_income_statement.loc['Total Revenue'][::-1]
        income_statement_scraped = get_soup_income_statement_processor(f'{yahoo_url}/{stock}/financials?p={stock}', ticker)
        income_statement_ttm = income_statement_scraped[1][1] if income_statement_scraped else quarterly_income_statement.loc['Total Revenue'][:-1].sum()
        income_statement_ttm = conversion(process_yfinance_scraped_value(income_statement_ttm), exchange_rate)

        #balance sheet
        quarterly_balance_sheet = conversion(ticker.quarterly_balance_sheet, exchange_rate)
        cash_equivalent_and_short_term_investments = quarterly_balance_sheet.loc['Cash Cash Equivalents And Short Term Investments']

        try:
            current_debt = quarterly_balance_sheet.loc['Current Debt']
        except KeyError:
            current_debt = 0
        long_term_debt = quarterly_balance_sheet.loc['Long Term Debt']
        total_debt = current_debt.add(long_term_debt, fill_value=0)

        #cash flow
        quarterly_cash_flow = conversion(ticker.quarterly_cash_flow, exchange_rate)
        annual_cash_flow = conversion(ticker.cash_flow, exchange_rate)
        operating_cash_flow = annual_cash_flow.loc['Operating Cash Flow'][::-1]
        net_income_from_continuing_operations = annual_cash_flow.loc['Net Income From Continuing Operations'][::-1]
        free_cash_flow = annual_cash_flow.loc['Free Cash Flow'][::-1]

        cash_flow_scraped_l1, hasCurrency = get_soup_cash_flow_level1_processor_and_currency(f'{yahoo_url}/{stock}/cash-flow?p={stock}', ticker)

        #Currency
        if hasCurrency:
            exchange_rate = get_exchange_rate_to_usd(hasCurrency)

        operating_cash_flow_ttm = cash_flow_scraped_l1[1][1] if cash_flow_scraped_l1 else quarterly_cash_flow.loc['Operating Cash Flow'][:-1].sum()
        operating_cash_flow_ttm = conversion(process_yfinance_scraped_value(operating_cash_flow_ttm), exchange_rate)

        net_income_from_continuing_operations_ttm = income_statement_scraped[-1][1] if income_statement_scraped else quarterly_cash_flow.loc['Net Income From Continuing Operations'][:-1].sum()
        net_income_from_continuing_operations_ttm = conversion(process_yfinance_scraped_value(net_income_from_continuing_operations_ttm), exchange_rate)
        free_cash_flow_ttm = cash_flow_scraped_l1[-1][1] if cash_flow_scraped_l1 else quarterly_cash_flow.loc['Free Cash Flow'][:-1].sum()
        free_cash_flow_ttm = conversion(process_yfinance_scraped_value(free_cash_flow_ttm), exchange_rate)
        end = timer()
        data = {
            'timeTaken': end-start,
            'epsNext5Y': float(eps_next_5y[:-1]),
            'lastClose': round(last_close, 2),
            # 'fullName': ticker.info["longName"], //.info currently not working because yahoo API end point change. Waiting for fix https://github.com/ranaroussi/yfinance/issues/1729#issuecomment-1793803181
            'fullName': finvizfinance(stock).ticker_fundament()['Company'],
            'totalRevenue': total_revenue.to_json(),
            'incomeStatementTTM': round(income_statement_ttm, 2),
            'cashEquivalentAndShortTermInvestments': cash_equivalent_and_short_term_investments.to_json(),
            'totalDebt': total_debt.to_json(),
            'operatingCashFlow': operating_cash_flow.to_json(),
            'netIncomeFromContinuingOperations': net_income_from_continuing_operations.to_json(),
            'freeCashFlow': free_cash_flow.to_json(),
            'operatingCashFlowTTM': round(operating_cash_flow_ttm, 2),
            'netIncomeFromContinuingOperationsTTM': round(net_income_from_continuing_operations_ttm, 2),
            'freeCashFlowTTM': round(free_cash_flow_ttm, 2),
        }

        return jsonify({"code": 200, "data": data}), 200
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500       

@app.route('/get_fcf_growth_rate_yr_1_to_5', methods=['GET'])
def get_fcf_growth_rate_yr_1_to_5():
    stock = request.args.get('stock', default=default_stock)
    get_soup_fcf_growth_rate(stock)

@app.route('/search', methods=['GET'])
def search_tickers():
    query = request.args.get('query')
    response = get_suggested_stocks(query)

    return jsonify({"code": 200, "data": response['quotes']}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)