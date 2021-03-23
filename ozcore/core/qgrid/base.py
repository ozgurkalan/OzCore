"""  
Base class for qgrid settings

"""

import pandas as pd
import qgrid
import ipywidgets as widgets
from IPython.display import display, Javascript
import time

class Base:
    """  
    base class for qgrid settings
    """

    def __init__(self):
        self.qgrid_options = None  # options are set in class method

        # qgrid info
        self.qgrid_shape = None 
        self.qgrid_object = None  
        self.qgrid_df_slice = None

        # initiate display widget Outputs
        self._output_header = widgets.Output()
        self._output_before_header = widgets.Output()
        self._output_after_header = widgets.Output()
        
        self._output_qgrid = widgets.Output()
        
        self._output_footer = widgets.Output()
        self._output_before_footer = widgets.Output()
        self._output_after_footer = widgets.Output()

    def _display_qgrid(self, q):
        """  
        build qgrid display for Jupyter Notebook
        
        usage::
        
            q = self._qgrid(df_slice=df_slice, **kwargs)
            display_qgrid(q)
            
            # define before any headers to receive qgrid info, e.g. shape
        """
        
        with self._output_qgrid:
            self._output_qgrid.clear_output()  # first clear existing objects
            display(q)

        display(self._output_qgrid)

        time.sleep(0.5)  # sleep short for js injection
        self._clean_qgrid_js()

    def _set_grid_options(self, **kwargs):
        """  
        qgrid grid_options
        kwargs apply to values
        
        parameters:
            kwargs: option values are updated by kwargs
            
        usage::
        
            grid_options(editable=True)
        """
        options = {
            # SlickGrid options
            "fullWidthRows": False,
            "syncColumnCellResize": False,
            "forceFitColumns": False,
            "defaultColumnWidth": 150,
            "rowHeight": 70,
            "enableColumnReorder": False,  # causes glitch
            "enableTextSelectionOnCells": True,
            "editable": False,
            "autoEdit": False,
            "explicitInitialization": True,
            # Qgrid options
            "maxVisibleRows": 15,
            "minVisibleRows": 8,
            "sortable": True,  # causes glitch when editable, should be opposite of editable
            "filterable": True,  # causes glitch when editable, should be opposite of editable
            "highlightSelectedCell": False,
            "highlightSelectedRow": True,
            "height": "250px",
        }

        # update options with kwargs
        options.update({k: v for k, v in kwargs.items() if k in options})

        # causes glitch when editable, should be opposite of editable
        options.update(
            sortable=(not options["editable"]), filterable=(not options["editable"])
        )
        self.qgrid_options = options

    def _qgrid(self, df_slice=None, minor=None, **kwargs):
        """  
        Custom qgrid wrapper

        parameters:
            df_slice: Dataframe to be displayed
            minor: list, columns to display
            kwargs: arguments for qgrid settings

        """

        # check df_slice
        if not (isinstance(df_slice, pd.core.frame.DataFrame)):
            raise TypeError("df_slice must be a valid DataFrame!")
        elif df_slice.empty:
            raise TypeError("df_slice is empty!")
        else:
            self.qgrid_df_slice = df_slice  # given df, to be used in rec details

        # check minor
        if minor is not None:
            if not (isinstance(minor, list)):
                raise TypeError("minor columns must be a valid list object!!")
            elif df_slice.columns.intersection(minor).empty:
                raise Exception("df_slice columns do not match with minor columns!")
            else:
                df_slice = df_slice[df_slice.columns.intersection(minor)]

        # kwargs can set grid options
        self._set_grid_options(**kwargs)

        # column_definitions assigned during show_grid
        # get column_definitions from kwargs
        column_definitions = kwargs.get("column_definitions", {})

        # set all columns read-only unless defined in column_definitions
        for col in df_slice.columns:
            if not col in column_definitions.keys():
                column_definitions[col] = {"editable": False}

        # show qgrid
        q = qgrid.show_grid(df_slice, column_definitions=column_definitions)
        q.show_toolbar = kwargs.get("show_toolbar", True)

        # set grid options
        q.grid_options = self.qgrid_options

        # assign global properties
        self.qgrid_object = q  # for object functions stored
        self.qgrid_shape = df_slice.shape  # shape of final df displayed

        return q

    def _clean_qgrid_js(self):
        """ 
        Javascript injection for qgrid 

        returns: 
            * JS integrated in Jupyter Notebook for Qgrid
            * removes default buttons, 
            * adds a js button,
            * adds js to scroll action of qgrid
        """
        js = Javascript(
            """

        function cleanIt() {
            $('.slick-cell').attr('style','white-space:normal');
            }

        $('.q-grid-toolbar .btn[data-btn-text="Remove Row"]').remove();
        $('.q-grid-toolbar .btn[data-btn-text="Add Row"]').remove();
        $('.q-grid-toolbar').append('<button class="btn btn-default btn-sm fa fa-paint-brush" name="js_clean_grid">js</button>');
        $('.q-grid-toolbar .btn[name="js_clean_grid"]').click(cleanIt);
        slick_grid.onScroll.subscribe(cleanIt);

        """
        )

        display(js)
