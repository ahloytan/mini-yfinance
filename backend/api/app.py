from flask_cors import CORS
from flask import Flask, jsonify, request
import yfinance as yf
#dev 
from util import convertToMillion
#prod
# from .util import convertToMillion
import finviz

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def health_check():
    return "ok"

@app.route('/yfinance_data', methods=['GET'])
def yfinance_data():
    stock = request.args.get('stock', default='AAPL')
    ticker = yf.Ticker(stock)

    #income statement
    quarterly_income_statement = convertToMillion(ticker.quarterly_income_stmt)
    annual_income_statement = convertToMillion(ticker.income_stmt)
    total_revenue = annual_income_statement.loc['Total Revenue'][::-1]
    income_statement_ttm = quarterly_income_statement.loc['Total Revenue'][:-1].sum()


    #balance sheet
    quarterly_balance_sheet = convertToMillion(ticker.quarterly_balance_sheet)
    cash_equivalent_and_short_term_investments = quarterly_balance_sheet.loc['Cash Cash Equivalents And Short Term Investments']
    try:
        current_debt = quarterly_balance_sheet.loc['Current Debt']
    except KeyError:
        current_debt = 0
    long_term_debt = quarterly_balance_sheet.loc['Long Term Debt']
    total_debt = current_debt + long_term_debt

    #cash flow
    quarterly_cash_flow = convertToMillion(ticker.quarterly_cash_flow)
    annual_cash_flow = convertToMillion(ticker.cash_flow)
    operating_cash_flow = annual_cash_flow.loc['Operating Cash Flow'][::-1]
    net_income_from_continuing_operations = annual_cash_flow.loc['Net Income From Continuing Operations'][::-1]
    free_cash_flow = annual_cash_flow.loc['Free Cash Flow'][::-1]

    operating_cash_flow_ttm = quarterly_cash_flow.loc['Operating Cash Flow'][:-1].sum()
    net_income_from_continuing_operations_ttm = quarterly_cash_flow.loc['Net Income From Continuing Operations'][:-1].sum()
    free_cash_flow_ttm = quarterly_cash_flow.loc['Free Cash Flow'][:-1].sum()

    data = {
        'fullName': ticker.info["longName"],
        'totalRevenue': total_revenue.to_json(),
        'incomeStatementTTM': income_statement_ttm,
        'cashEquivalentAndShortTermInvestments': cash_equivalent_and_short_term_investments.to_json(),
        'totalDebt': total_debt.to_json(),
        'operatingCashFlow': operating_cash_flow.to_json(),
        'netIncomeFromContinuingOperations': net_income_from_continuing_operations.to_json(),
        'freeCashFlow': free_cash_flow.to_json(),
        'operatingCashFlowTTM': operating_cash_flow_ttm,
        'netIncomeFromContinuingOperationsTTM': net_income_from_continuing_operations_ttm,
        'freeCashFlowTTM': free_cash_flow_ttm,
    }

    return jsonify({"code": 200, "data": data}), 200

@app.route('/finviz_data', methods=['GET'])
def finviz_data():
    stock = request.args.get('stock', default='AAPL')

    finviz_data = finviz.get_stock(stock)
    peg = finviz_data['PEG']
    current_ratio = finviz_data['Current Ratio']
    roe = finviz_data['ROE']
    eps_next_5y = finviz_data['EPS next 5Y']
    beta = finviz_data['Beta']
    shs_outstanding = finviz_data['Shs Outstand']

    data = {
        'peg': peg,
        'currentRatio': current_ratio,
        'roe': roe,
        'epsNext5Y': eps_next_5y,
        'beta': beta,
        'shsOutstanding': shs_outstanding
    }

    return jsonify({"code": 200, "data": data}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)