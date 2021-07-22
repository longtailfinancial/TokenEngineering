#! /usr/bin/python3

def clamp(n, smallest: int=0, largest: int=1000) -> float:
    '''
    Binding an int or float
    to a minimum and maximum value.
    '''

    return max(smallest, min(n, largest))


def togglize(toggle_name):
    '''
    A Skeleton for what is planned
    decorator to embed a panel widget
    into a toggle control.

    So the widget can be hidden/unhidden
    with a button, with the button name being the provided
    argument to the decorator.
    '''
    pass
