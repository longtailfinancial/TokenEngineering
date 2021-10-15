import panel as pn
import pandas as pd
import numpy as np
import hvplot.pandas
import holoviews as hv
import param as pm
import random
import math
import warnings
import bokeh
import plotly
import plotly.express as px


warnings.filterwarnings('ignore')
hv.extension('bokeh')

class ReserveRatio(pm.Parameterized):
    """
    This model simulates bancor style model with reserve ratio
    """
    reserve_ratio = pm.Number(0.35, bounds=(0,1), step=0.01)
    price = pm.Number(100, bounds=(0,1000), step=0.1)
    supply = pm.Number(100, bounds=(0,1000), step=0.1)
    
    def x(self):
        return np.linspace(0, self.supply, 1000)
    
    def curve(self, x):
        y = (x**((1/self.reserve_ratio)-1) * self.price) / (self.supply**((1/self.reserve_ratio)-1))
        return pd.DataFrame(zip(x,y),columns=['supply','price'])
    
    def view(self):
        curve = self.curve(self.x())
        return curve.hvplot.line(x='supply',y='price', line_width=6)        

# Sigmoid
class Sigmoid(pm.Parameterized):
    """
    A parameterized class to represent sigmoid curve.

    ...

    Attributes
    ----------
    l : number that adjusts the y-axis scale
        default=20.8, bounds=(0, 100)
    s : number that adjusts the supply of tokens
        default=17, bounds=(1, 20)
    m : number that adjusts the slope
        default=21e6, bounds=(1, 21e6)
    k : number of tokens sold
        default=57300, bounds=(1, 1e5)
    steps : Integer
        default=1000, bounds=(10, 10000)
    zoom : number that affects the scale of the presented view
        default=0.03, bounds=(0.01, 1)
    current_supply : number modeling the current tokens in circulation
        default=10000

    Methods
    -------
    f(x):
        Paramaterized Sigmoid Function.

    x():
        returns values for x axis scale based on m, zoom, steps.

    curve(x):
        Returns a dataframe containing the supply and price based on the X values
        supplied to f(x)

    collateral(x):
        Creates and returns the dataframe containing values that are less than the
        current token supply

    view_curve():
        Return a holoviews line plot modeling the relationship between the supply
        and the price

    view_collateral():
        Returns a holoviews area plot that shows the relationship between the
        supply and price

    view():
        Returns the two previous views over layed


    """

    l = pm.Number(20.8, bounds=(0, 100), precedence=-1)
    s = pm.Number(17, bounds=(1, 20), precedence=-1)
    m = pm.Number(21e6, bounds=(1, 21e6), step=50000, precedence=-1)
    k = pm.Number(57300, bounds=(1, 1e5), step=100, precedence=-1)
    steps = pm.Integer(1000, bounds=(10, 10000), step=10, precedence=-1)
    zoom = pm.Number(0.03, bounds=(0.01, 1), step=0.01)
    current_supply = pm.Number(10000, step=1000)

    def __init__(self, **params):
        super(Sigmoid, self).__init__(**params)
        self.param['current_supply'].bounds = (1, self.m*self.zoom)

    def f(self, x):
        """Parameterized Sigmoid Function"""
        self.param['current_supply'].bounds = (1, self.m*self.zoom)
        return self.k/(1+np.exp(-x*self.l/self.m+self.s))

    def x(self):
        x = np.linspace(0, self.m*self.zoom, self.steps)
        return x

    def curve(self, x):
        y = self.f(x)
        return pd.DataFrame(zip(x, y), columns=['supply', 'price'])

    def collateral(self, x):
        df = self.curve(x)
        return df[df['supply'] < self.current_supply]

    def view_curve(self):
        x = self.x()
        return self.curve(x).hvplot.line(title='Bonding Curve', x='supply', y='price')

    def view_collateral(self):
        x = self.x()
        return self.collateral(x).hvplot.area(x='supply', y='price')

    def view(self):
        return self.view_curve()*self.view_collateral()


