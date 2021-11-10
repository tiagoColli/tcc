import pandas as pd

import seaborn as sns
from scipy.stats import zscore


def zscore_heatmap(
        dataframe: pd.DataFrame,
        index: str = None,
        head: int = None,
        abs: bool = None,
        return_dataframe: bool = False):
    ''' The z-score also know as standard score is the number of standard
    deviations by which the value of a raw score is above or below the mean and
    can be used to analyse how deviant an observation is from the rest of the
    distribution.

    This function provides not only z-score for the given dataframe but also
    presents it in the form of a heatmap.

        Args:
            **df** (pandas.DataFrame): The dataframe to be transformed

            **index** (str): The index of the dataframe e.g. the datetime of
            each row.

            **max** (int): The number of rows to be presented in the heatmap.

            **abs** (bool): Present only abosulte values.

            **return_dataframe** (bool): The possibility of returning the
            zscore dataframe or only presenting the heatmap.

        Returns:
            (pd.Dataframe): Transformed dataframe'''

    heatmap_df = dataframe.copy(deep=True)
    if index:
        heatmap_df.set_index(index, inplace=True)
    if abs:
        heatmap_df = heatmap_df.abs()

    heatmap_df = heatmap_df.apply(zscore)

    if head:
        heatmap_df = heatmap_df.head(head)

    sns.heatmap(heatmap_df, annot=True)
    if return_dataframe:
        return heatmap_df

    del heatmap_df
