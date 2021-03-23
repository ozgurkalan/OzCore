"""  
qgrid abstract class
"""

from .view import View
class Grid(View):
    """  
    abstract class for calling qgrid
    
    inherits:
        Base class
        View class
    
    methods:
        * view: displays with settings in Base class
        * edit: abstract method, to be implemented
        
    helper methods:
        | _handler_view_selection_changed()
        | already implemented in View class, can be altered by re-defining
            
    usage::
    
        # simple usage:
        from ozcore import core
        core.gridq.view(dataframe)
    
        # integrate with inner class:
        from ozcore.core.qgrid_.grid import Grid
        
        class MySampleClass:
            ....
            def grid(self):
                # call grid's inner class
                _grid = self._View()
                _grid.view(df_slice=self.df)
                
            class _View(Grid):
                # inner class to inherit core > qgrid > view method

                def __init__(self, cards=False):
                    super().__init__()

                def _handler_view_selection_changed(self, event, qgrid_widget):
                # ....  override handler
                def edit()
                # .... override edit
                        
    """
    
    def __init__(self):
        super().__init__()
        
    def edit(self, df_slice, **kwargs):
        """  
        edit qgrid fields
        
        NotImplemented
        """
        raise NotImplementedError("edit is not implemented yet!")