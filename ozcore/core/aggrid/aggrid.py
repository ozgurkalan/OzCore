""" AG Grid python wrapper 

"""

import pandas as pd
from ipyaggrid import Grid as agGrid


class Grid:
    """  
    wrapper class for ipyaggrid
    
    AG Grid integration with Jupyter Notebook
    """

    def __init__(self):
        """  parameters for grid options"""

    def view(self, df, **kwargs):
        """  
        view a dataframe with AG Grid
        
        parameters:
            df: Dataframe
        
        keyword arguments:
            groupby: list|str, define fields to group by 
                
            enableSorting: bool, default True
            enableFilter: bool, default True
            enableColResize: bool, default True
            enableRangeSelection: bool, default True
            enableRangeHandle: bool, default True
            
            quick_filter: bool, default True
                    
            show_toggle_edit: bool, default False
            export_mode: str, default "disabled"
            export_csv: bool, default False
            export_excel: bool, default False
            show_toggle_delete: bool, default False
            keep_multiindex: bool, default False
            index: bool, default False
            
            theme: str, default 'ag-theme-balham'
            columns_fit: str, default 'auto'
                
            
        returns:
            a dataframe displayed with AG Grid in a Jupyter Notebook
        """

        column_defs = [{"field": k} for k in df.columns]

        grid_options = {
            'enableSorting': True,
            'enableFilter': True,
            'enableColResize': True,
            'enableRangeSelection': True,
            'enableRangeHandle': True,
        }

        settings = {
            "quick_filter": True,

            "show_toggle_edit": False,
            "export_mode": "disabled",
            "export_csv": False,
            "export_excel": False,
            "show_toggle_delete": False,

            "theme": 'ag-theme-balham',
            "columns_fit": 'auto',
            "index": False,
            "keep_multiindex": False,
        }

        for arg in kwargs:
            if arg in grid_options:
                grid_options[arg] = kwargs[arg]
            elif arg in settings:
                settings[arg] = kwargs[arg]
            elif arg == "groupby":
                val = kwargs[arg]
                if not isinstance(val, list):
                    val = [val]
                for field in val:
                    pop = [i for i, e in enumerate(column_defs) if e["field"] == field]
                    if len(pop) == 1:
                        pop = pop[0]
                        column_defs.pop(pop)

        grid_options["columnDefs"] = column_defs

        g = agGrid(
            grid_data=df,
            grid_options=grid_options,
            **settings
        )

        return g
