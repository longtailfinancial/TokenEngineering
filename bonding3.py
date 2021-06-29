#!/usr/bin/env python
# coding: utf-8

# In[1]:


import panel as pn
import pandas as pd
import numpy as np
import hvplot.pandas
import holoviews as hv
import param as pm 
import random
import math
import warnings
warnings.filterwarnings('ignore')
hv.extension('bokeh')

class Sigmoid(pm.Parameterized):
    l = pm.Number(20.8, bounds=(0, 100), precedence=-1)
    s = pm.Number(17, bounds=(1,20), precedence=-1)
    m = pm.Number(21e6, bounds=(1, 21e6), step=50000, precedence=-1)
    k = pm.Number(57300, bounds=(1, 1e5), step=100, precedence=-1)
    steps = pm.Integer(1000, bounds=(10,10000), step=10, precedence=-1)
    zoom = pm.Number(0.03, bounds=(0.01,1),step=0.01)
    current_supply = pm.Number(10000, step=1000)
    
    def __init__(self, **params):
        super(Sigmoid, self).__init__(**params)
        self.param['current_supply'].bounds = (1,self.m*self.zoom)
    
    def f(self, x):
        """Paramaterized Sigmoid Function"""
        self.param['current_supply'].bounds = (1,self.m*self.zoom)
        return self.k/(1+np.exp(-x*self.l/self.m+self.s))

    def x(self):
        x = np.linspace(0,self.m*self.zoom, self.steps)
        return x
    
    def curve(self, x):
        y = self.f(x)
        return pd.DataFrame(zip(x,y),columns=['supply','price'])
    
    def collateral(self, x):
        df = self.curve(x)
        return df[df['supply'] < self.current_supply]
    
    def view_curve(self):
        x = self.x()
        return self.curve(x).hvplot.line(title='Bonding Curve', x='supply',y='price')
    
    def view_collateral(self):
        x = self.x()
        return self.collateral(x).hvplot.area(x='supply',y='price')
    
    def view(self):
        return self.view_curve()*self.view_collateral()


# In[2]:


x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

df = pd.DataFrame(zip(x,y), columns=['x','y'])


# In[3]:


df.hvplot.line(x='x',y='y', ylim=(-1,1))


# In[4]:


s = Sigmoid()
pn.Row(s,s.view)


# In[5]:


class MultiSigmoid(Sigmoid):
    l2 = pm.Number(2, bounds=(0, 100), precedence=-1)
    s2 = pm.Number(5, bounds=(1,20), precedence=-1)
    m2 = pm.Number(5e4, bounds=(1, 21e6), step=50000, precedence=-1)
    k2 = pm.Number(5, bounds=(1, 1000), step=1, precedence=-1)

    l3 = pm.Number(2, bounds=(0, 100), precedence=-1)
    s3 = pm.Number(5, bounds=(1,20), precedence=-1)
    m3 = pm.Number(5e5, bounds=(1, 21e6), step=50000, precedence=-1)
    k3 = pm.Number(50, bounds=(1, 21e6), step=100, precedence=-1)
    
    l4 = pm.Number(6, bounds=(0, 100), precedence=-1)
    s4 = pm.Number(9, bounds=(1,20), precedence=-1)
    m4 = pm.Number(5e6, bounds=(1, 21e6), step=50000, precedence=-1)
    k4 = pm.Number(2e3, bounds=(1, 21e6), step=100, precedence=-1)
    
    def __init__(self, **params):
        super(MultiSigmoid, self).__init__(**params)
        self.param['current_supply'].bounds = (1,self.m*self.zoom)
    
    def f2(self, x):
        return self.k2/(1+np.exp(-x*self.l2/self.m2+self.s2))
    
    def f3(self, x):
        return self.k3/(1+np.exp(-x*self.l3/self.m3+self.s3))
    
    def f4(self, x):
        return self.k4/(1+np.exp(-x*self.l4/self.m4+self.s4))

    def f(self, x):
        return super(MultiSigmoid, self).f(x) + self.f2(x) + self.f3(x) + self.f4(x)


# In[6]:


m = MultiSigmoid()
pn.Row(m,m.view)


# In[7]:


class Augmented(MultiSigmoid):
    reserve_rate = pm.Number(0.2, bounds=(0, 1), step=0.01)
    
    def curve(self, x):
        y = self.f(x)
        curve = pd.DataFrame(zip(x,y),columns=['supply','price'])
        curve['sell_price'] = curve['price'] * self.reserve_rate
        curve['minted'] = curve['supply'].diff()
        curve['reserve'] = curve['sell_price']*curve['minted']
        curve['funding'] = curve['price']*(1-self.reserve_rate)*curve['minted']
        return curve.bfill()
    
    def reserves(self):
        x = self.x()
        reserves = self.collateral(x)
        reserves['net'] = reserves['funding'] + reserves['reserve']
        return reserves[['funding','reserve', 'net']].sum()
    
    def view_collateral(self):
        x = self.x()
        return self.collateral(x).rename(columns={'price':'funding_price','sell_price':'reserve_price'}).hvplot.area(x='supply', y=['funding_price','reserve_price'], stacked=False, alpha=1)
    
    def view_reserves(self):
        r = self.reserves().to_frame()
        r.columns = ['CAD']
        r['CAD'] = r['CAD'].apply(lambda x: "${:,.2f}".format(x))
        return r

abc = Augmented()
pn.Row(abc,pn.Column(abc.view, abc.view_reserves))


# In[8]:


