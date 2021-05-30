"""
This module is an implementation of the book Quantitative Investment Analysis, DeFusco, McLeavey, Pinto, Runkle, Second Edition, CFA Institute Investment Series, Wiley Publishing.
You can find the 3rd edition of this book available here: https://www.wiley.com/en-gb/Quantitative+Investment+Analysis%2C+3rd+Edition-p-9781119104599
"""


import panel as pn
import pandas as pd
import numpy as np
import hvplot.pandas
import holoviews as hv
import param as pm 
import random
import math

from quantitativeinvestmentanalysis.qia import InterestRate
def test_interest_rate_view():
    params = {
        'real_risk_free_interest_rate': 0,
        'inflation_premium': 0,
        'default_risk_premium': 0,
        'liquidity_premium': 0,
        'maturity_premium': 0,
    }

    r = InterestRate(**params)
    pane = pn.Column(r, "Interest Rate:", r.interest_rate)
    return pane


from quantitativeinvestmentanalysis.qia import CompoundingCashFlow
def test_compounding_cash_flow():
    r = InterestRate(real_risk_free_interest_rate=0.08)
    c = CompoundingCashFlow(r, present_value=10000, compound_periods=4, N=2)
    assert c.future_lump_value() - 11716.59 < 0.1


from quantitativeinvestmentanalysis.qia import CashFlow
def test_present_value_annuity():
    params = {
        'real_risk_free_interest_rate': 0.07,
        'inflation_premium': 0,
        'default_risk_premium': 0,
        'liquidity_premium': 0,
        'maturity_premium': 0,
    }
    r = InterestRate(**params)
    cashflow = CashFlow(r, annuity=20000, N=19)
    assert cashflow.present_annuity_value() - 2267119.05 < 0.1

