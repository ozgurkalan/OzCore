""" 

initiate some of the modules for fast access with core

note:
    in order not to duplicate variables, some of the modules are called with dunder method 

"""

# # df and utils
from ozcore.core import df, utils
# path module::Folder
from ozcore.core.path.folders import Folder as __Folder

folder = __Folder()

# # Sqlite
from ozcore.core.data.sqlite.sqlite import Sqlite as sql

# # CSV
from ozcore.core.data.csv.base import Base as __csv_Base

csv = __csv_Base()

# # aggrid module
from ozcore.core.aggrid.aggrid import Grid as __agGrid

view = __agGrid().view
