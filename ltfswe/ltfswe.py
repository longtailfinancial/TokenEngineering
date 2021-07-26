import panel as pn
from functools import wraps

pn.extension()


def clamp(n, smallest: int=0, largest: int=1000) -> float:
    '''
    Binding an int or float
    to a minimum and maximum value.
    '''

    return max(smallest, min(n, largest))



def togglize(toggle_name: str="Hide / Unhide Widget", color: str="green"):
    '''
    A tool so widgets can be hidden/unhidden
    with a button, with the button name being the provided
    argument to the decorator.
    '''

    def decorator_function(original_function):

        @wraps(original_function) # So we can stack decorators. 
        def wrapper_function(*args, **kwargs):
            '''
            In this block are the boilerplate
            for the actual togglizer
            '''
            tog_color = {
              "green": "success",
              "red": "danger",
              "blue": "primary"
            }


            toggle = pn.widgets.Toggle(name=toggle_name, button_type=tog_color[color])
            @pn.depends(toggle)
            def toggle_watch(x):
                if x:
                    '''
                    The original function we wanted
                    to decorate is here. It's
                    what's being returned.
                    '''

                    return original_function

                else:
                    return None

            sample_widget_plot = pn.Column(pn.Column(toggle), toggle_watch)
            return sample_widget_plot


            return result
        return wrapper_function
    return decorator_function
