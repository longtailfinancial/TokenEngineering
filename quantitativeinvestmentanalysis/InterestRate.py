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


# Chapter 1 The Time Value of Money


class InterestRate(pm.Parameterized):
    """
    Interest rate r is a rate of return that reflects the relationship between
    differently dated cash flows. If $9,500 today and $10,000 one year from now
    are equivilent, then the interest rate is $500/$9,500 = 5.62%.
    """

    real_risk_free_interest_rate = pm.Number(
        0.01,
        bounds=(0, 1),
        step=0.01,
        precedence=1,
        doc="""The real risk free interest rate is the single-period interest rate for a completely risk-free
            security if no inflation were expected. In economic theory, the real
            risk-free rate reflects the time preferences of individuals for current
            versus future real consumption.""",
    )
    inflation_premium = pm.Number(
        0,
        step=0.01,
        precedence=1,
        doc="""The inflation premium compensates investors for expected
            inflation and reflects the average inflation rate expected over the
            maturity of the debt. Inflation reduces the purchasing power of a unit
            of currency - the amount of goods and services one can buy with it.""",
    )
    default_risk_premium = pm.Number(
        0,
        bounds=(0, 1),
        step=0.01,
        precedence=1,
        doc="""The default risk premium compensates investors for the
        possibility that the borrower will fail to make a promised payment at
        the contracted time and in the contracted amount.""",
    )
    liquidity_premium = pm.Number(
        0,
        bounds=(0, 1),
        step=0.01,
        precedence=1,
        doc="""The Liquidity Premium compensates investors for the risk of loss
        relative to an investment's fair value if the investment needs to be
        converted to cash quickly. US Treasury Bills do not bear a liquidity
        premium because large amounts can be bought and sold without affecting
        their market price. Many bonds of small issuers, by contrast, trade
        infrequently after they are issued; the interest rate on such bonds
        includes a liquidity premium reflecting the relatively high
        costs(including the impac on price) of selling a position.""",
    )

    maturity_premium = pm.Number(
        0,
        bounds=(0, 1),
        step=0.01,
        precedence=1,
        doc="""The maturity premium compensates investors for the increased
        sensitivity to the market value of debt to a change in market interest
        rates as maturity is extended, in general (holding all else equal). The
        difference between the interest rate on longer-maturity, liquid
        Treasury debt and that on short-term Treasury debt reflects a positive
        maturity premium for the longer-term debt.""",
    )

    def nominal_risk_free_interest_rate(self):
        """
        The sum of the real risk-free interest rate and the inflation premium.
        """
        return self.real_risk_free_interest_rate + self.inflation_premium

    def interest_rate(self):
        return (
            self.nominal_risk_free_interest_rate()
            + self.default_risk_premium
            + self.liquidity_premium
            + self.maturity_premium
        )
