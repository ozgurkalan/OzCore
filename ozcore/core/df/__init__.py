# check_module
from ..utils.__import_check import check_modules

# Pandas related helper functions and dummies
from .dataframe import (
    update_a_df_column,
    compare_two_df,
    add_a_col_from_a_df,
    search,
    cols,
    col,
    uni,
    search_in_multiindex,
)

# Pareto ranking
from .pareto_ranking import ParetoRanking as __ParetoRanking
paretoranking = __ParetoRanking

__all__ = [
    "update_a_df_column",
    "compare_two_df",
    "add_a_col_from_a_df",
    "search",
    "cols",
    "col",
    "uni",
    "search_in_multiindex",
    "paretoranking",
]

# faker - dummy data
if check_modules("faker"):
    from .dummy import Dummy as __Dummy
    dummy = __Dummy()
    __all__ += ["dummy"]





