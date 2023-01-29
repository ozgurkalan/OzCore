"""  
Jupyter Notebook helper functions mainly to setup on initial kernel start.

"""
# Jupyter Notebook display options
from IPython.display import display, HTML
import pandas as pd

class Jupyter:
    """  
    Jupyter Notebook helper functions
    
    run setup function in a jupyter notebook, preferably in an init file like `bot_init.ipynb`
    
    usage::

        %reset -f 
        from ozcore.core import jupyter
        jupyter.Jupyter().setup()   

    """
    
    def setup(self):
        """  
        setup Jupyter Notebook with beloved attributes
            - large view
            - pandas view options
        """
        self.large_view()
        self.pandas_view_options()
    
    
    def large_view(self):
        """  
        larger view for Jupyter Notebook
        """    
        # displays a larger container width
        display(HTML(data="""
        <style>
            div#notebook-container    { width: 97%; }
            div#menubar-container     { width: 90%; }
            div#maintoolbar-container { width: 90%; }
        </style>
        """))
        
    def pandas_view_options(self):
        """  
        pandas view options
        """
        pd.reset_option("^display", silent=True) # first reset all display options
        pd.options.display.width=None # reset limits to table width
        pd.options.display.min_rows=None # reset min row to allow max row
        pd.options.display.max_rows=100 # show at least 50 rows
        pd.options.display.max_columns=999 # show all available columns
        pd.options.display.max_colwidth=150 # prevent truncate upto 150 points
        pd.options.display.expand_frame_repr=True # no wrap on tables
        pd.options.display.float_format="{:,.2f}".format # floating numbers with 2 digit + comma