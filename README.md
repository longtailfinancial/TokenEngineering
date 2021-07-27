<div align="center">
<h1>Token Engineering</h1>



<!--------------=| GITHUB BADGES START HERE |=-------------->

<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/longtailfinancial/TokenEngineering?label=Repo%20Size&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAC3klEQVQokV2Sz0sbURDHZ7NPTaIxJkG7yVbRqI1WInRjiSZW2pTSEprqQUpLwUBvhZ56KBT8C0qOFQT1JBTxpLZGpagXBVsFf6I0koi7CxKySXeTStZkk1dejn0wPHjDd2be5ztUZ2cnBINB4DgO0ul0Q3d3d7CxsTFUW1vr0jSNvr6+jsmy/J3n+W8IoUw2m4WFhQVAFEVBPp8HmqZ7g8HgF6PR+ECSJNDpdGCxWIBl2V6KokbtdvvPg4ODd6qq7hONjojy+Xz78PDwMk3TD/b29ioCu91euW9ubuDq6go6Ojq8g4ODywDgKhaLAC0tLTXb29tbiqLgyclJnE6n8f9HVVW8tbWFeZ7H6+vrv7xerx6NjY098/l8/sXFRfB4PGC1WkGSpNLS0tLXeDy+WiqV8qFQ6K3L5Xp+fHwMdXV19wcGBkJ0JBL5aDAY7p2cnIDf74dEIpGNxWIvRVH8PDExcXx4eNgcjUYPWJalWJZ1y7IM1dXVlM5ms7UBAFRVVZX1ej3e2dlZM5lMKxzH6YrFor+5uXkEITQ+Pz/PSJKUKRQKBORtkiyT8Ww2W3Z2dnYlEAi09Pf3zwmCEHC73dscx71vb2+/cDgcj0RRbFBVFTRNo5CiKHGM8WOPx9PA83x+eno60tfXlxVF8Uc4HK4WRXEUY/yipqYGKIrSYYwhk8kk6NbW1vLQ0NCbXC4HPT09dwuFwq3d3d3fFovlodls/qBp2rgsy1Usy4LJZKp4vra29onq6upCMzMzUZ/P92R/fx8MBgMoilLxjkQymayQNpvNZLPI2+bU1NRTmmGY8unp6QbDMMNer9cqCAIQcmSCcrkMDMOA0WiE8/NziMViF4IgjCSTyT+00+kk1XIbGxuruVyujWXZO2QzCL1SqVTpcnR0RP61nEqlwgAQT6VSgEjV+vp6YnoskUi8Pjs7C1xeXr5yOBxOQjCTycQRQnNNTU2bCKG/BA7GGP4BmOqAELYwZPMAAAAASUVORK5CYII=">


<img alt="Language Count" src="https://img.shields.io/github/languages/count/longtailfinancial/TokenEngineering">


<!--------------=| GITHUB BADGES END HERE |=-------------->


</div>




<br>
<font>
A collection of tools, boilerplates, scripts, and functions often used in our
Token Engineering and Software Engineering tasks.
</font>

<h2>Packages and Modules</h2>

<h3>⠗ ltfte ⠺</h3>

Longtail Financial Token Engineering tools.

Usage:
```python
import tokenengi.ltfte
or 
from tokenengi import ltfte
```


[ NEED ASSISTANCE UPDATING THIS SECTION. ]

<h3>⠗  ltfswe  ⠺</h3>

Longtail Financial Software Engineering tools.

**ltfswe** can be imported by the following lines.
```python
import tokenengi.ltswe
or 
from tokenengi import ltfswe
```

<h4>
Contents:
</h4>


***togglize*** - A decorator for Panel widget functions that gives you a toggle button to hide/unhide the widget. The decorator is able to accept two optional parameters — the button label (string), and the button color (string). By default, the default button label is "Hide / Unhide Widget" and the default button color is green.

Currently it supports three colors: red, green, and blue.

Usage:

```python
import panel as pn
pn.extension()

from tokenengi.ltfswe import togglize

@togglize("Hide/Unhide Blue Square", "blue")
def some_panel_widget():
    return pn.pane.PNG('blue_square.png')
```

<br/>

***clamp*** - A function that binds an int or float to a minimum or maximum value. 

For example, if we clamped an int x to [0, 1000] and gave it a value of 1002, the int will remain at 1000. Inversely, if we assigned -2 to x, then x remains at 0.

Usage:

```python
from tokenengi.ltfswe import clamp

x = 1001
clamp(x, 0, 1000)

print(x)
# X will be 1000.
```
