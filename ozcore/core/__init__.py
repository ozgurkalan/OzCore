""" 

initiate some of the modules for fast access with core

note:
    in order not to duplicate variables, some of the modules are called with dunder method 

"""
# helper functions
from ozcore.core.helpers import (
    now_prefix, # datetime str for now or today
    clean_html, # clean html and return markdown
    md_2_html, # convert markdown to html
    translate, # translate text with Google,
    dirme, # lists methods of a given module
    serialize_a_json_field, # validate and join nodes of json or dict
)


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

# # Qgrid module
from ozcore.core.qgrid.grid import Grid as __qGrid
gridq = __qGrid()

# # aggrid module
from ozcore.core.aggrid.aggrid import Grid as __agGrid
gridag = __agGrid()