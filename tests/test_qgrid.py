""" 
Qgrid module tests

"""
import pytest
import pandas as pd
from ozcore import core

def test_exceptions():
    # GIVEN a dummy Dataframe with 5 columns and 5 records
    df = core.dummy.df1
    
    with pytest.raises(TypeError):
        # WHEN minor is not a valid list object
        core.gridq.view(df_slice=df, handler=False, minor="col1")
        
    with pytest.raises(Exception):
        # WHEN col7 does not exist
        core.gridq.view(df_slice=df, handler=False, minor=["col7"])
        
    with pytest.raises(NotImplementedError):
        # WHEN edit called from abstract class
        core.gridq.edit(df)
        
    with pytest.raises(Exception):
        # WHEN Series given
        core.gridq.view(df.col1)
        
    with pytest.raises(Exception):
        # WHEN Dataframe is empty
        core.gridq.view(pd.DataFrame())
        
    
