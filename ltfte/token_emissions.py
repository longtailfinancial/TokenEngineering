import copy
import pandas as pd
import numpy as np
import plotly.express as px

class TokenEmissions:
    """
    Generalized model of Token Emissions
    """
    def __init__(self, stakeholders: list = [
        {
            "name": "Early_Backers",
            "allocation": 8,
            "cliff": 6,
            "vesting": 24,
            "unlock0_amt": 0
        },
        {
            "name": "Team",
            "allocation": 16,
            "cliff": 6,
            "vesting": 36,
            "unlock0_amt": 0
        },
        {
            "name": "Collator_Fund",
            "allocation": 5,
            "cliff": 0,
            "vesting": 3,
            "unlock0_amt": 10000000
        },
        {
            "name": "Community",
            "allocation": 66,
            "cliff": 0,
            "vesting": 36,
            "unlock0_amt": 50000
        },
        {
            "name": "Parachain_Slot",
            "allocation": 5,
            "cliff": 6,
            "vesting": 24,
            "unlock0_amt": 0
        }
        ], 
        total_token_supply: int = 1000000000):
        """Initialize class

        Args:
            stakeholders (list, optional): list of dicts containing stakeholder info. 
            Refer method calc_emissions_linear for more info
            total_token_supply (int, optional): total token supply. Defaults to 1000000000.
        """        
        self.total_token_supply = total_token_supply
        self.stakeholders = stakeholders
        self._df_vesting_schedule = None
    
    def calc_emissions_linear(
            self,
            name: str,
            allocation: float,
            cliff: int,
            vesting: int,
            unlock0_amt: float):
        """Returns a list of vesting schedule for each token allocation
        If unlock0_amt is not 0, then the cliff period is ignored

        Args:
            name (str): name of stakeholder
            allocation (float): stakeholder's allocation percent
            cliff (int): number of months to pause emissions from month 0
            vesting (int): total number of months to vest
            unlock0_amt (float): amount of tokens to be unlocked at the beginning
             of the month or launch of the token

        Returns:
            list: list of tokens to be unlocked at the end of each month
        """
        tokens_allocated = self.total_token_supply * allocation * 0.01
        # if 0 tokens Unlock at first month
        if unlock0_amt == 0:
            if vesting == 0:
                vesting_schedule = [tokens_allocated]
            else:
                monthly_unlock = tokens_allocated / vesting
                vesting_schedule = []
                for i in range(vesting + 1):
                    if i < cliff:
                        vesting_schedule.append(0)
                    elif i == cliff:
                        vesting_schedule.append(monthly_unlock * cliff)
                    else:
                        vesting_schedule.append(monthly_unlock)
            return vesting_schedule
        else:
            day1_unlock = unlock0_amt
            vesting_schedule = [day1_unlock]
            monthly_unlock = (tokens_allocated - day1_unlock) / vesting
            for i in range(1, vesting + 1):
                vesting_schedule.append(monthly_unlock)
            return vesting_schedule

    def get_vesting_schedule(self):
        """
        Returns a dataframe of vesting schedule containing all stakeholders.

        Returns:
            DataFrame: DataFrame with stakeholders as columns and months as rows
        """
        df_columns = []
        vesting_schedule = []
        for i in self.stakeholders:
            df_columns.append(i["name"])
            vesting_schedule.append(
                self.calc_emissions_linear(**i)
                )
        # generate a list of lists to dataframe
        df = pd.DataFrame(vesting_schedule)
        df = df.replace(np.nan, 0)
        df = df.T
        df.columns = df_columns
        self._df_vesting_schedule = df
        return df

    def plot_vesting_schedule(self):
        """
        Returns a plot of the vesting schedule

        Returns:
            fig: plotly fig object
        """        
        df = copy.deepcopy(self._df_vesting_schedule)
        # display(df)
        df['Circulating Supply'] = df.sum(axis=1)
        df = df.cumsum()
        df.insert(0, "Month", df.index, True)
        fig = px.bar(df.drop(columns=['Month', 'Circulating Supply']),
                     labels={"index": "Months",
                             "variable": "Category",
                             "value": "Number of Tokens"},
                     title='Cumulative Token Release Schedule')

        return fig

    def plot_supply_analysis(self):
        """Plot supply Analysis

        Returns:
            fig: plotly fig object
        """        
        df = copy.deepcopy(self._df_vesting_schedule)
        df['Circulating Supply'] = df.sum(axis=1)
        inflation_abs = df['Circulating Supply']
        inflation = inflation_abs.cumsum()
        inflation_percent = inflation.pct_change() * 100
        df = pd.DataFrame([inflation, inflation_abs, inflation_percent])
        df = df.T
        df = df.replace(np.nan, 0)
        df.columns = ['inflation', 'inflation_abs', 'inflation_pct']
        fig = px.line(df['inflation_pct'],
                      labels={"index": "Months",
                              "value": "Inflation %"},
                      title='Relative Inflation Percent by Month',)
        fig.layout.update(showlegend=False)
        return fig

    def plot_token_allocation(self):
        """Plot token allocation pie chart

        Returns:
            fig: plotly figure object
        """
        names = [s["name"] for s in self.stakeholders]
        allocations = [s["allocation"] for s in self.stakeholders]
        fig = px.pie(values=allocations, names=names)
        return fig

    def output(self):
        """Calculate vesting schedule and run all fig objects

        Returns:
            list: list of all output objects
        """        
        return [
            self.get_vesting_schedule(),
            self.plot_vesting_schedule(),
            self.plot_token_allocation(),
            self.plot_supply_analysis()
            ]
