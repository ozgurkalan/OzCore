"""Helper functions

dirme::

    core.dirme(some_class)
    
now_prefix::

    core.now_prefix(separator='_', format='now')

serialize_a_jason_field::

    core.serialize_a_jason_field(some_jason_content)

"""
import numpy as np
import pandas as pd
import datetime
import ast # for safe eval of list nodes in json fields (ast.literal_eval(s))
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

    
def serialize_a_json_field(val, node=None):
        """Safely eval a field with a string list or dict inherited from a json file
            e.g. [{name:test}] => list object having dict node 'name'
        
        parameters:
            val: json | dict, field value passed
            node: str, key name in the dictionary
            
        returns:
            * semicolon seperated values if val is a set, dict or list
            * if node is given, returns the values in the node as semicolon separated string
            * if val is None, returns None
            * if fails to the opretion returns back the val itself
            
        hint:
            useful in serializing fields in a dataframe having dict like objects
        """
        if val == np.nan: return val # return NaN values back
    
        try:
            val = ast.literal_eval(str(val)) # first be sure it is str then eval as dict/list object

            if node:
                if isinstance(val, dict) and (node in val.keys()):
                    val = val.get(node) # get the node values
                
                
            val = set(list(val)) # return a list
            val = sorted(val)
            return ";".join(val) # return a string separated by ;

        except:
            return val # if try is not successful, return back the value