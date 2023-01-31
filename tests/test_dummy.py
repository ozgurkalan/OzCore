""" test dummy module """

import pytest
import pandas as pd
import numpy as np
from ozcore import core

def test_emp_dummy():
    # GIVEN emp as property
    # WHEN called directly from core.df.dummy
    # THEN returns a record with a shape(10,12)
    assert core.df.dummy.emp.shape == (10,12)
    
@pytest.mark.parametrize(
    "template, n, verbose,expected",
    [
        ("emp", 5, True, (5,12) ),
        ("emp", 1, True, (2,12) ),
        ("wrong_template", 1, True, (2,12) ),
        (None, 1, True, (2,12) )
        
    ]
)
def test_dummy_dataframe_with_n_records(template, n, verbose, expected):
    assert core.df.dummy.dataframe(template=template, n=n, verbose=verbose).shape == expected
    
def test_dummy_df_properties():
    """ df1, df2, df3 """
    # GIVEN dataframes faked with seed 99
    df1 = core.df.dummy.df1
    df2 = core.df.dummy.df2
    df3 = core.df.dummy.df3
    
    assert df1.shape == (5,5)
    assert df1.col5.dtype.type == np.datetime64 # datetime object
    
    assert df2.shape == (5,5)
    assert df2.col5.dtype.type == np.object_ # a dict type object
    
    assert df3.shape == (5,4)
    
    # all three dataframes have first two columns equal
    pd.testing.assert_frame_equal(df1.iloc[:,:2], df3.iloc[:,:2])
    pd.testing.assert_frame_equal(df2.iloc[:,:2], df3.iloc[:,:2])
    
    
    