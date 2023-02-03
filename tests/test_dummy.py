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
    
def test_df_dup_parent_child():
    # GIVEN a faker dataframe with duplicated values
    # WHEN called from core.df.dummy
    # THEN df has 20,4 shape with certain columns
    df = core.df.dummy.df_dup_parent_child
    
    assert df.shape == (20,4)
    assert all(df.columns == ["parent","child","path","user"])
    
def test_df_country_scores():
    # GIVEN a faker dataframe with 50 countries having scores; two columns
    df = core.df.dummy.df_country_scores
    # CHECK the countries, if seed is ok
    # WHEN called from core.df.dummy
    # THEN should yield the results below
    assert sum(df.score ) == 1275
    assert df.iat[49,0] == 'Germany'
    assert df.iat[0,0] == 'Tanzania'
    assert df.shape == (50,2)
    
    
    
    