"""  
View class for qgrid
"""

import ipywidgets as widgets
from IPython.display import display

from .base import Base

class View(Base):
    """  
    class with displaying options for dataframe
    

    view:
        view method to call
            
    _handler_view_selection_changed():
        | helper handler method to display a record below the grid
        | display content can be overriden in your own class
        
    usage::
    
        view(df_slice, handler=True)
    """
    
    def __init__(self):
        super().__init__()
    
    def view(self, df_slice, handler=True, minor=None, **kwargs):
        """  
        display dataframe with qgrid
            qgrid display settings defined in inherited Base class
        
        parameters:
            df_slice: Dataframe to be displayed
            handler: bool, default True, turns on/off preview below grid
            minor: list, columns to display, default None
            
            
        Keyword Arguments:
            show_toolbar: bool, default True
            sortable: bool, default True, causes glitch with editable
            filterable: bool, default True, causes glitch with editable
            forceFitColumns: bool, default True
            rowHeight: int, default 70
            defaultColumnWidth: int, default 150
            maxVisibleRows: int, default 15
            minVisibleRows: int, default 8
            height: str, default "250px"

        returns:
            Jupyter Notebook display with a header, qgrid, footer and selected record block
                
        usage::
        
            from ozcore import core
            core.grid.view(core.dummy.emp, rowHeight=30, handler=False)
        
        """
        # call qgrid
        q = self._qgrid(df_slice=df_slice, minor=minor, **kwargs)
        
        # observe cell change
        if handler:
            q.on(names="selection_changed", handler=self._handler_view_selection_changed)
        
        # Label for displaying shape
        shape_label=widgets.Label(value=f"read-only view => shape: {self.qgrid_shape}")

        # put label in header output
        with self._output_header:
            self._output_header.clear_output()
            display(widgets.Box([shape_label], box_style="info"))
            
        before_footer_label = widgets.Label(
            value="end of df_slice: select a record to view below in detail")
        
        with self._output_before_footer:
            self._output_before_footer.clear_output()
            display(widgets.Box([before_footer_label], box_style="danger"))
        
        after_footer_label = widgets.Label(
            value="~end of display~")
        
        with self._output_after_footer:
            self._output_after_footer.clear_output()
            display(widgets.Box([after_footer_label], box_style="success"))
            
        display(self._output_header)
        self._display_qgrid(q)
        if handler:
            display(self._output_before_footer)
            display(self._output_footer)
            display(self._output_after_footer)
        
        
    
    def _handler_view_selection_changed(self, event, qgrid_widget):
        """  
        event handler for view when qgrid on selection_changed
        
        returns:
            displays selected row in footer single rec Output
        """
        row = event["new"]
        if len(row)<1: # if no keys return None
            return

        # selected df
        df = self.qgrid_object.get_selected_df() 
        
        # the given df_slice
        df_slice = self.qgrid_df_slice
        
        # get the detailed record from given df_slice
        rec = df_slice.loc[df.index.to_list()[0]].to_frame()

        # output to footer
        with self._output_footer:
            self._output_footer.clear_output()
            display(rec)
        
        
    
