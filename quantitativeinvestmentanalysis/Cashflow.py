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


class CashFlow(pm.Parameterized):
    """
    The time value associated with a single cash flow or lump-sum investment. The difference between an initial investment or present value (PV), which earns a rate of return (the interest rate per period) denoted as r, and its future value(FV), which will be received N years or periods from today.
    """

    present_value = pm.Number(
        30,
        bounds=(0, None),
        step=1,
        precedence=1,
        doc="""Present value of the investment.""",
    )

    annuity = pm.Number(
        10, step=1, precedence=1, doc="""A finite set of level sequential cash flows."""
    )

    perpetuity = pm.Boolean(
        False,
        precedence=1,
        doc="""Is the annuity an infinite series (like a dividend on a stock)?""",
    )

    N = pm.Integer(
        1, bounds=(0, 100), step=1, precedence=1, doc="""Number of periods"""
    )

    def __init__(self, interest_rate, **params):
        self.interest_rate = interest_rate
        super(CashFlow, self).__init__(**params)

    def effective_rate(self):
        return self.interest_rate.interest_rate()

    def _future_lump_value(self, t):
        return self.present_value * (1 + self.interest_rate.interest_rate()) ** t

    def future_lump_value(self):
        return self._future_lump_value(self.N)

    def _future_annuity_value(self, t):
        value = (
            self.annuity
            * ((1 + self.effective_rate()) ** t - 1)
            / self.effective_rate()
        )
        if self.perpetuity:
            value += self.perpetuity_value()
        return value

    def future_annuity_value(self):
        return self._future_annuity_value(self.N)

    def _present_value_factor(self, t):
        return (1 + self.effective_rate()) ** (-t)

    def present_value_factor(self):
        return self._present_value_factor(self.N)

    def _present_annuity_value(self, t):
        return self.annuity * (
            (1 - 1 / (1 + self.effective_rate()) ** t) / self.effective_rate()
        )

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
        cash_flow = pd.DataFrame(
            [
                {
                    "Time Period": t,
                    "Lump Value": self._future_lump_value(t),
                    "Annuity Value": self._future_annuity_value(t),
                    "Total Value": self._total_future_value(t),
                }
                for t in range(self.N + 1)
            ]
        )
        cash_flow["Cash Flow"] = cash_flow["Total Value"].diff().fillna(0)
        return cash_flow

    def view_cash_flow(self):
        cash_flow = self.cash_flow()
        return cash_flow.hvplot.table()

    def view_cash_flow_chart(self):
        cash_flow = self.cash_flow()
        return cash_flow.hvplot.line(x="Time Period", title="Cash Flow")

    @pm.depends("interest_rate.param")
    def view(self):
        return pn.Row(
            pn.Column(
                "Effective Rate",
                self.effective_rate(),
                "Present Value Factor:",
                self.present_value_factor,
                "Future Lump Value:",
                self.future_lump_value,
                "Future Annuity Value:",
                self.future_annuity_value,
                "Present Annuity Value:",
                self.present_annuity_value,
                "Total Future Value:",
                self.total_future_value,
                "Total Present Value:",
                self.total_present_value,
            ),
            pn.Column(self.view_cash_flow, self.view_cash_flow_chart),
        )


class CompoundingCashFlow(CashFlow):
    compound_periods = pm.Integer(
        1,
        bounds=(1, None),
        step=1,
        precedence=1,
        doc="""Number compounding periods in a period.""",
    )

    def periodic_interest_rate(self):
        return self.interest_rate.interest_rate() / self.compound_periods

    def total_compound_periods(self):
        return self.N * self.compound_periods

    def effective_rate(self):
        return (1 + self.periodic_interest_rate()) ** self.compound_periods - 1

    def future_lump_value(self):
        return self.present_value * (1 + self.periodic_interest_rate()) ** (
            self.total_compound_periods()
        )


class ContinuousCompoundingCashFlow(CashFlow):
    def effective_rate(self):
        return math.e ** self.interest_rate.interest_rate() - 1

    def future_lump_value(self):
        return self.present_value * math.e ** (
            self.interest_rate.interest_rate() * self.N
        )
