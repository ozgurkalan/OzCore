""" 

initiate some of the modules for fast access with core

note:
    in order not to duplicate variables, some of the modules are called with dunder method 

"""
# check_module
from .utils import check_modules

# # iöport modules
from ozcore.core import df, utils, aggrid, path, data

# path module::Folder
folder = path.folder

# if aggrid module is available
try:
    # view - aggric
    view = aggrid.view
except:
    pass

# if sql module is available
try:
    csv = data.csv.csv
    sql = data.sqlite.sql
except:
    pass