# Multisigmoid
class MultiSigmoid(Sigmoid):
    """
    A parameterized class to represent a Multi-Sigmoid curve that inherits
    all the methods and attributes from Sigmoid

    Attributes
    ----------

    l : number that adjusts the y-axis scale
        default=20.8, bounds=(0, 100)

    s : number that adjusts the supply of tokens
        default=17, bounds=(1, 20)

    m : number that adjusts the slope
        default=21e6, bounds=(1, 21e6)

    k : number of tokens sold
        default=57300, bounds=(1, 1e5)

    NOTE: Each of the additional Sigmoid have their own respective variables appropriately
          labeled with that curves number. (Ex: l2, s2, m2, k2)

    Methods
    -------
    f2(x): Calculates the second Sigmoid curve fundamental function

    f3(x): Calculates the third Sigmoid curve fundamental function

    f4(x): Calculates the fourth Sigmoid curve fundamental function

    f(x): Returns the sum of the original Sigmoid curve plus f2(), f3(), and f4()


    """
    l2 = pm.Number(2, bounds=(0, 100), precedence=-1)
    s2 = pm.Number(5, bounds=(1, 20), precedence=-1)
    m2 = pm.Number(5e4, bounds=(1, 21e6), step=50000, precedence=-1)
    k2 = pm.Number(5, bounds=(1, 1000), step=1, precedence=-1)

    l3 = pm.Number(2, bounds=(0, 100), precedence=-1)
    s3 = pm.Number(5, bounds=(1, 20), precedence=-1)
    m3 = pm.Number(5e5, bounds=(1, 21e6), step=50000, precedence=-1)
    k3 = pm.Number(50, bounds=(1, 21e6), step=100, precedence=-1)

    l4 = pm.Number(6, bounds=(0, 100), precedence=-1)
    s4 = pm.Number(9, bounds=(1, 20), precedence=-1)
    m4 = pm.Number(5e6, bounds=(1, 21e6), step=50000, precedence=-1)
    k4 = pm.Number(2e3, bounds=(1, 21e6), step=100, precedence=-1)

    def __init__(self, **params):
        super(MultiSigmoid, self).__init__(**params)
        self.param['current_supply'].bounds = (1, self.m*self.zoom)

    def f2(self, x):
        return self.k2/(1+np.exp(-x*self.l2/self.m2+self.s2))

    def f3(self, x):
        return self.k3/(1+np.exp(-x*self.l3/self.m3+self.s3))

    def f4(self, x):
        return self.k4/(1+np.exp(-x*self.l4/self.m4+self.s4))

    def f(self, x):
        """
        The fundamental function for this class as it calls all the other functions
        and returns the sum of their values.
        """
        return super(MultiSigmoid, self).f(x) + self.f2(x) + self.f3(x) + self.f4(x)


# Augumented
class Augmented(MultiSigmoid):
    """
    A parameterized class to model the Augmented MultiSigmoid bonding Curve.

    Attributes
    ----------

    reserve_rate: number that represents the reserve rate of the curve.
                  default=0.2, bounds=(0, 1), step=0.01

    NOTE: Inherits all previous attributes.


    Methods
    -------
    curve(x):
        Calculates and returns an Augmented bonding curve data frame that shows
        the supply, price, minted  tokens, reserve, and funding of the curve as a whole

    reserves():
        Returns data frame of the collateral and includes the net gains of the curve

    view_collateral():
        Returns a holoviews plot of the collateral against the curve

    view_reserves():
        Returns a data frame showing the sum of the reserves in regards to CAD

    """
    reserve_rate = pm.Number(0.2, bounds=(0, 1), step=0.01)

    def curve(self, x):
        y = self.f(x)
        curve = pd.DataFrame(zip(x, y), columns=['supply', 'price'])
        curve['sell_price'] = curve['price'] * self.reserve_rate
        curve['minted'] = curve['supply'].diff()
        curve['reserve'] = curve['sell_price']*curve['minted']
        curve['funding'] = curve['price']*(1-self.reserve_rate)*curve['minted']
        return curve.bfill()

    def reserves(self):
        x = self.x()
        reserves = self.collateral(x)
        reserves['net'] = reserves['funding'] + reserves['reserve']
        return reserves[['funding', 'reserve', 'net']].sum()

    def view_collateral(self):
        x = self.x()
        return self.collateral(x).rename(columns={'price': 'funding_price', 'sell_price': 'reserve_price'}).hvplot.area(x='supply', y=['funding_price', 'reserve_price'], stacked=False, alpha=1)

    def view_reserves(self):
        r = self.reserves().to_frame()
        r.columns = ['CAD']
        r['CAD'] = r['CAD'].apply(lambda x: "${:,.2f}".format(x))
        return r


