""" 

initiate some of the modules for fast access with core

note:
    in order not to duplicate variables, some of the modules are called with dunder method 

"""

# path module::Folder
from ozcore.core.path.folders import Folder as __Folder
folder = __Folder()  

# Dummy Data
from ozcore.core.data.dummy import Dummy as __Dummy
dummy = __Dummy()

# Dataframe module
from ozcore.core.data.dataframe import Dataframe as __Dataframe
df = __Dataframe()

# # SQL
from ozcore.core.data.sqlite.sqlite import Sqlite as __sqlite
sql = __sqlite()

# # CSV
from ozcore.core.data.csv.base import Base as __csv_Base
csv = __csv_Base()

# # aggrid module
from ozcore.core.aggrid.aggrid import Grid as __agGrid
gridag = __agGrid()

# # utils
from .utils import *
