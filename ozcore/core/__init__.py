""" 

initiate some of the modules for fast access with core

note:
    in order not to duplicate variables, some of the modules are called with dunder method 

"""

# # df, utils, aggrid
from ozcore.core import df, utils, aggrid

# path module::Folder
from ozcore.core.path.folders import Folder as __Folder
folder = __Folder()

# # Sqlite
from ozcore.core.data.sqlite.sqlite import Sqlite as sql

# # CSV
from ozcore.core.data.csv.base import Base as __csv_Base
csv = __csv_Base()