# Smart
class Smart(Augmented):
    """
    A parameterized class to model the Smart augmented MultiSigmoid bonding Curve.

    Attributes
    ----------

    reserve_power: The power at which the curves reserve ratio is calculated

    NOTE: Inherits all previous attributes.

    Methods
    -------

    collateral(x):
        Creates and returns a data frame of the collateral against the curve and the
        selling curve.

    curve(x):
       Same as the curve function from earlier, but missing values are now filled with
       .bfill() from pandas

    """
    reserve_power = pm.Integer(4, bounds=(0, 4))

    def __init__(self, **params):
        super(Smart, self).__init__(**params)
        self.reserve_rate = 1
        self.param['reserve_rate'].precedence = -1

    def collateral(self, x):
        curve = self.curve(x)
        curve = curve[curve['supply'] < self.current_supply]
        reserve_rate = np.power(np.linspace(
            0, 1, len(curve)), self.reserve_power) * self.reserve_rate
        curve['sell_price'] = curve['price'] * reserve_rate
        curve['minted'] = curve['supply'].diff()
        curve['reserve'] = curve['sell_price']*curve['minted']
        curve['funding'] = curve['price']*(1-reserve_rate)*curve['minted']
        return curve

    def curve(self, x):
        y = self.f(x)
        curve = pd.DataFrame(zip(x, y), columns=['supply', 'price'])
        return curve.bfill()


# Token Engineering
class TokenEngineering(pm.Parameterized):
    monthly_salary = pm.Integer(5000, bounds=(1500, 5000), step=500)
    number_employees = pm.Integer(7, bounds=(3, 12), step=1)
    number_months = pm.Integer(24, bounds=(3, 24), step=1)
    monthly_contract_size = pm.Integer(7500, bounds=(6000, 10000), step=50)
    number_of_initial_contracts = pm.Integer(2, bounds=(1, 10), step=1)
    new_contracts_per_month = pm.Number(0.33, bounds=(0, 3), step=0.33)
    office_expense = pm.Integer(7000, bounds=(3000, 7000), step=50)

    def salary_costs(self):
        cummulative = [i*self.number_employees *
                       self.monthly_salary for i in range(self.number_months)]
        return cummulative

    def office_expenses(self):
        cummulative = [
            i*self.office_expense for i in range(self.number_months)]
        return cummulative

    def costs(self):
        return [a+b for a, b in zip(self.salary_costs(), self.office_expenses())]

    def number_of_contracts(self):
        cummulative = [i*self.new_contracts_per_month +
                       self.number_of_initial_contracts for i in range(self.number_months)]
        return cummulative

    def contract_revenue(self):
        number_of_contracts = self.number_of_contracts()
        cummulative = [i*self.monthly_contract_size*number_of_contracts[i]
                       for i in range(self.number_months)]
        return cummulative

    def ltf_treasury(self):
        return [a-b for a, b in zip(self.contract_revenue(), self.costs())]

    def cummulative_data(self):
        data = pd.DataFrame({
            'Contract Revenue': self.contract_revenue(),
            'Number of Contracts': self.number_of_contracts(),
            'Salary Costs': self.salary_costs(),
            'Net Profit': self.ltf_treasury(),
            'Office Expenses': self.office_expenses()})
        data.index.name = 'Month'
        return data

    def results(self):
        return self.cummulative_data().iloc[[-1]]

    def results_view(self):
        return self.results().reset_index().hvplot.table(title="Results")

    def chart_view(self):
        return self.cummulative_data().hvplot.line(title='Cumulative Revenue, Costs, and Profit') * hv.HLine(0).opts(color='black', line_width=1.2)

    def view_te(self):
        return lambda te: pn.Row(te, pn.Column(te.chart_view, te.results_view))


# Bonding Curve

class Bonding(Smart):

    def batch_minted(self):
        return self.current_supply - self.collateral(self.x()).iloc[-1]['supply']

    def batch_available(self):
        return self.collateral(self.x()).iloc[-1]['minted'] - self.batch_minted()

    def current_price(self):
        return self.collateral(self.x()).iloc[-1]['price']

    def mint(self, CAD: float, tol=1e-6):
        self.zoom = 0.05
        current_price = self.current_price()
        requested = CAD/current_price
        batch_available = self.batch_available()
        if batch_available < tol:
            self.current_supply += tol
            return self.mint(CAD)
        print("CAD:", CAD, 'Price:', current_price, 'Request:',
              requested, 'Batch Available:', batch_available)

        if requested <= batch_available:
            self.current_supply += requested
            received = requested
            return received, current_price

        else:
            self.current_supply += batch_available
            next_received, next_price = self.mint(
                current_price*(requested-batch_available))
            total_received = next_received + batch_available
            weighted_price = current_price * \
                (batch_available/total_received) + \
                next_price*(next_received/total_received)
            return total_received, weighted_price

    def view_market(self):
        df = pd.DataFrame({
            'price': self.current_price(),
            'supply': int(self.current_supply),
            'marketcap': self.current_price() * self.current_supply,
        }, index=['LTT'])
        df['price'] = df['price'].apply(lambda x: "${:,.2f}".format(x))
        df['marketcap'] = df['marketcap'].apply(lambda x: "${:,.0f}".format(x))
        return df.T

    def view_abc(self):
        return lambda abc: pn.Row(abc, pn.Column(abc.view, pn.Row(abc.view_reserves, abc.view_market)))


