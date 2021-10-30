import pandas as pd

import seaborn as sns
from scipy.stats import zscore


def zscore_heatmap(
        dataframe,
        index: str = None,
        head: int = None,
        abs: bool = None):

    heatmap_df = dataframe.copy(deep=True)
    if index:
        heatmap_df.set_index(index, inplace=True)
    if abs:
        heatmap_df = heatmap_df.abs()

    heatmap_df = heatmap_df.apply(zscore)

    if head:
        heatmap_df = heatmap_df.head(head)

    sns.heatmap(heatmap_df, annot=True)
    del heatmap_df
