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
        0.01, bounds=(0, 1), step=0.01, precedence=1,
        doc="""The real risk free interest rate is the single-period interest rate for a completely risk-free
            security if no inflation were expected. In economic theory, the real
            risk-free rate reflects the time preferences of individuals for current
            versus future real consumption.""",
    )
    inflation_premium = pm.Number(
        0, bounds=(0, 1), step=0.01, precedence=1,
        doc="""The inflation premium compensates investors for expected
            inflation and reflects the average inflation rate expected over the
            maturity of the debt. Inflation reduces the purchasing power of a unit
            of currency - the amount of goods and services one can buy with it.""",
    )
    default_risk_premium = pm.Number(
        0, bounds=(0, 1), step=0.01, precedence=1,
        doc="""The default risk premium compensates investors for the
        possibility that the borrower will fail to make a promised payment at
        the contracted time and in the contracted amount.""",
    )
    liquidity_premium = pm.Number(
        0, bounds=(0, 1), step=0.01, precedence=1,
        doc="""The Liquidity Premium compensates investors for the risk of loss
        relative to an investment's fair value if the investment needs to be
        converted to cash quickly. US Treasury Bills do not bear a liquidity
        premium because large amounts can be bought and sold without affecting
        their market price. Many bonds of small issuers, by contrast, trade
        infrequently after they are issued; the interest rate on such bonds
        includes a liquidity premium reflecting the relatively high
        costs(including the impac on price) of selling a position.""")

    maturity_premium = pm.Number(
        0, bounds=(0, 1), step=0.01, precedence=1,
        doc="""The maturity premium compensates investors for the increased
        sensitivity to the market value of debt to a change in market interest
        rates as maturity is extended, in general (holding all else equal). The
        difference between the interest rate on longer-maturity, liquid
        Treasury debt and that on short-term Treasury debt reflects a positive
        maturity premium for the longer-term debt.""")

    def nominal_risk_free_interest_rate(self):
        """
        The sum of the real risk-free interest rate and the inflation premium.
        """
        return self.real_risk_free_interest_rate + self.inflation_premium

    def interest_rate(self):
        return self.nominal_risk_free_interest_rate() + self.default_risk_premium + self.liquidity_premium + self.maturity_premium


class CashFlow(pm.Parameterized):
    """
    The time value associated with a single cash flow or lump-sum investment. The difference between an initial investment or present value (PV), which earns a rate of return (the interest rate per period) denoted as r, and its future value(FV), which will be received N years or periods from today.
    """
    present_value = pm.Number(
        30, bounds=(0, None), step=1, precedence=1,
        doc="""Present value of the investment.""")

    annuity = pm.Number(
        10, bounds=(0, None), step=1, precedence=1,
        doc="""A finite set of level sequential cash flows.""")

    perpetuity = pm.Boolean(
        False, precedence=1,
        doc="""Is the annuity an infinite series (like a dividend on a stock)?""")

    N = pm.Integer(
        1, bounds=(0,100), step=1, precedence=1,
        doc="""Number of periods""")

    def __init__(self, interest_rate, **params):
        self.interest_rate = interest_rate
        super(CashFlow, self).__init__(**params)

    def effective_rate(self):
        return self.interest_rate.interest_rate()

    def _future_lump_value(self, t):
        return self.present_value * (1 + self.interest_rate.interest_rate())**t

    def future_lump_value(self):
        return self._future_lump_value(self.N)

    def _future_annuity_value(self, t):
        value = self.annuity * ((1 + self.effective_rate())**t - 1) / self.effective_rate()
        if self.perpetuity:
            value += self.perpetuity_value()
        return value

    def future_annuity_value(self):
        return self._future_annuity_value(self.N)

    def _present_value_factor(self, t):
        return (1 + self.effective_rate())**(-t)

    def present_value_factor(self):
        return self._present_value_factor(self.N)

    def _present_annuity_value(self, t):
        return self.annuity * ((1 -  1/(1+self.effective_rate())**t)/self.effective_rate())

    def present_annuity_value(self):
        return self._present_annuity_value(self.N)

    def perpetuity_value(self):
        return self.annuity / self.effective_rate()

    def _total_future_value(self, t):
        return self._future_lump_value(t) + self._future_annuity_value(t)

    def total_future_value(self):
        return self._total_future_value(self.N)

    def total_present_value(self):
        return self.present_value + self.present_annuity_value()

    def cash_flow(self):
        cash_flow = pd.DataFrame([{
                'Time Period':t,
                'Lump Value': self._future_lump_value(t),
                'Annuity Value': self._future_annuity_value(t),
                'Total Value': self._total_future_value(t),
            } for t in range(self.N+1)])
        cash_flow['Cash Flow'] = cash_flow['Total Value'].diff().fillna(0)
        return cash_flow

    def view_cash_flow(self):
        cash_flow = self.cash_flow()
        return cash_flow.hvplot.table()

    def view_cash_flow_chart(self):
        cash_flow = self.cash_flow()
        return cash_flow.hvplot.line(x='Time Period', title="Cash Flow")

    @pm.depends('interest_rate.param')
    def view(self):
        return pn.Row(pn.Column(
            "Effective Rate",
            self.effective_rate(),
            'Present Value Factor:',
            self.present_value_factor,
            'Future Lump Value:',
            self.future_lump_value,
            'Future Annuity Value:',
            self.future_annuity_value,
            'Present Annuity Value:',
            self.present_annuity_value,
            'Total Future Value:',
            self.total_future_value,
            'Total Present Value:',
            self.total_present_value,
        ), pn.Column(self.view_cash_flow, self.view_cash_flow_chart),
      )

