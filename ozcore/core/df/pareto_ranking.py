"""Calculate Pareto and Ranking from a Dataframe"""
from typing import Union

import pandas as pd
from pandas.core.frame import DataFrame


class ParetoRanking:
    """
    calculates pareto and raking from a Dataframe

    paramaters:
        df: Pandas DataFrame
        col: str or list, column(s) in the DataFrame for calcultion
    """

    def __init__(self, df: DataFrame, col: Union[str, list[str]]) -> None:
        self.df = df
        self.col = [col] if isinstance(col, str) else col

    @property
    def pareto(self) -> DataFrame:
        """Calculate pareto percentages from the DataFrame

        returns:
            Series as a Dataframe
        """
        df = pd.DataFrame()
        for col in self.col:
            g = self.df.sort_values(col, ascending=False)[col]
            g = (100 * g.cumsum() / g.sum()).to_frame(f"{col}_pareto")
            df = pd.concat([df, g], axis=1)
        return df

    @property
    def ranking(self) -> DataFrame:
        """Calculate ranking from the DataFrame

        returns:
            Series as a Dataframe
        """
        df = pd.DataFrame()
        for col in self.col:
            g = self.df.sort_values(col, ascending=False)[col]
            g = (100 * g / g.max()).to_frame(f"{col}_ranking")
            df = pd.concat([df, g], axis=1)
        return df

    @property
    def merge_pareto_and_ranking(self) -> DataFrame:
        """Merges pareto and ranking columns in the given DataFrame

        returns:
            The given DataFrame merged with pareto and ranking columns
        """
        return pd.concat([self.df, self.pareto, self.ranking], axis=1)
