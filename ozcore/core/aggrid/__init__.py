# import check_modules
from ..utils.__import_check import check_modules


# # aggrid module
if check_modules("ipyaggrid","jupyter"):
    from ozcore.core.aggrid.aggrid import Grid as __agGrid

    view = __agGrid().view
    __all__ = ["view"]