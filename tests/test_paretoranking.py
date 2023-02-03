""" dataframe helper function tests 
    pareto_ranking module
"""

import pandas as pd
import pytest
from ozcore import core

def test_pareto_ranking_merge():
    # GIVEN dummy df_country_scores from core
    df = core.df.dummy.df_country_scores
    # WHEN paretoranking called from core with scores and dummy df
    pr = core.df.paretoranking(df, 'score')
    # THEN pareto method should return 100 at index 49
    assert pr.pareto.iat[49,0] == 100
    # THEN ranking method should return 100 at index 0
    assert pr.ranking.iat[0,0] == 100
    # THEN merge method should return the whole dataframe with additional two score_ columns
    assert all(pr.merge_pareto_and_ranking.columns.isin(['country', 'score', 'score_pareto', 'score_ranking']))