class CompoundingCashFlow(CashFlow):
    compound_periods = pm.Integer(
        1, bounds=(1,None), step=1, precedence=1,
        doc="""Number compounding periods in a period.""")

    def periodic_interest_rate(self):
        return self.interest_rate.interest_rate() / self.compound_periods

    def total_compound_periods(self):
        return self.N * self.compound_periods

    def effective_rate(self):
        return (1 + self.periodic_interest_rate())**self.compound_periods - 1

    def future_lump_value(self):
        return self.present_value * (1 + self.periodic_interest_rate())**(self.total_compound_periods())



class ContinuousCompoundingCashFlow(CashFlow):

    def effective_rate(self):
        return math.e**self.interest_rate.interest_rate() - 1

    def future_lump_value(self):
        return self.present_value * math.e**(self.interest_rate.interest_rate() * self.N)


# Chapter 2 Discounted Cash Flow Operations


"""
2.0 Net Present Value and Internal Rate of Return

There are three chief areas of financial decision-making in most businesses. 

Capital Budgeting is the allocation of funds to relatively long-range projects
or investements. 

From the perspective of capital budgeting, a company is a portfolio of projects
and investments. 

Capital structure is the choice of long-term financing for the investments the
company wants to make.

Working Capital Management is the management of the company's short-term assets
(such as inventory) and short-term liabilities (such as money owed to
suppliers).

2.1 Net Present Value and the Net Present Value Rule

Net present value (NPV) describes a way to characterize the value of an
investment, and the net present value rule is a method for choosing among
alternative investments. 

The net present value of an investment is the present value of its cash inflows
minus the present value of its cash outflows. The word "net" in an NPV refers
to subtracting the present value of the investments outflows (costs) from the
present value of its inflows (benefits) to arrive at the net benefit.

The steps in computing NPV and applying the NPV rule are as follows:
1. Identify all cash flows associated with the investment - all inflows and outflows.
2. Determine the appropriate discount rate or opportunity cost, r, for the investment project
3. Using that discount rate, find the present value of each cash flow. (Inflows are positive, outflows are negative.)
4. Sum all present values. The sum of the present values of all cash flows (inflows and outflows) is the investments net present value.
5. Apply the NPV rule: if the investment's NPV is positive, an investor should undertake it; if the NPV is negative, the investor should not undertake it. If an investor must choose one project over another, they will choose the one with higher NPV.
"""

class NetPresentValue(pm.Parameterized):
    cashflows = pm.ListSelector(default=[], objects=[])

    def __init__(self, discount_rate: InterestRate, cash_flows: list, **params):
        self.discount_rate = discount_rate
        self.cash_flows = cash_flows
        super(NetPresentValue, self).__init__(**params)

