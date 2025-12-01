import yfinance as yf
import pandas as pd
import streamlit as st

def get_financials(ticker):
    stock = yf.Ticker(ticker)
    bs = stock.balance_sheet
    inc = stock.income_stmt
    cf = stock.cashflow
    return bs, inc, cf

def calculate_ratios(bs, inc, cf):
    latest_bs = bs.iloc[:, 0]
    latest_inc = inc.iloc[:, 0]
    latest_cf = cf.iloc[:, 0]

    ratios = {}

    # Activity ratios
    ratios['Inventory Turnover'] = latest_inc.get('Cost Of Revenue', 0) / latest_bs.get('Inventory', 1)
    ratios['Days Sales Outstanding'] = latest_inc.get('Operating Revenue', 0) / latest_bs.get('Net Receivables', 1) * 365
    ratios['Payables Period'] = latest_inc.get('Cost Of Revenue', 0) / latest_bs.get('Accounts Payable', 1) * 365
    ratios['Cash Conversion Cycle'] = ratios['Days Sales Outstanding'] + \
                                      (365 / ratios['Inventory Turnover']) - ratios['Payables Period']

    # Liquidity
    ratios['Current Ratio'] = latest_bs.get('Current Assets', 0) / latest_bs.get('Current Liabilities', 1)
    ratios['Quick Ratio'] = (latest_bs.get('Current Assets', 0) - latest_bs.get('Inventory', 0)) / latest_bs.get('Current Liabilities', 1)
    ratios['Cash Ratio'] = latest_bs.get('Cash And Cash Equivalents', 0) / latest_bs.get('Current Liabilities', 1)

    # Solvency
    ratios['Debt to Equity'] = latest_bs.get('Total Debt', 0) / latest_bs.get('Stockholders Equity', 1)
    ratios['Interest Coverage'] = latest_inc.get('EBIT', 0) / latest_inc.get('Interest Expense', 1)

    # Profitability
    ratios['Gross Margin %'] = latest_inc.get('Gross Profit', 0) / latest_inc.get('Operating Revenue', 0) * 100
    ratios['Operating Margin %'] = latest_inc.get('Operating Income', 0) / latest_inc.get('Operating Revenue', 0) * 100
    ratios['Net Profit Margin %'] = latest_inc.get('Net Income', 0) / latest_inc.get('Operating Revenue', 0) * 100
    ratios['ROA %'] = latest_inc.get('Net Income', 0) / latest_bs.get('Total Assets', 0) * 100
    ratios['ROE %'] = latest_inc.get('Net Income', 0) / latest_bs.get('Stockholders Equity', 0) * 100

    # DuPont 5-part
    ratios['DuPont ROE'] = (latest_inc.get('Net Income', 0) / latest_inc.get('Operating Revenue', 0)) * \
                           (latest_inc.get('Operating Revenue', 0) / latest_bs.get('Total Assets', 0)) * \
                           (latest_inc.get('EBIT', 0) / latest_inc.get('Operating Revenue', 0)) * \
                           (latest_inc.get('Net Income', 0) / latest_inc.get('EBIT', 0)) * \
                           (latest_bs.get('Total Assets', 0) / latest_bs.get('Stockholders Equity', 0))

    # Altman Z-Score (1968 original)
    ratios['Altman Z-Score'] = 1.2 * (latest_bs.get('Working Capital', 0) / latest_bs.get('Total Assets', 0)) + \
                               1.4 * (latest_bs.get('Retained Earnings', 0) / latest_bs.get('Total Assets', 0)) + \
                               3.3 * (latest_inc.get('EBIT', 0) / latest_bs.get('Total Assets', 0)) + \
                               0.6 * (latest_bs.get('Stockholders Equity', 0) / latest_bs.get('Total Liabilities', 0)) + \
                               1.0 * (latest_inc.get('Operating Revenue', 0) / latest_bs.get('Total Assets', 0))

    return pd.Series(ratios).round(3)
