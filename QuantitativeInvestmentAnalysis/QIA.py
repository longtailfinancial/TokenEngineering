import panel as pn
import pandas as pd
import numpy as np
import hvplot.pandas
import holoviews as hv
import param as pm 
import random
import math


class TimeValueMoney(pm.Parameterized):
    real_risk_free_interest_rate = pm.Number(
        30, bounds=(0, 100), step=1, precedence=1
        doc="""The rrfir is the single-period interest rate for a completely
            risk-free security if no inflation were expected. In economic theory,
            the real risk-free rate reflects the time preferences of individuals
            for current versus future real consumption."""
    )
    inflation_premium = pm.Number(30, bounds=(0, 100), step=1, precedence=1)
    default_risk_premium = pm.Number(30, bounds=(0, 100), step=1, precedence=1)
    liquidity_premium = pm.Number(30, bounds=(0, 100), step=1, precedence=1)
    maturity_premium = pm.Number(30, bounds=(0, 100), step=1, precedence=1)


    # r= real_risk_free_interest_rate + inflation_premium + default_risk_premium



if __name__ == "__main__":
    tvm = TimeValueMoney()
    pane = pn.Pane(tvm)
    pane.app('localhost:8888')
