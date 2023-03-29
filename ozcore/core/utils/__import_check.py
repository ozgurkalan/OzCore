"""Check modules

prevents importing modules which are not installed
"""

from importlib.util import find_spec


def check_modules(*args)-> bool:
    """
    check_modules check if given modules exists

    Check the modules given
    
    usage
    -----
        
        check_modules(*["numpy","Pandas"])
        check_modules("jupyter")

    returns
    -------
        bool
        returns false if any given module not exists
        
    """
    for arg in args:
        if find_spec(arg) is None:
            return False
    
    # if every module exists
    return True