# ### The Augmented Bonding Curve
# ### LTF Sustainability Loop
class Corporate(Bonding):
    '''
    The Augmented Bonding Curve
    Org's Sustainability Loop
    '''
    debt = pm.Number()

    def __init__(self, **params):
        super(Corporate, self).__init__(**params)
        self.update_debt_bounds()

    def collateral(self, x):
        collateral = super(Corporate, self).collateral(x)
        collateral['price'] = np.where(
            collateral['funding'].cumsum() < self.debt, 0, collateral['price'])
        return collateral

    @pm.depends('debt', watch=True)
    def reserves(self):
        x = self.x()
        reserves = self.collateral(x)
        reserves['net'] = reserves['funding'] + reserves['reserve']
        reserves = reserves[['funding', 'reserve', 'net']].sum()
        reserves['debt'] = self.debt
        reserves['net'] = reserves['net'] - self.debt
        return reserves[['funding', 'debt', 'reserve', 'net']]

    @pm.depends('current_supply', watch=True)
    def update_debt_bounds(self):
        self.param['debt'].bounds = (0, self.reserves()['funding'])


class SineWave(pm.Parameterized):
    '''
    Docstring
    '''
    y_intercept = pm.Number(0)
    amplitude = pm.Number(1)
    period = pm.Number(10)
    plot_range = pm.Number(500)
    rotation = pm.Number(0.7)

    def __init__(self,
                 y_intercept: float = 0,
                 amplitude: float = 1.0,
                 period: float = 10.0,
                 plot_range: int = 500,
                 rotation: float = 0.7):
        super().__init__()
        '''
        Docstring
        '''
        self.y_intercept = y_intercept
        self.amplitude = amplitude
        self.period = period
        self.plot_range = plot_range
        self.rotation = rotation

    def show_controls(self):
        '''
        Docstring
        '''

        return pn.Column(
            self.param.y_intercept,
            self.param.amplitude,
            self.param.period,
            self.param.rotation
        )

    @pm.depends('y_intercept',
                'amplitude',
                'period',
                'plot_range',
                'rotation')
    def xy_cols(self):
        '''
        If we just want the two columns of the x and y
        values, we call this function. Very useful for debugging
        and if SineWave is to be used within another function.
        '''
        a = self.rotation
        b = self.period
        c = self.amplitude

        # The limit of the Axis, since we're plotting discrete points.
        t = np.linspace(0, self.plot_range, self.plot_range + 1)

        x = np.cos(a)*(t/b) - np.sin(a) * np.sin(t/b) * c
        y = np.sin(a)*t/b + (np.cos(a)*np.sin(t/b) * c) + self.y_intercept

        return x, y

    @pm.depends('y_intercept',
                'amplitude',
                'period',
                'plot_range',
                'rotation')
    def data_frame(self):
        '''
        Same purpose as xy_cols, but if we want the data as a Pandas
        Dataframe.
        '''
        x_col, y_col = self.xy_cols()
        sine_dataframe = pd.DataFrame(zip(x_col, y_col), columns=['x', 'y'])

        return sine_dataframe

    @pm.depends('y_intercept',
                'amplitude',
                'period',
                'plot_range',
                'rotation')
    def plot(self):
        '''
        Asks for the dataframe so it can be plotted.
        Initially, everything was here. But coupling was so severe, so
        I split everything into separate functions.
        '''

        sine_plot = self.data_frame()
        return px.line(sine_plot, x="x", y=['y'])

## Modified from https://github.com/CommonsBuild/commons-config-dashboard/blob/development/models/notebooks/Bonding_Curve_Calculator.ipynb

