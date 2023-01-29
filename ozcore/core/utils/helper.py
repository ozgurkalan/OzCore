"""Helper functions

dirme::

    core.dirme(some_class)
    
now_prefix::

    core.now_prefix(separator='_', format='now')

"""
import pandas as pd
import datetime
from IPython.display import display

def dirme(me):
    '''lists methods of a given module in Jupyter Notebook
    
    parameters:
        me:str, module, argument, method
    
    returns:
        * displays module, arg or method as a pandas DataFrame
        * display option, set to the len of df (in Jupyter Notebook)
    
    '''
    s = pd.Series([e for e in dir(me) if not "__" in e]).sort_values()
    
    op = pd.options.display.max_rows
    pd.options.display.max_rows=len(s)
    
    display(pd.DataFrame(s, columns=[me.__name__]))
    
    pd.options.display.max_rows=op

    
def now_prefix(separator:str ="-", format:str ="now")->str:
    """datetime today or now as prefix
        
    parameters:
        separator:str, default None, a seperator string for date and time
        format:str, default now, :: 

                ("now")=> "%y%m%d-%H%M%S"
                ("today")=> "%y%m%d"
                ("or any valid format")=> "%y%m%d-%H%M%S"
        
    returns: 
        str
            
    hint:
        useful for naming files or folders
    """
    if format == "now":
        format = "%y%m%d" + separator + "%H%M%S"
    elif format == "today":
        format= "%y%m%d"
        
    return datetime.datetime.today().strftime(format)