""" dataframe helper function tests 

"""

import pandas as pd
import pytest
from ozcore import core


def test_update_a_dataframe_column():
    # df_to_update, df_as_source, unique_col, col_to_update
    # GIVEN a df having person names in col3 as df_to_update
    df_to_update = core.df.dummy.df1
    # GIVEN another df having person names in col3 as df_as_source
    df_as_source = core.df.dummy.df2
    # GIVEN col1 is unique for two dataframes
    unique_col = "col1"
    # WHEN col3 where person names to be updated
    updated_df = core.df.update_a_df_column(
        df_to_update=df_to_update,
        df_as_source=df_as_source,
        unique_col=unique_col,
        col_to_update="col3",
    )
    # THEN col3 of updated_df should equal to df_as_source's
    pd.testing.assert_series_equal(updated_df.col3, df_as_source.col3)


@pytest.mark.parametrize(
    "df_1, df_2, col_to_compare, side, expected",
    [
        (core.df.dummy.df1, core.df.dummy.df2, "col1", "both", 0),
        (core.df.dummy.df1, core.df.dummy.df2, "col3", "left", 5),
        (core.df.dummy.df1, core.df.dummy.df2, "col3", "left", 5),
        (core.df.dummy.df1, core.df.dummy.df2, "col3", "both", 10),
    ],
)
def test_compare_two_dataframes(df_1, df_2, col_to_compare, side, expected):
    # GIVEN dummy df1, df2 and df3 from core
    # WHEN compared
    # THEN len of df should be expected
    assert (
        len(
            core.df.compare_two_df(
                df_1=df_1, df_2=df_2, col_to_compare=col_to_compare, side=side
            )
        )
        == expected
    )


def test_add_a_column_from_another_dataframe():
    into_df = core.df.dummy.df3  # has no col5
    from_df = core.df.dummy.df1  # col5 is a datetime object
    unique_col = "col1"
    col_to_add = "col5"

    result = core.df.add_a_col_from_a_df(into_df, from_df, unique_col, col_to_add)

    pd.testing.assert_series_equal(from_df.col5, result.col5)


@pytest.mark.parametrize("q, columns", [("derri", None), ("derr", "col3")])
def test_searching_a_dataframe(q, columns):
    # GIVEN core.df.dummy.df1 column `col3`has the value = 'Derrick Smith'
    # WHEN searched
    # THEN result is the first row of the dataframe
    expected = core.df.dummy.df1.iloc[0:1]
    result = core.df.search(core.df.dummy.df1, q, columns)
    pd.testing.assert_frame_equal(expected, result)


def test_png_table(tmp_folder, clean_tmp):
    # GIVEN core.df.dummy.df1 as a sample dataframe
    df = core.df.dummy.df1
    # WHEN saved as png table
    clean_tmp
    core.df.pngTable(
        df,
        save=True,
        in_folder=tmp_folder,
        colwidth_factor=0.15,
        fontsize=9,
        formatFloats=True,
    )
    # THEN Downdloads folder has one png file
    assert len(list(tmp_folder.glob("table-*.png"))) == 1
    clean_tmp


@pytest.mark.parametrize("col, i", [("col1", 0), ("col3", 2)])
def test_cols(col, i):
    # GIVEN core.df.dummy.df1 as a sample dataframe
    df = core.df.dummy.df1

    # WHEN cols is called
    # THEN result is the column index of the dataframe
    expected = df.columns.get_loc(col)
    assert expected == core.df.cols(df)[i][1]


@pytest.mark.parametrize("col, i", [("col1", 0), ("col3", 2)])
def test_col(col, i):
    # GIVEN core.df.dummy.df1 as a sample data
    df = core.df.dummy.df1

    # WHEN col is called with an index
    # THEN result is the column name
    expected = df.columns[i]
    assert expected == core.df.col(df=df, i=i, c=None)

    # WHEN col is called with a column name
    # THEN result is the column index
    expected = df.columns.get_loc(col)
    assert expected == core.df.col(df=df, i=None, c=col)

    # WHEN col is called with both a column name and an index
    # THEN result is matching boolean
    assert core.df.col(df=df, i=i, c=col)

    with pytest.raises(Exception):
        core.df.col(df=df, i=None, c=None)
    # WHEN col is called without a column name or an index
    # THEN raise Exception
