import pytest

import pandas as pd

from oam.score.isolation_path import IsolationPath
from oam.search.simple_combination import SimpleCombination


@pytest.fixture
def dataframe():
    return pd.read_csv('../../datasets/df_outliers.csv')


@pytest.fixture
def ipath():
    return IsolationPath(
        subsample_size=50,
        number_of_paths=5
    )


@pytest.fixture
def ipath_sc(ipath):
    return SimpleCombination(
        ipath,
        min_items_per_subspace=2,
        max_items_per_subspace=4,
        dimensions=['variation_mean', 'variation_std', 'up_count',
                    'down_count', 'top_15_variation_mean',
                    'top_15_variation_std'],
        multiprocessing=True
    )


def test_ipath_score(ipath_sc, dataframe):
    score_output = ipath_sc.search(dataframe, 41)
    assert score_output.shape == (35, 3)
