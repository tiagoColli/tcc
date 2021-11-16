import sys

sys.path.insert(0, '../../')
import pandas as pd
import seaborn as sns

from oam.score.isolation_path import IsolationPath
from oam.search.simple_combination import SimpleCombination


df = pd.read_csv('../../datasets/df_outliers.csv')

correlation_list = []

ipath = IsolationPath(
    subsample_size=256,
    number_of_paths=600
)

search = SimpleCombination(
    ipath,
    min_items_per_subspace=2,
    max_items_per_subspace=4,
    dimensions=['variation_mean', 'variation_std', 'up_count',
                'down_count', 'top_15_variation_mean',
                'top_15_variation_std'],
    multiprocessing=True
)

result_df = search.search(df, 41)
columns = set(result_df.loc[0].subspace)
for subspaces in result_df.subspace[1:]:
    for dimension in subspaces:
        columns.add(dimension)

df2 = pd.DataFrame(columns=columns)

for idx, subspace in enumerate(result_df.subspace):
    for dimension in subspace:
        df2.loc[idx, dimension] = 1

df2.fillna(0, inplace=True)

for idx, score in enumerate(result_df.score):
    df2.loc[idx, 'score'] = score

df2 = df2.head(5)

sns.heatmap(df2, annot=True)