class BondingCurveInitializer(pm.Parameterized):
    """This class initializes the bonding curve.

    Default Params:
    ----------------
        initial price (float): initial token price

        initial supply (int): initial token supply ex: ETH

        initial balance (int): initial collateral balance ex: USDT

    Functions:
    --------
        view: returns the complete dashboard pane view of the model
    """

    initial_price = pm.Number(1, bounds=(0.1,10), step=0.1)
    initial_supply = pm.Number(3000, bounds=(1,10000), step=10)
    initial_balance = pm.Number(1000, bounds=(1,10000), step=10)

    def reserve_ratio(self):
        return self.initial_balance / (self.initial_price * self.initial_supply)
    
    #Returns the token price given a specific supply
    def get_price(self, supply):
        return (supply ** ((1 / self.reserve_ratio()) - 1) * self.initial_price) / (
            self.initial_supply ** ((1 / self.reserve_ratio()) - 1)
        )

    #Returns the collateral balance price given a specific supply
    def get_balance(self, supply):
        return (
            self.reserve_ratio() * self.get_price(supply) * supply
        )
    
    #For drawing the bonding curve. Range shows how many times the initial supply you make the graph for, steps: how many subdivisions
    def curve_over_supply(self, range=1000, steps=10000):
        x = np.linspace(0, range, steps)
        y = self.get_price(x)
        return pd.DataFrame(zip(x, y), columns=["Supply", "Price"])
    
    def curve_over_balance(self, range=1000, steps=10000):
        supply_list = np.linspace(0, range, steps)
        x = self.get_balance(supply_list)
        y = self.get_price(supply_list)

        return pd.DataFrame(zip(x, y), columns=["Balance", "Price"])
    
    def initial_point(self):
        points = hv.Points((self.initial_supply,self.initial_price))
        return points.opts(color='k', size=7)
    
    def outputs(self):
        return "Reserve Ratio: {0:.2f}".format(self.reserve_ratio())
    
    def plot_curve(self):
        hv.extension('bokeh')
        curve = self.curve_over_supply(range=self.initial_supply*6)
        return curve.hvplot.line(x='Supply', y='Price', line_width=4) * self.initial_point()
    
    def view(self):
        return pn.Row(pn.Column(self.param, self.outputs), self.plot_curve)

class BondingCurve(BondingCurveInitializer):
    """This class is inherited from the BondingCurveInitializer class.
    Additionally, it help manage current and max token supply

    Functions:
    --------
        view: returns the complete dashboard pane view of the model
    """
    
    supply = pm.Range(default=(5000, 20000), bounds=(0, 50000), label='Current Supply : Max Supply')# current supply, Max Supply
    
    #Returns how much USDT you get from selling Token X 
    def sale_return(self, bonded):
        return self.get_balance(self.supply[0]) * (
            (bonded / self.supply[0] + 1) ** (1 / self.reserve_ratio()) - 1
        )

    #Returns how much Token X you get from purchasing with USDT
    def purchase_return(self, collateral):
        return self.supply[0] * (
            (collateral / self.get_balance(self.supply[0]) + 1) ** (self.reserve_ratio()) - 1
        )
    
    def current_point(self):
        points = hv.Points((self.supply[0],self.get_price(self.supply[0])))
        return points.opts(color='red', size=7)

    def outputs(self):
        return "Reserve Ratio: {0:.2f}\n\rInitial price: {1:.2f}\n\rCurrent price: {2:.2f}".format(self.reserve_ratio(),self.initial_price,self.get_price(self.supply[0]))

    def plot_curve(self):
        hv.extension('bokeh')
        curve = self.curve_over_supply(range=self.supply[1])
        return curve.hvplot.line(x='Supply', y='Price', line_width=4) * self.initial_point() * self.current_point()
    
    def view(self):
        return pn.Row(pn.Column(self.param, self.outputs), self.plot_curve)

class BondingCurveCalculator(BondingCurve):
    """This class is inherited from the BondingCurve class.
    Additionally, it offers the ability to calculate the change in token price and token supply with change in supply

    Functions:
    --------
        view: returns the complete dashboard pane view of the model
    """
    
    amount = pm.Number(0, bounds=(-1000, 1000), label='Change in Token Supply')
    
    def new_supply(self):
        return max(0, min(self.supply[0] + self.purchase_return(self.sale_return(self.amount)), self.supply[1]))

    def new_point(self):
        new_supply = self.new_supply()
        points = hv.Points((new_supply, self.get_price(new_supply)))
        return points.opts(color='green', size=7)
    
    def outputs(self):
        return "Reserve Ratio: {0:.2f}\n\rInitial price: {1:.2f}\n\rCurrent price: {2:.2f}\n\rIf Token supply is changed by {5:.2f}:\n\r New price: {3:.2f}\n\rNew Supply: {4:.2f}".format(self.reserve_ratio(), self.initial_price, self.get_price(self.supply[0]), self.get_price(self.new_supply()), self.new_supply(), self.amount)

    def plot_curve(self):
        hv.extension('bokeh')
        curve = self.curve_over_supply(range=self.supply[1])
        return curve.hvplot.line(x='Supply', y='Price', line_width=4) * self.current_point() * self.new_point() * self.initial_point()
    
    def view(self):
        return pn.Row(pn.Column(self.param, self.outputs), self.plot_curve)