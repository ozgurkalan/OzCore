""" 
Base class for csv operations 

"""

import logging
from pathlib import Path, PosixPath, WindowsPath
from typing import Union

import pandas as pd
from pandas.core.frame import DataFrame
from typeguard import typechecked


class Base:
    """
    Base class for csv operations.

    Usage::

        from ozcore import core

        csv = core.csv

        csv.read("path_to_csv_file", **kwargs)

        csv.save(df_altered, index=False, verbose=False, overwrite=False, **kwargs)
        # warning: this saves over the read csv file!

        csv.search(q="something")
        # searches every column

        # but if certain columns desired to be searched than define it before action
        csv.searchable = ["col1"]
        csv.search(q="something in col1")

    """

    def __init__(self):
        self._actual_df = pd.DataFrame()  # initiate
        self.df = self._actual_df.copy()  # get a undestructed copy from read csv
        self.searchable = None  # columns to search
        self.path = None

    @typechecked
    def read(
        self, path: Union[str, PosixPath, WindowsPath], verbose: bool = True, **kwargs
    ):
        """
        read a csv file

        parameters:
            path: str|posixpath, path to csv file
            verbose: bool, default: True, logging success
            kwargs: pandas read_csv arguments

        returns:
            fills self.actual_df and self.df
        """

        if isinstance(path, str):
            path = Path(path)

        if not path.exists() or path.suffix != ".csv":
            logging.error("File path is not valid!")
            raise Exception("something wrong! please check your path to csv!")

        self.path = path

        df = pd.read_csv(path, **kwargs)

        self._actual_df = df
        self.df = df

        if verbose:
            logging.warning(f"csv is loaded: " + path.name)
            return df

    @typechecked
    def save(
        self,
        df_altered: DataFrame,
        index: bool = False,
        verbose: bool = False,
        overwrite: bool = False,
        **kwargs,
    ):
        """
        saves altered dataframe on the csv file

        paramaters:
            df_altered: Dataframe
            index: bool, default False, if index will be saved in csv
            verbose: bool, default False, logging success
            overwrite: bool, default False, if overwrite allowed
            kwargs: pandas to_csv arguments

        returns:
            logging if verbose is True

        warning:
            if overwrite is True, dumps given df into file without checking its len with actual_df
        """

        actual = self._actual_df

        if not self.path or actual.empty or df_altered.empty:
            logging.error("dataframes are empty!")
            raise Exception("something wrong! Dataframes are empty")

        if not overwrite:  # checks if its the same len as actual_df
            if len(df_altered) != len(actual) or not (
                actual.iloc[:, 0].isin(df_altered.iloc[:, 0]).all()
            ):
                logging.error("Dataframe is suspicous!")
                raise Exception(
                    "something wrong! please check your dataframe! or mark overwrite=True"
                )

        df_altered.to_csv(self.path, index=index, **kwargs)
        self.df = df_altered
        if verbose:
            logging.warning("file saved!")

    @typechecked
    def search(self, q: str) -> DataFrame:
        """
        search records based on self._searchable argument (col name to search given in child classes)

        returns:
            dataframe slice from search results
        """

        df = self.df
        if self.searchable and len(self.searchable) > 0:
            return df[df[self.searchable].str.contains(q, case=False, na=False)]
        else:
            return df[
                df.apply(
                    lambda x: x.str.contains(q, case=False, na=False).any()
                    if x.dtype == "object"
                    else x,
                    axis=1,
                )
            ]
