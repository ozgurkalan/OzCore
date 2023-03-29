""" 
Pandas data and dataframe  helper functions for Core

hint:
    can be directly called from core as ``core.df``

basic usage::

    from ozcore import core
    core.df.search(df, q="something")

"""

from typing import List, Union

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from typeguard import typechecked

from ozcore import core


@typechecked
def update_a_df_column(
    df_to_update: DataFrame,
    df_as_source: DataFrame,
    unique_col: str,
    col_to_update: str,
) -> DataFrame:
    """Updates a Dataframe column with a source Dataframe based on their common unique columns

    parameters:
        df_to_update: dataframe, main df to be updated
        df_as_source: dataframe, source df to update the main df
        unique_col: str,
            common columns (should have same name) to match records,
            this unique column must have unique values
        col_to_update: str, which column value to be updated

    returns:
        a copy of the updated DataFrame

    warning:
        index is reset during the update
    """

    # copy df
    df = df_to_update.copy()
    source = df_as_source.copy()

    # reset index: WARNING: drops index if exist
    df.reset_index(inplace=True, drop=True)
    source.reset_index(inplace=True, drop=True)

    # set unique_col as index
    df.set_index(unique_col, inplace=True)
    source.set_index(unique_col, inplace=True)

    # update on series
    df[col_to_update].update(source[col_to_update])

    # reset index: WARNING: puts back the index to first
    df.reset_index(inplace=True, drop=False)
    source.reset_index(inplace=True, drop=False)

    return df


@typechecked
def compare_two_df(
    df_1: DataFrame, df_2: DataFrame, col_to_compare: str, side="both"
) -> DataFrame:
    """
    Compares two dataframes based on a given column, aka given common Series

    warning:
        This comparison is only checking the identical values in a Series. Other columns may not match.

    parameters:
        df_1: dataframe 1
        df_2: dataframe 2
        col_to_compare (str): column to make the comparison, which is common
        side: str, default `both`, options: `left`, `right`

    returns:
        * a dataframe with diffrences of df_1 from df_2
        * empty if all match
    """

    df1 = df_1.copy()
    df2 = df_2.copy()

    df1.sort_values(col_to_compare, inplace=True)
    df2.sort_values(col_to_compare, inplace=True)
    df1.reset_index(drop=False, inplace=True)
    df2.reset_index(drop=False, inplace=True)

    left = df1[~df1[col_to_compare].isin(df2[col_to_compare])]
    right = df2[~df2[col_to_compare].isin(df1[col_to_compare])]
    both = pd.concat([left, right])

    if side == "left":
        return left
    elif side == "right":
        return right
    else:
        return both


@typechecked
def add_a_col_from_a_df(
    into_df: DataFrame, from_df: DataFrame, unique_col: str, col_to_add: str
) -> DataFrame:
    """
    Add a column into a dataframe from another dataframe

    parameters:
        into_df: dataframe, main df, which will be updated with a new column
        from_df: dataframe, source df, which has the column to add into main df
        unique_col: str, column name which is common in both dataframes
        col_to_add: str, column to be added from source dataframe

    returns:
        * main dataframe filled with the new column and values, where unique column matches

    warning:
        this method assumes no index
    """

    main = into_df.copy()
    source = from_df.copy()

    return main.merge(source[[unique_col, col_to_add]], on=unique_col, how="left")


@typechecked
def search(
    df_to_search: DataFrame, q: str, columns: Union[str, list, None] = None
) -> DataFrame:
    """Search all or any column of a dataframe, where columns having str (type: object)

    parameters:
        df_to_search: dataframe to be searched
        q: str, query term
        columns: str | list, default None, columns to search, if None all columns

    returns:
        a dataframe with found records

    note:
        index columns are not included.
    """

    df = df_to_search.copy()

    if columns is None:
        df_cols = df
    elif isinstance(columns, str):
        df_cols = df[[columns]]
    elif isinstance(columns, list):
        df_cols = df[columns]

    return df[
        df_cols.apply(
            lambda x: x.str.contains(q, case=False, na=False).any()
            if x.dtype == "object"
            else x,
            axis=1,
        )
    ]


def cols(df: DataFrame) -> dict:
    """Returns dataframe columns as a dictionary with index positions

    parameters:
        df: dataframe to be searched

    returns:
        dictionary with index positions
    """
    return list(zip(df.columns, df.columns.get_indexer(df.columns)))


@typechecked
def col(df: DataFrame, i: Union[int, None] = None, c: Union[str, None] = None) -> Union[int, str, bool]:
    """Returns a str or int representing a dataframe column name or index
        Or, checks the column name - index if both params given

    parameters:
        df: Pandas dataframe
        i: int, default None, index position to retrieve
        c: str, default None, column name to retrieve index

    returns:
        int, str or bool
    """

    if i is None and c is None:
        raise Exception("either index or column name must be specified")
    elif c is None:
        return df.columns[i]
    elif i is None:
        return df.columns.get_loc(c)
    elif c is not None and i is not None:
        return c == df.columns[i]


@typechecked
def uni(
    df: DataFrame, i: Union[int, list[int], None] = None, c: Union[str, list[str], None] = None
) -> Union[DataFrame, list]:
    """Returns a list or a dataframe containing unique values

    paramaters:
        df: Pandas DataFrame
        i: int | list[int], default is None, index of the columns
        c: str | list[str], default is None, name of the columns

    returns:
        if single parameter given, returns a sorted list,
        otherwise returns a pandas DataFrame with matching unique columns
    """

    if i is None and c is None:
        raise Exception("either index or column name must be specified")
    elif c is None:
        i = [i] if isinstance(i, int) else i
        zf = df.iloc[:, i]

    elif i is None:
        c = [c] if isinstance(c, str) else c
        zf = df.loc[:, c]
    elif c is not None and i is not None:
        pass  # last check is for index, so index is counted

    if zf.shape[1] == 1:
        ll = list(zf.iloc[:, 0].unique())
        ll.sort()
        return ll
    else:
        zf = pd.DataFrame(np.unique(zf.to_records(index=None)), columns=zf.columns)
        return zf


@typechecked
def search_in_multiindex(
    df: DataFrame,
    s: Union[str, int, List],
    axis: int = 0,
):
    """Search multiindex column names or multiindex index names in a dataframe.


    parameters:
        df: Pandas DataFrame, should not be multiindexed.
        s: str or int, column name or index to search for
        axis: int, defaults to 0; rows: 0, columns: 1,


    hint:
        Useful to locate tupled column or index positions

    """
    s = [s]
    ax = None
    if axis == 0:
        ax = df.index
    else:
        ax = df.columns

    for _ in range(ax.nlevels):
        search = ax.get_level_values(_).get_indexer_for(s)
        if not np.isin([-1], search).all():
            result = ax[search]
            break
        else:
            result = None
    return result
