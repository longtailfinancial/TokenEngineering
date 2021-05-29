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
    ir = InterestRate()
    pane = pn.Column(ir, "Interest Rate:", ir.interest_rate)
    return pane


