""" 

initiate some of the modules for fast access with core

note:
    in order not to duplicate variables, some of the modules are called with dunder method 

"""
# check_module
from .utils import check_modules

# # df, utils, aggrid
from ozcore.core import df, utils, aggrid, path

# path module::Folder
folder = path.folder

if check_modules("jupyter","ipyaggrid"):
    # view - aggric
    view = aggrid.view

# # Sqlite
from ozcore.core.data.sqlite.sqlite import Sqlite as sql

# # CSV
from ozcore.core.data.csv.base import Base as __csv_Base
csv = __csv_Base()

