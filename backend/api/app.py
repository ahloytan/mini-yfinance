from flask_cors import CORS
from flask import Flask, jsonify, request
import yfinance as yf
from finvizfinance.quote import finvizfinance

#dev 
from util import *
#prod
# from .util import *

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def health_check():
    return "ok"

@app.route('/yfinance_data', methods=['GET'])
def yfinance_data():
    stock = request.args.get('stock', default='AAPL')
    ticker = yf.Ticker(stock)

    last_close = ticker.history()['Close'].iloc[-1]
    exchange_rate = 1

    eps_next_5y = get_soup_fcf_growth_rate(stock)

    yahoo_url = 'https://finance.yahoo.com/quote'

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
    total_debt = current_debt + long_term_debt

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

    data = {
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

@app.route('/finviz_data', methods=['GET'])
def finviz_data():
    stock = request.args.get('stock', default='AAPL')

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

@app.route('/get_fcf_growth_rate_yr_1_to_5', methods=['GET'])
def get_fcf_growth_rate_yr_1_to_5():
    stock = request.args.get('stock', default='AAPL')
    get_soup_fcf_growth_rate(stock)


if __name__ == '__main__':
    app.run(debug=True, port=5000)