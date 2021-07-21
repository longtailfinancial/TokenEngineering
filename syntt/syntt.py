#! /usr/bin/python3

def clamp(n, smallest: int=0, largest: int=1000) -> float:
    '''
    Binding an int or float
    to a minimum and maximum value.
    '''

    return max(smallest, min(n, largest))
