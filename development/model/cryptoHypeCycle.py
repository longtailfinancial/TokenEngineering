import panel as pn
import pandas as pd
import numpy as np
import hvplot.pandas
import holoviews as hv
import param as pm 

hv.extension('bokeh')

class CryptoHypeCycle(pm.Parameterized):
    """
    Based on the following formula: https://www.desmos.com/calculator/dufjkjfyk6 
    Thanks to Dr. P for the tutorial on interpolation https://youtu.be/3z3ljk5VhTk
    And to Austin for sharing the purely exponential formula for interpolation  y = a * e^(bx) + c. fyi, c = -a, and b = ln(1/a - 1)
    """
    current_x = pm.Number(0.5, bounds=(0,1), step=0.001)
    trend = pm.Number(0.0001, step=0.0001)
    variance = pm.Number(0.02, step=0.001)
    step = pm.Action(lambda self: self.brownian_step())
    simulation_steps = pm.Integer(250)
    run_simulation = pm.Action(lambda self: self.brownian_motion())
    brownian_data = [0.1]
    
    def x(self):
        return np.linspace(0,1)
    
    def y(self, x):
        return 0.0125 * np.exp(4.39445*x) + 0.0125
    
    def plot(self):
        x = self.x()
        y = self.y(x)
        df = pd.DataFrame({'x':x,'y':y})
        
        return df.hvplot.line(title='Crypto Hype Cycle', x='x') * hv.Points([[self.current_x, self.y(self.current_x)]]).opts(color='red', size=10)
    
    def brownian_step(self):
        self.current_x = min(1, max(0, self.current_x + np.random.normal(self.trend,self.variance)))
        self.brownian_data.append(self.y(self.current_x))
        
    def plot_brownian(self):
        return pd.DataFrame(self.brownian_data).hvplot.line()
    
    def brownian_motion(self):
        for i in range(self.simulation_steps):
            self.brownian_step()

c = CryptoHypeCycle()

