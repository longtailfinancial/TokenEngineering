# from QIA import TimeValueMoney


# tvm = TimeValueMoney()

# tvm.servable()

# pip install pandas hvplot==0.7.1 holoviews==1.14.3 bokeh panel==0.11.3
# panel serve holoviz_linked_brushing.py --auto --show
import hvplot.pandas
import holoviews as hv
import panel as pn
from bokeh.sampledata.iris import flowers

pn.extension(sizing_mode="stretch_width")
hv.extension("bokeh")


# From Template

accent_color = "#00286e"

# scatter = flowers.hvplot.scatter(
    # x="sepal_length", y="sepal_width", c=accent_color, responsive=True, height=350
# )
# hist = flowers.hvplot.hist("petal_width", c=accent_color, responsive=True, height=350)

# scatter.opts(size=10)

# selection_linker = hv.selection.link_selections.instance()

# scatter = selection_linker(scatter)
# hist = selection_linker(hist)

# scatter.opts(tools=["hover"], active_tools=["box_select"])
# hist.opts(tools=["hover"], active_tools=["box_select"])

# pn.template.FastListTemplate(
    # site="Quantitative Investment Analysis",
    # title="Cash Flow Modelling and Investment",
    # header_background=accent_color,
    # main=[scatter, hist],
# ).servable()


from qia import InterestRate
ir = InterestRate()
pane = pn.Column(ir, "Interest Rate:", ir.interest_rate)
# pane.servable()
pn.template.FastListTemplate(
    site="Quantitative Investment Analysis",
    title="Investement and Cash Flow Modelling",
    header_background=accent_color,
    main=[pane],
).servable()
