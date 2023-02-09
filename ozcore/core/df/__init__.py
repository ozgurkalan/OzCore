# Pandas related helper functions and dummies
from .dataframe import (
    update_a_df_column,
    pngTable,
    compare_two_df,
    add_a_col_from_a_df,
    search,
    cols,
    col,
    uni,
    search_in_multiindex,
)

from .dummy import Dummy as __Dummy

dummy = __Dummy()

from .pareto_ranking import ParetoRanking as __ParetoRanking

paretoranking = __ParetoRanking

__all__ = [
    "update_a_df_column",
    "pngTable",
    "compare_two_df",
    "add_a_col_from_a_df",
    "search",
    "cols",
    "col",
    "uni",
    "search_in_multiindex",
    "dummy",
    "paretoranking",
]