class Smart(Augmented):
    reserve_power = pm.Integer(4, bounds=(0,4))
    
    def __init__(self, **params):
        super(Smart, self).__init__(**params)
        self.reserve_rate = 1
        self.param['reserve_rate'].precedence = -1
        
    def collateral(self, x):
        curve = self.curve(x)
        curve = curve[curve['supply'] < self.current_supply]
        reserve_rate = np.power(np.linspace(0,1,len(curve)), self.reserve_power) * self.reserve_rate
        curve['sell_price'] = curve['price'] * reserve_rate
        curve['minted'] = curve['supply'].diff()
        curve['reserve'] = curve['sell_price']*curve['minted']
        curve['funding'] = curve['price']*(1-reserve_rate)*curve['minted']
        return curve
        
    def curve(self, x):
        y = self.f(x)
        curve = pd.DataFrame(zip(x,y),columns=['supply','price'])
        return curve.bfill()


# In[9]:


smart_abc = Smart()
pn.Row(smart_abc,pn.Column(smart_abc.view, smart_abc.view_reserves))


# In[10]:


class TokenEngineering(pm.Parameterized):
    monthly_salary = pm.Integer(5000, bounds=(1500,5000), step=500)
    number_employees = pm.Integer(7, bounds=(3, 12), step=1)
    number_months = pm.Integer(24, bounds=(3, 24), step=1)
    monthly_contract_size = pm.Integer(7500, bounds=(6000, 10000), step=50)
    number_of_initial_contracts = pm.Integer(2, bounds=(1, 10), step=1)
    new_contracts_per_month = pm.Number(0.33, bounds=(0, 3), step=0.33)
    office_expense = pm.Integer(7000, bounds=(3000,7000), step=50)
    
    def salary_costs(self):
        cummulative = [i*self.number_employees*self.monthly_salary for i in range(self.number_months)]
        return cummulative
    
    def office_expenses(self):
        cummulative = [i*self.office_expense for i in range(self.number_months)]
        return cummulative
    
    def costs(self):
        return [a+b for a,b in zip(self.salary_costs(), self.office_expenses())]
    
    def number_of_contracts(self):
        cummulative = [i*self.new_contracts_per_month + self.number_of_initial_contracts for i in range(self.number_months)]
        return cummulative
    
    def contract_revenue(self):
        number_of_contracts = self.number_of_contracts()
        cummulative = [i*self.monthly_contract_size*number_of_contracts[i] for i in range(self.number_months)]
        return cummulative
    
    def ltf_treasury(self):
        return [a-b for a,b in zip(self.contract_revenue(),self.costs())]
    
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


# In[11]:


t = TokenEngineering()
t.view_te()(t)


# In[12]:


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
        print("CAD:", CAD, 'Price:', current_price, 'Request:', requested, 'Batch Available:', batch_available)
        
        if requested <= batch_available:
            self.current_supply += requested
            received = requested
            return received, current_price
        
        else:
            self.current_supply += batch_available
            next_received, next_price =  self.mint(current_price*(requested-batch_available))
            total_received = next_received + batch_available
            weighted_price = current_price*(batch_available/total_received) + next_price*(next_received/total_received)
            return total_received, weighted_price
        

    def view_market(self):
        df = pd.DataFrame({
            'price' : self.current_price(),
            'supply' : int(self.current_supply),
            'marketcap' : self.current_price() * self.current_supply,
        },index=['LTT'])
        df['price'] = df['price'].apply(lambda x: "${:,.2f}".format(x))
        df['marketcap'] = df['marketcap'].apply(lambda x: "${:,.0f}".format(x))
        return df.T
    
    def view_abc(self):
        return lambda abc: pn.Row(abc,pn.Column(abc.view, pn.Row(abc.view_reserves, abc.view_market)))


# In[13]:


abc = Bonding()


# In[14]:


abc.view_abc()(abc)


# In[15]:


pn.Row(abc,pn.Column(abc.view, pn.Row(abc.view_reserves, abc.view_market)))


# In[16]:


CAD = 1e3
abc.mint(CAD)


# ### The Augmented Bonding Curve

# ### LTF Sustainability Loop

# In[17]:


class Corporate(Bonding):
    debt = pm.Number()
    
    def __init__(self, **params):
        super(Corporate, self).__init__(**params)
        self.update_debt_bounds()
        
    def collateral(self, x):
        collateral = super(Corporate, self).collateral(x)
        collateral['price'] = np.where(collateral['funding'].cumsum() < self.debt, 0, collateral['price'])
        return collateral

    @pm.depends('debt', watch=True)
    def reserves(self):
        x = self.x()
        reserves = self.collateral(x)
        reserves['net'] = reserves['funding'] + reserves['reserve']
        reserves = reserves[['funding','reserve', 'net']].sum()
        reserves['debt'] = self.debt
        reserves['net'] = reserves['net'] - self.debt
        return reserves[['funding','debt','reserve','net']]
    
    @pm.depends('current_supply', watch=True)
    def update_debt_bounds(self):
        self.param['debt'].bounds = (0,self.reserves()['funding'])


# In[18]:


c = Corporate()


# In[19]:


c.view_abc()(c)


# ### Integration with MATIC, CAD, CSTK, TEA, and TEC

# ### Multi-collateral Bonding as Portfolio Management

# ### Staking on Services Provided

# ### Leverage Accumulation

# ### The LTF CAD stablecoin

# ### Launching on Matic

# ### Conviction Voting
# https://forum.tecommons.org/t/conviction-voting-tl-dr/308

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




